## 1. Skill Format And Loader

- [x] 1.1 Define skill directory constants and `skills/<id>/skill.yaml` lookup.
- [x] 1.2 Extend loader to load only skill files and fail clearly for missing skill ids.
- [x] 1.3 Validate required skill metadata: `kind`, `schema_version`, `id`, `name`, `description`, `suitable_for`, `steps`, `expected_outputs`.
- [x] 1.4 Preserve existing validation for steps, intake questions, and contextual intake prompts.

## 2. Built-In Skill Migration

- [x] 2.1 Create `skills/problem_framing/skill.yaml` from the current process.
- [x] 2.2 Create `skills/goldratt_conflict_cloud/skill.yaml` from the current process.
- [x] 2.3 Remove the legacy `processes/` directory after built-in skills are migrated.
- [x] 2.4 Ensure router ids continue to resolve to the same built-in tools.

## 3. Tests

- [x] 3.1 Add loader test proving skill files load from `skills/<id>/skill.yaml`.
- [x] 3.2 Add loader test proving missing skill ids fail clearly.
- [x] 3.3 Add validation test for missing required skill metadata.
- [x] 3.4 Add validation test that contextual intake behavior remains available from the Goldratt skill.
- [x] 3.5 Add safety test or search verification that skills remain declarative and no executable hooks are introduced.

## 4. Documentation

- [x] 4.1 Update README to describe Sepulka thinking skills and their directory layout.
- [x] 4.2 Document how to add a new reusable thinking skill.
- [x] 4.3 Document that Sepulka thinking skills are declarative cognitive processes, not Codex skills or action tools.

## 5. Verification

- [x] 5.1 Run unit tests and compile checks.
- [x] 5.2 Verify CLI behavior still works with existing process ids.
- [x] 5.3 Verify no shell execution or external action tools are introduced.
