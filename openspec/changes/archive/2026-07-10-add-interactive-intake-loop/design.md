## Context

Sepulka's current execution model is fast and linear: route the problem, run every YAML step through the LLM, and print a final result. That works for non-interactive use, but conflict analysis often needs intake questions before producing a useful Goldratt Conflict Cloud.

The design should preserve Sepulka's identity as a cognitive assistant, not a tool-using agent. The new loop is an interactive thinking loop only: it collects user-provided context, stores it in working memory, and feeds it into the same reasoning process.

## Goals / Non-Goals

**Goals:**

- Ask intake questions by default when Sepulka is run in an interactive terminal and the selected process defines intake questions.
- Preserve the current one-shot behavior for scripts, pipes, CI, and explicit `--fast` runs.
- Keep intake questions process-defined in YAML rather than hard-coded into the runner.
- Store intake answers in working memory and include them in LLM prompts.
- Start with Goldratt Conflict Cloud as the first process with intake questions.

**Non-Goals:**

- Add multi-turn chat memory beyond one CLI session.
- Add tool execution, shell commands, web browsing, email, or other external-world actions.
- Add a general planner/agent loop.
- Make every process interactive.
- Add a new dependency for terminal UI.

## Decisions

1. Use implicit interactive mode for TTY sessions.

   If stdin and stdout are TTYs and the user did not pass `--fast`, Sepulka may run intake questions for processes that define them. If the command is non-interactive, Sepulka must skip intake and preserve the current one-shot flow.

   Alternative considered: add `--interactive`. This is less ergonomic because terminal users generally expect dialogue from a cognitive assistant, while automation is already detectable through TTY state.

2. Add `--fast` as the explicit override.

   `--fast` forces the existing one-shot behavior even in a TTY. This gives users a direct way to request a draft analysis without intake.

   Alternative considered: `--no-interactive`. This is technically precise but less user-centered than `--fast`.

3. Add optional `intake_questions` to process YAML.

   Each intake question should have an `id` and `question`. The loader should validate these fields when `intake_questions` is present. Processes without intake questions continue to run as before.

   Alternative considered: hard-code Goldratt questions in Python. This would make process authoring less transparent and less teachable.

4. Store intake answers in working memory.

   Working memory should keep intake entries separate from LLM step results, then render both into prompt context and saved markdown. This makes the analysis traceable.

   Alternative considered: concatenate intake answers directly into the problem string. This is simpler but hides the provenance of user-provided context.

## Risks / Trade-offs

- [Risk] Interactive prompts can surprise users who expect immediate output -> Mitigation: provide `--fast` and skip intake in non-TTY contexts.
- [Risk] Intake questions can feel too long -> Mitigation: keep Goldratt intake focused on the minimum information needed before diagnosis.
- [Risk] Empty user answers may pollute memory -> Mitigation: store only non-empty answers or clearly mark skipped answers.
- [Risk] YAML validation becomes stricter -> Mitigation: make `intake_questions` optional and validate only required fields when present.
