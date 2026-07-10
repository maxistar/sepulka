## Why

The current intake loop asks generic process questions, which can feel detached from the user's concrete dilemma. Sepulka should generate contextual intake questions in the user's language and avoid overwriting prior saved analyses.

## What Changes

- Add contextual intake generation for processes that define a contextual intake prompt.
- Generate intake questions from the user's original problem, using concrete option names when possible.
- Require contextual intake questions to use the same language as the original problem unless the user explicitly requested another language.
- Fall back to static `intake_questions` when contextual generation is unavailable or cannot be parsed.
- Update Goldratt Conflict Cloud to use contextual intake generation.
- Save analysis notes with timestamped filenames so repeated saves do not overwrite previous results.
- Keep `--fast` behavior unchanged: no intake generation or intake prompts.
- Keep external actions limited to markdown notes; no shell or physical-world tools are introduced.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `mvp-usability`: Adds contextual intake generation, language requirements for generated intake questions, and timestamped analysis note filenames.

## Impact

- Affected code: `sepulka/main.py`, `sepulka/process_loader.py`, `sepulka/process_runner.py`, `sepulka/notes.py` if needed.
- Affected process definitions: `processes/goldratt_conflict_cloud.yaml`.
- Affected docs: `README.md`.
- No new runtime dependencies are expected.
- One additional LLM call may occur before intake prompts in interactive mode for processes with contextual intake enabled.
