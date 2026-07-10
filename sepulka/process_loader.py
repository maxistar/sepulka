from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SKILLS_DIR = PROJECT_ROOT / "skills"
REQUIRED_PROCESS_FIELDS = {"id", "name", "description", "suitable_for", "steps", "expected_outputs"}
REQUIRED_SKILL_FIELDS = REQUIRED_PROCESS_FIELDS | {"kind", "schema_version"}
REQUIRED_STEP_FIELDS = {"id", "name", "prompt"}
REQUIRED_INTAKE_FIELDS = {"id", "question"}
SKILL_KIND = "thinking_skill"


class ProcessValidationError(ValueError):
    pass


def load_process(process_id: str, skills_dir: Path = DEFAULT_SKILLS_DIR) -> dict[str, Any]:
    skill_path = skill_file_path(process_id, skills_dir)
    if not skill_path.exists():
        raise FileNotFoundError(f"No thinking skill found for id '{process_id}' at {skill_path}")

    return _load_yaml_file(skill_path)


def load_all_processes(skills_dir: Path = DEFAULT_SKILLS_DIR) -> list[dict[str, Any]]:
    ids = sorted(path.parent.name for path in skills_dir.glob("*/skill.yaml"))
    return [load_process(process_id, skills_dir) for process_id in ids]


def skill_file_path(skill_id: str, skills_dir: Path = DEFAULT_SKILLS_DIR) -> Path:
    return skills_dir / skill_id / "skill.yaml"


def _load_yaml_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        process = yaml.safe_load(file)

    _validate_process(process, path)
    return process


def _validate_process(process: Any, path: Path) -> None:
    if not isinstance(process, dict):
        raise ProcessValidationError(f"Skill file {path} must contain a YAML mapping.")

    missing = sorted(REQUIRED_SKILL_FIELDS - set(process))
    if missing:
        raise ProcessValidationError(f"Skill file {path} is missing required fields: {', '.join(missing)}")

    if process.get("kind") != SKILL_KIND:
        raise ProcessValidationError(f"Skill file {path} field 'kind' must be '{SKILL_KIND}'.")
    if not isinstance(process.get("schema_version"), str):
        raise ProcessValidationError(f"Skill file {path} field 'schema_version' must be a string.")

    if not isinstance(process["steps"], list) or not process["steps"]:
        raise ProcessValidationError(f"Skill file {path} field 'steps' must be a non-empty list.")

    for index, step in enumerate(process["steps"], start=1):
        if not isinstance(step, dict):
            raise ProcessValidationError(f"Skill file {path} step {index} must be a YAML mapping.")

        missing_step_fields = sorted(REQUIRED_STEP_FIELDS - set(step))
        if missing_step_fields:
            fields = ", ".join(missing_step_fields)
            raise ProcessValidationError(f"Skill file {path} step {index} is missing required fields: {fields}")

    if "intake_questions" in process:
        _validate_intake_questions(process["intake_questions"], path)

    if "contextual_intake_prompt" in process and not isinstance(process["contextual_intake_prompt"], str):
        raise ProcessValidationError(f"Skill file {path} field 'contextual_intake_prompt' must be a string when present.")


def _validate_intake_questions(intake_questions: Any, path: Path) -> None:
    if not isinstance(intake_questions, list):
        raise ProcessValidationError(f"Skill file {path} field 'intake_questions' must be a list when present.")

    for index, question in enumerate(intake_questions, start=1):
        if not isinstance(question, dict):
            raise ProcessValidationError(f"Skill file {path} intake question {index} must be a YAML mapping.")

        missing_fields = sorted(REQUIRED_INTAKE_FIELDS - set(question))
        if missing_fields:
            fields = ", ".join(missing_fields)
            raise ProcessValidationError(
                f"Skill file {path} intake question {index} is missing required fields: {fields}"
            )
