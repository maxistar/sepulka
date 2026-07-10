## Requirements

### Requirement: Load directory-based thinking skills
The system SHALL support reusable thinking skills stored as `skills/<skill-id>/skill.yaml`.

#### Scenario: Skill file exists
- **WHEN** `skills/goldratt_conflict_cloud/skill.yaml` exists
- **THEN** the system can load `goldratt_conflict_cloud` from that skill file

#### Scenario: Skill directory contains extra files
- **WHEN** a skill directory contains files other than `skill.yaml`
- **THEN** the loader ignores those files for execution

### Requirement: Validate thinking skill metadata
The system SHALL validate required thinking skill metadata before executing a skill.

#### Scenario: Valid skill metadata
- **WHEN** a skill file includes `kind`, `schema_version`, `id`, `name`, `description`, `suitable_for`, `steps`, and `expected_outputs`
- **THEN** the skill is valid if its process fields are also valid

#### Scenario: Missing skill metadata
- **WHEN** a skill file is missing required metadata
- **THEN** loading fails with an error naming the missing field and skill file

### Requirement: Preserve process field compatibility
The system SHALL support existing process fields inside thinking skills.

#### Scenario: Skill defines contextual intake
- **WHEN** a skill file defines `contextual_intake_prompt` and `intake_questions`
- **THEN** the existing contextual intake behavior works for that skill

#### Scenario: Skill defines process steps
- **WHEN** a skill file defines `steps`
- **THEN** each step MUST include `id`, `name`, and `prompt`

### Requirement: Remove legacy process loading
The system SHALL load built-in thinking tools only from `skills/<skill-id>/skill.yaml`.

#### Scenario: Skill id exists
- **WHEN** `skills/<id>/skill.yaml` exists
- **THEN** the system loads that thinking skill

#### Scenario: Skill id missing
- **WHEN** no `skills/<id>/skill.yaml` exists for a requested id
- **THEN** loading fails with an error naming the missing thinking skill id

### Requirement: Convert built-in processes to thinking skills
The system SHALL provide built-in thinking skills for the existing `problem_framing` and `goldratt_conflict_cloud` processes.

#### Scenario: Problem framing skill
- **WHEN** the project is installed
- **THEN** `problem_framing` is available as a thinking skill

#### Scenario: Goldratt skill
- **WHEN** the project is installed
- **THEN** `goldratt_conflict_cloud` is available as a thinking skill with contextual intake behavior preserved

### Requirement: Keep thinking skills declarative
Thinking skills SHALL NOT introduce executable hooks, shell commands, or external-world action tools.

#### Scenario: Skill loaded
- **WHEN** a thinking skill is loaded
- **THEN** the runtime treats it as declarative YAML for cognitive processing only
