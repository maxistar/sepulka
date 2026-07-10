import argparse
from datetime import datetime
import json
import re
import sys
from typing import TextIO

from .llm import LLMClient, LLMError
from .notes import read_notes, write_note
from .process_loader import load_process
from .process_runner import ProcessRunner, SYSTEM_PROMPT, response_language_hint
from .router import choose_process


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sepulka cognitive assistant")
    parser.add_argument("problem", help="Problem description to analyze")
    parser.add_argument("--fast", action="store_true", help="Skip intake questions and run one-shot analysis")
    parser.add_argument("--save-note", action="store_true", help="Save the final analysis to notes/")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    routing = choose_process(args.problem)
    process = load_process(routing.process_id)
    matching_notes = read_notes(args.problem)

    print(f"Selected process: {process['id']} - {process['name']}")
    print(f"Selection reason: {routing.reason}")
    print()

    try:
        llm = LLMClient()
        intake_answers = []
        if should_run_intake(args.fast, _is_interactive(), process):
            questions = intake_questions_for_problem(llm, args.problem, process)
            intake_answers = collect_intake_answers(process, questions=questions)
        runner = ProcessRunner(llm)
        result = runner.run(args.problem, process, matching_notes, intake_answers)
    except LLMError as error:
        print(f"LLM error: {error}", file=sys.stderr)
        print("Create .env from .env.example and check your OpenAI-compatible endpoint.", file=sys.stderr)
        return 2

    memory = result["memory"]
    final_answer = result["final_answer"]
    note_content = memory.as_markdown() + "\n\n" + final_answer

    print("Intermediate analysis:")
    for step in memory.steps:
        print(f"\n## {step['title']}\n{step['result']}")

    print("\nFinal recommendations:")
    print(final_answer)

    if args.save_note:
        _save_analysis(process["id"], note_content)
    elif _is_interactive():
        _prompt_save_analysis(process["id"], note_content)
    else:
        print("\nTo save this result, rerun with --save-note.")

    return 0


def should_run_intake(fast: bool, interactive: bool, process: dict) -> bool:
    return not fast and interactive and bool(process.get("intake_questions"))


def intake_questions_for_problem(llm: LLMClient, problem: str, process: dict) -> list[dict[str, str]]:
    generated = generate_contextual_intake_questions(llm, problem, process)
    return generated or process.get("intake_questions", [])


def generate_contextual_intake_questions(llm: LLMClient, problem: str, process: dict) -> list[dict[str, str]]:
    prompt = process.get("contextual_intake_prompt")
    if not prompt:
        return []

    language_hint = response_language_hint(problem)
    user_prompt = f"""Problem:
{problem}

Language instruction:
{language_hint}
Generate all intake questions in that language.

Process:
{process['name']} - {process['description']}

Contextual intake instruction:
{prompt}

Return only JSON with this shape:
{{
  "option_a": "short concrete option if available",
  "option_b": "short concrete option if available",
  "questions": [
    {{"id": "option_a_attraction", "question": "..."}},
    {{"id": "option_b_attraction", "question": "..."}},
    {{"id": "option_a_risk", "question": "..."}},
    {{"id": "option_b_risk", "question": "..."}},
    {{"id": "constraints", "question": "..."}}
  ]
}}"""

    try:
        content = llm.chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ]
        )
    except LLMError:
        return []

    return parse_contextual_intake_questions(content)


def parse_contextual_intake_questions(content: str) -> list[dict[str, str]]:
    try:
        data = json.loads(_strip_json_fences(content))
    except json.JSONDecodeError:
        return []

    questions = data.get("questions") if isinstance(data, dict) else None
    if not isinstance(questions, list):
        return []

    valid_questions = []
    for item in questions:
        if not isinstance(item, dict):
            continue
        question_id = item.get("id")
        question = item.get("question")
        if isinstance(question_id, str) and isinstance(question, str) and question_id.strip() and question.strip():
            valid_questions.append({"id": question_id.strip(), "question": question.strip()})

    return valid_questions


def _strip_json_fences(content: str) -> str:
    text = content.strip()
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


def collect_intake_answers(
    process: dict,
    questions: list[dict[str, str]] | None = None,
    input_stream: TextIO = sys.stdin,
    output_stream: TextIO = sys.stdout,
) -> list[dict[str, str]]:
    questions = questions if questions is not None else process.get("intake_questions", [])
    if not questions:
        return []

    print("Before building the analysis, I need a bit more context.", file=output_stream)
    answers = []
    for index, item in enumerate(questions, start=1):
        question = item["question"]
        print(f"\n{index}. {question}", file=output_stream)
        print("> ", end="", file=output_stream, flush=True)
        answer = input_stream.readline().strip()
        if answer:
            answers.append({"id": item["id"], "question": question, "answer": answer})

    if answers:
        print("\nNow building the analysis...\n", file=output_stream)
    else:
        print("\nNo intake answers provided. Continuing with one-shot analysis...\n", file=output_stream)
    return answers


def analysis_note_title(process_id: str, now: datetime | None = None) -> str:
    timestamp = (now or datetime.now()).strftime("%Y-%m-%d-%H%M%S")
    return f"{timestamp}-analysis-{process_id}"


def _is_interactive() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def _prompt_save_analysis(process_id: str, content: str) -> None:
    answer = input("\nSave this result as a markdown note? [y/N] ").strip().lower()
    if answer in {"y", "yes"}:
        _save_analysis(process_id, content)
    else:
        print("To save this result later, rerun with --save-note.")


def _save_analysis(process_id: str, content: str) -> None:
    note_path = write_note(analysis_note_title(process_id), content)
    print(f"\nSaved note: {note_path}")
