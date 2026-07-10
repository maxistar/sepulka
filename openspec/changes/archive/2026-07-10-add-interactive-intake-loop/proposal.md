## Why

Sepulka currently produces a one-shot analysis immediately after the initial problem statement. For conflict work, especially Goldratt Conflict Cloud, this skips the intake questions that often reveal the real needs, assumptions, and constraints behind the dilemma.

## What Changes

- Add a default interactive intake loop when Sepulka runs in a TTY and the selected process defines intake questions.
- Add a `--fast` CLI option to force the existing one-shot behavior.
- Keep non-interactive runs prompt-free and fast by default.
- Extend process YAML so processes may define `intake_questions`.
- Add intake questions to `goldratt_conflict_cloud`.
- Store intake answers in working memory and include them in LLM prompts.
- Preserve `--save-note` behavior and the existing final save prompt behavior.
- Keep external actions limited to markdown notes; no shell or physical-world tools are introduced.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `mvp-usability`: Adds interactive intake behavior, `--fast`, optional YAML intake questions, and working-memory support for intake answers.

## Impact

- Affected code: `sepulka/main.py`, `sepulka/process_loader.py`, `sepulka/process_runner.py`, `sepulka/memory.py`.
- Affected process definitions: `processes/goldratt_conflict_cloud.yaml`.
- Affected docs: `README.md`.
- No new runtime dependencies are expected.
- No breaking behavior for scripts: non-interactive runs remain prompt-free.
