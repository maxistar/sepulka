import argparse
import sys
from typing import TextIO

from .llm import LLMClient, LLMError
from .notes import read_notes, write_note
from .process_loader import load_process
from .process_runner import ProcessRunner
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
            intake_answers = collect_intake_answers(process)
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


def collect_intake_answers(process: dict, input_stream: TextIO = sys.stdin, output_stream: TextIO = sys.stdout) -> list[dict[str, str]]:
    questions = process.get("intake_questions", [])
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


def _is_interactive() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def _prompt_save_analysis(process_id: str, content: str) -> None:
    answer = input("\nSave this result as a markdown note? [y/N] ").strip().lower()
    if answer in {"y", "yes"}:
        _save_analysis(process_id, content)
    else:
        print("To save this result later, rerun with --save-note.")


def _save_analysis(process_id: str, content: str) -> None:
    note_path = write_note(f"analysis-{process_id}", content)
    print(f"\nSaved note: {note_path}")
