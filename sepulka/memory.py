from dataclasses import dataclass, field


@dataclass
class WorkingMemory:
    """Small in-memory store for one reasoning session.

    The runner writes user intake and every process step here. In a larger
    system this could be persisted, summarized, or linked to user notes, but the
    MVP keeps it simple.
    """

    problem: str
    process_id: str
    notes_context: list[dict[str, str]] = field(default_factory=list)
    intake_answers: list[dict[str, str]] = field(default_factory=list)
    steps: list[dict[str, str]] = field(default_factory=list)

    def add_intake_answer(self, question_id: str, question: str, answer: str) -> None:
        self.intake_answers.append({"id": question_id, "question": question, "answer": answer})

    def add_step_result(self, step_id: str, title: str, result: str) -> None:
        self.steps.append({"id": step_id, "title": title, "result": result})

    def intake_as_prompt_context(self) -> str:
        if not self.intake_answers:
            return "No intake answers collected."

        blocks = []
        for item in self.intake_answers:
            blocks.append(f"Question {item['id']}: {item['question']}\nAnswer: {item['answer']}")
        return "\n\n".join(blocks)

    def as_prompt_context(self) -> str:
        blocks = ["User intake:", self.intake_as_prompt_context()]

        if self.steps:
            blocks.append("Process steps:")
            for step in self.steps:
                blocks.append(f"Step {step['id']} - {step['title']}:\n{step['result']}")
        else:
            blocks.append("Process steps:\nNo previous steps yet.")

        return "\n\n".join(blocks)

    def as_markdown(self) -> str:
        lines = ["# Sepulka Analysis", "", f"Problem: {self.problem}", "", f"Process: {self.process_id}", ""]

        if self.intake_answers:
            lines.extend(["## Intake", ""])
            for item in self.intake_answers:
                lines.extend([f"### {item['question']}", "", item["answer"], ""])

        for step in self.steps:
            lines.extend([f"## {step['title']}", "", step["result"], ""])
        return "\n".join(lines).strip() + "\n"
