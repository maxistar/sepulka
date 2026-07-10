## Why

Sepulka's MVP already demonstrates the core cognitive-assistant loop, but the user experience is still opaque in a few important places. Improving process-selection transparency, language handling, process validation, and note-saving flow will make the tool easier to learn from and safer to extend.

## What Changes

- Show why a thinking process was selected, including conflict keywords or fallback reasoning.
- Make LLM responses explicitly follow the user's language.
- Validate process YAML step structure before running a process.
- Improve the result-saving experience by offering an interactive save prompt when appropriate while preserving `--save-note`.
- Keep external actions constrained to markdown note read/write; no shell or physical-world tools are introduced.

## Capabilities

### New Capabilities

- `mvp-usability`: Covers CLI usability, routing transparency, language behavior, process validation, and note-save workflow for the Sepulka MVP.

### Modified Capabilities

- None.

## Impact

- Affected code: `sepulka/main.py`, `sepulka/router.py`, `sepulka/process_loader.py`, `sepulka/process_runner.py`, `sepulka/notes.py`.
- Affected docs: `README.md`.
- No new runtime service dependencies are expected.
- No breaking CLI changes are expected; existing `python -m sepulka` and `uv run sepulka` flows should continue to work.
