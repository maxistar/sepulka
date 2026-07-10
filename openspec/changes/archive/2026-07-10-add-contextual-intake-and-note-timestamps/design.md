## Context

Sepulka now supports process-defined intake questions, but those questions are static. For Goldratt Conflict Cloud this means the user may see generic prompts like "first side" and "other side" instead of concrete questions about "leaving the job" and "staying at the current job".

This change adds a small contextual intake generation step before asking intake questions. It also improves note persistence so saved analysis files are chronological and do not overwrite prior analyses.

## Goals / Non-Goals

**Goals:**

- Generate concrete intake questions from the user's original problem when the selected process defines a contextual intake prompt.
- Keep generated questions in the user's language unless the user explicitly requested another language.
- Fall back to static intake questions when contextual generation is unavailable, fails, or returns invalid JSON.
- Preserve `--fast`: no contextual intake generation and no intake prompts.
- Save analysis notes with timestamped filenames.

**Non-Goals:**

- Add adaptive multi-turn follow-up after intake answers.
- Add a general planner or autonomous agent loop.
- Add new external actions beyond markdown note read/write.
- Add a JSON/schema validation dependency.
- Guarantee perfect language detection; prompt-level language guidance remains sufficient for the MVP.

## Decisions

1. Use process-defined `contextual_intake_prompt`.

   A process may define a prompt that asks the LLM to extract concrete options and generate intake questions. The runner/CLI will use this prompt only in interactive mode and only when not running `--fast`.

   Alternative considered: improve static YAML question wording. This is useful but cannot reliably mention concrete user options.

2. Require a small JSON response contract.

   The contextual generation call should request JSON with `questions`, where each question has `id` and `question`. Optional extracted fields such as `option_a` and `option_b` may be accepted for debugging or future use, but only questions are required for the intake loop.

   Alternative considered: parse free text. This is less reliable and harder to test.

3. Reuse the existing language hint.

   The contextual intake prompt should include the same language instruction used by the main process runner. This keeps the language behavior consistent without adding a separate language detector.

   Alternative considered: add explicit language detection. This is unnecessary for the current MVP.

4. Fall back to static intake questions.

   If contextual generation fails, returns invalid JSON, or returns no valid questions, Sepulka should ask the process's static `intake_questions` if present. This keeps interactive sessions useful even when the LLM does not follow the JSON contract.

   Alternative considered: abort with an error. That would make intake fragile.

5. Timestamp analysis note titles at save time.

   `_save_analysis()` should generate titles like `2026-07-10-143522-analysis-goldratt_conflict_cloud`. `write_note()` remains a general utility that can still write a deterministic title when explicitly requested.

   Alternative considered: change `write_note()` to always add timestamps. This would remove useful deterministic write behavior for non-analysis notes.

## Risks / Trade-offs

- [Risk] Extra LLM call increases latency and cost -> Mitigation: only run it in interactive intake mode, never in `--fast` or non-TTY mode.
- [Risk] LLM returns malformed JSON -> Mitigation: fall back to static intake questions.
- [Risk] Generated questions may still be awkward -> Mitigation: keep static questions as a safety net and use focused Goldratt instructions.
- [Risk] Timestamp filenames are less predictable in tests -> Mitigation: isolate timestamp generation in a helper that can accept an injected datetime.
