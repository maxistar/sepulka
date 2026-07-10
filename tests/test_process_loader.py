from pathlib import Path
import tempfile
import unittest

from sepulka.process_loader import ProcessValidationError, load_process


VALID_PROCESS = """
id: demo
name: Demo
description: Demo process
suitable_for:
  - tests
steps:
  - id: step
    name: Step
    prompt: Do the step.
expected_outputs:
  - result
"""


class ProcessLoaderTests(unittest.TestCase):
    def test_process_without_intake_questions_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "demo.yaml"
            path.write_text(VALID_PROCESS, encoding="utf-8")

            process = load_process("demo", Path(directory))

        self.assertEqual(process["id"], "demo")

    def test_intake_question_requires_question_field(self) -> None:
        process_text = VALID_PROCESS + """
intake_questions:
  - id: missing_question
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "demo.yaml"
            path.write_text(process_text, encoding="utf-8")

            with self.assertRaises(ProcessValidationError) as error:
                load_process("demo", Path(directory))

        self.assertIn("intake question 1", str(error.exception))
        self.assertIn("question", str(error.exception))


if __name__ == "__main__":
    unittest.main()
