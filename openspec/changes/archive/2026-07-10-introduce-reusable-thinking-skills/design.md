## Context

Sepulka currently treats thought tools as YAML processes in `processes/`. Those files already describe reusable cognitive methods, but the name and layout make them feel like internal runtime configuration rather than shareable thinking skills.

The next step is to separate the runtime from the reusable thinking artifacts. Sepulka should load first-class thinking skills from a `skills/` directory and remove the older `processes/` source to avoid duplicate definitions.

## Goals / Non-Goals

**Goals:**

- Introduce a reusable thinking skill file format.
- Keep existing process YAML fields compatible where possible.
- Add schema versioning to future-proof skill files.
- Provide a loader path for `skills/<skill-id>/skill.yaml`.
- Convert the current Goldratt and Problem Framing processes into skills.
- Remove the old `processes/` directory after built-in skills are migrated.
- Document how to author, share, and test thinking skills.

**Non-Goals:**

- Implement OAuth, accounts, marketplace publishing, or remote skill installation.
- Convert Sepulka thinking skills into Codex skills in this change.
- Add shell execution or other external-world tools.
- Add a plugin system with dynamic code execution.
- Add structured step output schemas beyond the current expected outputs.

## Decisions

1. Use directory-based skills.

   A skill should live at `skills/<skill-id>/skill.yaml`. This gives each skill room for future `README.md`, examples, tests, or fixtures without changing the core format.

   Alternative considered: keep a flat `skills/*.yaml` directory. This is simpler but makes examples and documentation harder to colocate.

2. Keep `skill.yaml` close to the existing process schema.

   The skill file should support existing process fields: `id`, `name`, `description`, `suitable_for`, `contextual_intake_prompt`, `intake_questions`, `steps`, and `expected_outputs`. New fields should include `kind`, `schema_version`, and optional `examples`.

   Alternative considered: design a completely new format. This would create migration friction without enough benefit for the MVP.

3. Use skills as the only built-in source.

   The loader should read `skills/<id>/skill.yaml` and fail clearly when a skill id is missing. Removing `processes/` avoids duplicate definitions drifting apart.

   Alternative considered: keep `processes/` as a legacy fallback. This was rejected because the project is still early and does not need backward compatibility for duplicate local files.

4. Do not execute skill code.

   Thinking skills are declarative YAML artifacts. They may contain prompts, examples, and metadata, but not Python hooks or shell commands.

   Alternative considered: allow skill-local code. This would blur the boundary between cognitive assistant and action agent.

## Risks / Trade-offs

- [Risk] Removing `processes/` can break local unpublished process files -> Mitigation: the project is pre-release, and README will document the new skill layout.
- [Risk] Naming "skill" may be confused with Codex skills -> Mitigation: call them "Sepulka thinking skills" and explicitly state they are declarative cognitive processes.
- [Risk] Directory layout adds small complexity -> Mitigation: keep the loader simple and support only `skill.yaml` for now.
- [Risk] Over-designing the schema too early -> Mitigation: keep schema v1 close to existing fields and defer structured output schemas.
