import argparse
import sys

from .llm import LLMClient, LLMError
from .notes import read_notes, write_note
from .process_loader import load_process
from .process_runner import ProcessRunner
from .router import choose_process


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sepulka cognitive assistant")
    parser.add_argument("problem", help="Problem description to analyze")
    parser.add_argument("--save-note", action="store_true", help="Save the final analysis to notes/")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    process_id = choose_process(args.problem)
    process = load_process(process_id)
    matching_notes = read_notes(args.problem)

    try:
        runner = ProcessRunner(LLMClient())
        result = runner.run(args.problem, process, matching_notes)
    except LLMError as error:
        print(f"LLM error: {error}", file=sys.stderr)
        print("Create .env from .env.example and check your OpenAI-compatible endpoint.", file=sys.stderr)
        return 2

    memory = result["memory"]
    final_answer = result["final_answer"]

    print(f"Selected process: {process['id']} - {process['name']}")
    print()
    print("Intermediate analysis:")
    for step in memory.steps:
        print(f"\n## {step['title']}\n{step['result']}")

    print("\nFinal recommendations:")
    print(final_answer)

    if args.save_note:
        note_path = write_note(f"analysis-{process['id']}", memory.as_markdown() + "\n\n" + final_answer)
        print(f"\nSaved note: {note_path}")
    else:
        print("\nTo save this result, rerun with --save-note.")

    return 0
