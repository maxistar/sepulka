from dataclasses import dataclass, field


@dataclass
class WorkingMemory:
    """Small in-memory store for one reasoning session.

    The runner writes every process step here. In a larger system this could be
    persisted, summarized, or linked to user notes, but the MVP keeps it simple.
    """

    problem: str
    process_id: str
    notes_context: list[dict[str, str]] = field(default_factory=list)
    steps: list[dict[str, str]] = field(default_factory=list)

    def add_step_result(self, step_id: str, title: str, result: str) -> None:
        self.steps.append({"id": step_id, "title": title, "result": result})

    def as_prompt_context(self) -> str:
        if not self.steps:
            return "No previous steps yet."

        blocks = []
        for step in self.steps:
            blocks.append(f"Step {step['id']} - {step['title']}:\n{step['result']}")
        return "\n\n".join(blocks)

    def as_markdown(self) -> str:
        lines = [f"# Sepulka Analysis", "", f"Problem: {self.problem}", "", f"Process: {self.process_id}", ""]
        for step in self.steps:
            lines.extend([f"## {step['title']}", "", step["result"], ""])
        return "\n".join(lines).strip() + "\n"
