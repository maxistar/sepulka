from datetime import datetime
import io
import unittest

from sepulka.main import (
    analysis_note_title,
    build_parser,
    collect_intake_answers,
    generate_contextual_intake_questions,
    intake_questions_for_problem,
    should_run_intake,
)


PROCESS_WITH_INTAKE = {
    "id": "goldratt_conflict_cloud",
    "name": "Goldratt Conflict Cloud",
    "description": "Finds assumptions behind a dilemma.",
    "contextual_intake_prompt": "Generate concrete questions.",
    "intake_questions": [
        {"id": "first", "question": "What makes the first side attractive?"},
        {"id": "second", "question": "What makes the other side attractive?"},
    ],
}


class FakeLLM:
    def __init__(self, response: str) -> None:
        self.response = response
        self.calls = []

    def chat(self, messages, temperature=0.2):
        self.calls.append(messages)
        return self.response


class MainModeTests(unittest.TestCase):
    def test_fast_flag_parses(self) -> None:
        args = build_parser().parse_args(["--fast", "problem"])

        self.assertTrue(args.fast)
        self.assertEqual(args.problem, "problem")

    def test_interactive_process_with_questions_runs_intake(self) -> None:
        self.assertTrue(should_run_intake(False, True, PROCESS_WITH_INTAKE))

    def test_fast_mode_skips_intake(self) -> None:
        self.assertFalse(should_run_intake(True, True, PROCESS_WITH_INTAKE))

    def test_non_interactive_skips_intake(self) -> None:
        self.assertFalse(should_run_intake(False, False, PROCESS_WITH_INTAKE))

    def test_process_without_questions_skips_intake(self) -> None:
        self.assertFalse(should_run_intake(False, True, {"id": "problem_framing"}))

    def test_collect_intake_answers_stores_non_empty_answers(self) -> None:
        input_stream = io.StringIO("first answer\n\n")
        output_stream = io.StringIO()

        answers = collect_intake_answers(PROCESS_WITH_INTAKE, input_stream=input_stream, output_stream=output_stream)

        self.assertEqual(
            answers,
            [{"id": "first", "question": "What makes the first side attractive?", "answer": "first answer"}],
        )

    def test_contextual_intake_generation_uses_fake_llm_questions(self) -> None:
        fake_llm = FakeLLM(
            '{"questions":[{"id":"quit_risk","question":"Что плохого случится, если ты уволишься?"}]}'
        )

        questions = generate_contextual_intake_questions(fake_llm, "Уволиться или остаться?", PROCESS_WITH_INTAKE)

        self.assertEqual(questions, [{"id": "quit_risk", "question": "Что плохого случится, если ты уволишься?"}])

    def test_contextual_intake_invalid_json_falls_back_to_static_questions(self) -> None:
        fake_llm = FakeLLM("not json")

        questions = intake_questions_for_problem(fake_llm, "Уволиться или остаться?", PROCESS_WITH_INTAKE)

        self.assertEqual(questions, PROCESS_WITH_INTAKE["intake_questions"])

    def test_contextual_intake_prompt_includes_language_instruction(self) -> None:
        fake_llm = FakeLLM('{"questions":[]}')

        generate_contextual_intake_questions(fake_llm, "Уволиться или остаться?", PROCESS_WITH_INTAKE)

        prompts = "\n\n".join(message["content"] for call in fake_llm.calls for message in call)
        self.assertIn("Respond in Russian", prompts)
        self.assertIn("Generate all intake questions in that language", prompts)

    def test_analysis_note_title_includes_timestamp_and_process(self) -> None:
        title = analysis_note_title("goldratt_conflict_cloud", datetime(2026, 7, 10, 14, 35, 22))

        self.assertEqual(title, "2026-07-10-143522-analysis-goldratt_conflict_cloud")


if __name__ == "__main__":
    unittest.main()
