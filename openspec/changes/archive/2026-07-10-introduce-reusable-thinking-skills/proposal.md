## Why

Sepulka's current YAML processes are already close to reusable thinking tools, but they are still treated as local process files. Formalizing them as thinking skills will make them easier to share, version, test, document, and eventually export to other runtimes without turning Sepulka into an action agent.

## What Changes

- Introduce a reusable thinking skill format with schema version, metadata, routing hints, intake strategy, reasoning steps, expected outputs, and examples.
- Add a skill loader that loads skills from a `skills/` directory and removes the old `processes/` loading path.
- Convert `problem_framing` and `goldratt_conflict_cloud` into first-class thinking skills.
- Keep the runner focused on cognitive workflows; no OAuth, shell execution, or external-world action tools are introduced.
- Add validation and tests for skill metadata, required fields, and skill-only loading.
- Update README to explain the difference between Sepulka runtime, thinking skills, and future export possibilities.

## Capabilities

### New Capabilities

- `thinking-skills`: Defines reusable Sepulka thinking skills, their file layout, validation rules, compatibility behavior, and runtime loading expectations.

### Modified Capabilities

- None.

## Impact

- Affected code: `sepulka/process_loader.py`, `sepulka/process_runner.py` if naming assumptions need adjustment, `sepulka/router.py`, and `sepulka/main.py`.
- Affected content: remove `processes/`, add `skills/` directory, update README and tests.
- No new runtime dependencies are expected.
- Existing CLI behavior should remain compatible for users because router ids continue to resolve to built-in skills.
