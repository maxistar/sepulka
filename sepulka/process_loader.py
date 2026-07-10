from pathlib import Path
from typing import Any

import yaml


DEFAULT_PROCESSES_DIR = Path(__file__).resolve().parent.parent / "processes"
REQUIRED_PROCESS_FIELDS = {"id", "name", "description", "suitable_for", "steps", "expected_outputs"}
REQUIRED_STEP_FIELDS = {"id", "name", "prompt"}
REQUIRED_INTAKE_FIELDS = {"id", "question"}


class ProcessValidationError(ValueError):
    pass


def load_process(process_id: str, processes_dir: Path = DEFAULT_PROCESSES_DIR) -> dict[str, Any]:
    path = processes_dir / f"{process_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Process file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        process = yaml.safe_load(file)

    _validate_process(process, path)
    return process


def load_all_processes(processes_dir: Path = DEFAULT_PROCESSES_DIR) -> list[dict[str, Any]]:
    return [load_process(path.stem, processes_dir) for path in sorted(processes_dir.glob("*.yaml"))]


def _validate_process(process: Any, path: Path) -> None:
    if not isinstance(process, dict):
        raise ProcessValidationError(f"Process file {path} must contain a YAML mapping.")

    missing = sorted(REQUIRED_PROCESS_FIELDS - set(process))
    if missing:
        raise ProcessValidationError(f"Process file {path} is missing required fields: {', '.join(missing)}")

    if not isinstance(process["steps"], list) or not process["steps"]:
        raise ProcessValidationError(f"Process file {path} field 'steps' must be a non-empty list.")

    for index, step in enumerate(process["steps"], start=1):
        if not isinstance(step, dict):
            raise ProcessValidationError(f"Process file {path} step {index} must be a YAML mapping.")

        missing_step_fields = sorted(REQUIRED_STEP_FIELDS - set(step))
        if missing_step_fields:
            fields = ", ".join(missing_step_fields)
            raise ProcessValidationError(f"Process file {path} step {index} is missing required fields: {fields}")

    if "intake_questions" in process:
        _validate_intake_questions(process["intake_questions"], path)


def _validate_intake_questions(intake_questions: Any, path: Path) -> None:
    if not isinstance(intake_questions, list):
        raise ProcessValidationError(f"Process file {path} field 'intake_questions' must be a list when present.")

    for index, question in enumerate(intake_questions, start=1):
        if not isinstance(question, dict):
            raise ProcessValidationError(f"Process file {path} intake question {index} must be a YAML mapping.")

        missing_fields = sorted(REQUIRED_INTAKE_FIELDS - set(question))
        if missing_fields:
            fields = ", ".join(missing_fields)
            raise ProcessValidationError(
                f"Process file {path} intake question {index} is missing required fields: {fields}"
            )
