## Context

Sepulka is a minimal Python CLI cognitive assistant. The current MVP already has a clean core loop: accept a problem, route it to a YAML-defined thinking process, run each step through an OpenAI-compatible LLM API, keep working memory, and optionally save the result as a markdown note.

The next usability improvements should preserve that architecture. Sepulka should remain a cognitive process runner, not a general tool-using agent. External actions remain limited to local markdown notes.

## Goals / Non-Goals

**Goals:**

- Make process routing explainable at the CLI level.
- Make output language behavior explicit and predictable.
- Fail early with useful errors when process YAML is malformed.
- Make saving analysis results more discoverable without removing `--save-note`.
- Keep the implementation small and readable for educational use.

**Non-Goals:**

- Add shell execution, browser automation, email, filesystem tools beyond markdown notes, or other agentic actions.
- Add LangChain or another orchestration framework.
- Add vector search, a database, or persistent multi-session memory.
- Replace the current YAML process format.

## Decisions

1. Return routing metadata from the router.

   `choose_process()` can evolve from returning only a process id to returning a small structured result containing `process_id`, `reason`, and matched keywords. This keeps routing transparent without introducing an LLM-based router.

   Alternative considered: ask the LLM to choose the process. This was rejected for the MVP because deterministic keyword routing is easier to inspect, test, and teach.

2. Add process schema validation in `process_loader.py`.

   Validation should check top-level fields and each step's required fields: `id`, `name`, and `prompt`. Errors should name the process file and the missing field. This keeps authoring new YAML processes safer while avoiding a heavy schema dependency.

   Alternative considered: add JSON Schema. This may be useful later, but hand-written validation is enough for the current two-process MVP.

3. Put language guidance in the system prompt and step prompts.

   The runner should instruct the LLM to respond in the same language as the user's problem unless the user explicitly asks otherwise. This is a prompt-level behavior, not a language-detection subsystem.

   Alternative considered: implement explicit language detection. This adds complexity and is unnecessary for the current CLI.

4. Support an interactive save prompt only when stdout is attached to a terminal.

   `--save-note` should continue to save without prompting. Without `--save-note`, the CLI may ask whether to save the result when running interactively. In non-interactive contexts, it should print the existing instruction to rerun with `--save-note`.

   Alternative considered: always prompt. This would make scripts and tests awkward.

## Risks / Trade-offs

- Keyword routing can misclassify ambiguous problems -> Mitigation: print routing reasoning so the user can see why the process was chosen.
- Interactive prompts can break automation -> Mitigation: only prompt on TTY and preserve `--save-note`.
- Prompt-only language control may not be perfect -> Mitigation: keep the instruction explicit and include it in both system-level and task-level context.
- Hand-written YAML validation may miss deeper semantic issues -> Mitigation: validate the fields the runner actually requires and keep errors actionable.
