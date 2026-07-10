import io
import unittest

from sepulka.main import build_parser, collect_intake_answers, should_run_intake


PROCESS_WITH_INTAKE = {
    "id": "goldratt_conflict_cloud",
    "intake_questions": [
        {"id": "first", "question": "What makes the first side attractive?"},
        {"id": "second", "question": "What makes the other side attractive?"},
    ],
}


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

        answers = collect_intake_answers(PROCESS_WITH_INTAKE, input_stream, output_stream)

        self.assertEqual(
            answers,
            [{"id": "first", "question": "What makes the first side attractive?", "answer": "first answer"}],
        )


if __name__ == "__main__":
    unittest.main()
