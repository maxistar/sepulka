from pathlib import Path
import tempfile
import unittest

from sepulka.process_loader import ProcessValidationError, load_process


VALID_SKILL = """
kind: thinking_skill
schema_version: "1"
id: demo
name: Demo Skill
description: Demo skill
suitable_for:
  - tests
steps:
  - id: skill_step
    name: Skill Step
    prompt: Do the skill step.
expected_outputs:
  - skill result
"""


class ProcessLoaderTests(unittest.TestCase):
    def test_skill_file_loads_from_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills_dir = Path(directory) / "skills"
            (skills_dir / "demo").mkdir(parents=True)
            (skills_dir / "demo" / "skill.yaml").write_text(VALID_SKILL, encoding="utf-8")

            process = load_process("demo", skills_dir)

        self.assertEqual(process["name"], "Demo Skill")
        self.assertEqual(process["steps"][0]["id"], "skill_step")

    def test_missing_skill_id_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError) as error:
                load_process("missing", Path(directory) / "skills")

        self.assertIn("No thinking skill found", str(error.exception))
        self.assertIn("missing", str(error.exception))

    def test_skill_requires_metadata(self) -> None:
        missing_metadata = """
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
        with tempfile.TemporaryDirectory() as directory:
            skills_dir = Path(directory) / "skills"
            (skills_dir / "demo").mkdir(parents=True)
            (skills_dir / "demo" / "skill.yaml").write_text(missing_metadata, encoding="utf-8")

            with self.assertRaises(ProcessValidationError) as error:
                load_process("demo", skills_dir)

        self.assertIn("kind", str(error.exception))
        self.assertIn("schema_version", str(error.exception))

    def test_intake_question_requires_question_field(self) -> None:
        skill_text = VALID_SKILL + """
intake_questions:
  - id: missing_question
"""
        with tempfile.TemporaryDirectory() as directory:
            skills_dir = Path(directory) / "skills"
            (skills_dir / "demo").mkdir(parents=True)
            (skills_dir / "demo" / "skill.yaml").write_text(skill_text, encoding="utf-8")

            with self.assertRaises(ProcessValidationError) as error:
                load_process("demo", skills_dir)

        self.assertIn("intake question 1", str(error.exception))
        self.assertIn("question", str(error.exception))

    def test_contextual_intake_prompt_must_be_string(self) -> None:
        skill_text = VALID_SKILL + """
contextual_intake_prompt:
  - invalid
"""
        with tempfile.TemporaryDirectory() as directory:
            skills_dir = Path(directory) / "skills"
            (skills_dir / "demo").mkdir(parents=True)
            (skills_dir / "demo" / "skill.yaml").write_text(skill_text, encoding="utf-8")

            with self.assertRaises(ProcessValidationError) as error:
                load_process("demo", skills_dir)

        self.assertIn("contextual_intake_prompt", str(error.exception))

    def test_goldratt_skill_preserves_contextual_intake(self) -> None:
        process = load_process("goldratt_conflict_cloud")

        self.assertEqual(process["kind"], "thinking_skill")
        self.assertIn("contextual_intake_prompt", process)
        self.assertTrue(process["intake_questions"])


if __name__ == "__main__":
    unittest.main()
