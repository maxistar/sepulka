from typing import Any

from .llm import LLMClient
from .memory import WorkingMemory


SYSTEM_PROMPT = """You are Sepulka, an educational cognitive assistant.
Your job is to help the user think through complex problems using formal reasoning processes.
You do not execute commands in the physical world. You may only reason and refer to markdown notes.
Write clearly, structure the answer, and expose assumptions."""


class ProcessRunner:
    """Executes a YAML-defined thinking process step by step."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, problem: str, process: dict[str, Any], notes_context: list[dict[str, str]] | None = None) -> dict[str, Any]:
        memory = WorkingMemory(problem=problem, process_id=process["id"], notes_context=notes_context or [])

        for index, step in enumerate(process["steps"], start=1):
            result = self._run_step(problem, process, step, index, memory)
            memory.add_step_result(step["id"], step["name"], result)

        final_answer = self._finalize(problem, process, memory)
        return {"process": process, "memory": memory, "final_answer": final_answer}

    def _run_step(
        self,
        problem: str,
        process: dict[str, Any],
        step: dict[str, str],
        index: int,
        memory: WorkingMemory,
    ) -> str:
        notes_block = _format_notes(memory.notes_context)
        user_prompt = f"""Problem:
{problem}

Selected process:
{process['name']} - {process['description']}

Relevant notes:
{notes_block}

Previous working memory:
{memory.as_prompt_context()}

Current step {index}: {step['name']}
Instruction:
{step['prompt']}

Return a concise but useful structured result for this step."""

        return self.llm.chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ]
        )

    def _finalize(self, problem: str, process: dict[str, Any], memory: WorkingMemory) -> str:
        expected = "\n".join(f"- {item}" for item in process["expected_outputs"])
        user_prompt = f"""Problem:
{problem}

Process:
{process['name']}

Working memory:
{memory.as_prompt_context()}

Expected outputs:
{expected}

Create the final response. Include recommendations, uncertainties, and next thinking steps.
End by suggesting that the user can save this result as a markdown note."""

        return self.llm.chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ]
        )


def _format_notes(notes: list[dict[str, str]]) -> str:
    if not notes:
        return "No matching notes found."

    blocks = []
    for note in notes:
        content = note["content"][:1500]
        blocks.append(f"Note: {note['title']}\n{content}")
    return "\n\n".join(blocks)
