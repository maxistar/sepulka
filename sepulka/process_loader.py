from pathlib import Path
from typing import Any

import yaml


DEFAULT_PROCESSES_DIR = Path(__file__).resolve().parent.parent / "processes"


def load_process(process_id: str, processes_dir: Path = DEFAULT_PROCESSES_DIR) -> dict[str, Any]:
    path = processes_dir / f"{process_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Process file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        process = yaml.safe_load(file)

    required = {"id", "name", "description", "suitable_for", "steps", "expected_outputs"}
    missing = sorted(required - set(process))
    if missing:
        raise ValueError(f"Process {path} is missing fields: {', '.join(missing)}")

    return process


def load_all_processes(processes_dir: Path = DEFAULT_PROCESSES_DIR) -> list[dict[str, Any]]:
    return [load_process(path.stem, processes_dir) for path in sorted(processes_dir.glob("*.yaml"))]
