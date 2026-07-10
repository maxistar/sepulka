## ADDED Requirements

### Requirement: Support fast mode override
The system SHALL provide a `--fast` CLI option that forces one-shot analysis without intake prompts.

#### Scenario: Fast mode in terminal
- **WHEN** the user runs Sepulka in a TTY with `--fast`
- **THEN** the system skips all intake questions and runs the selected process directly

#### Scenario: Fast mode with save flag
- **WHEN** the user runs Sepulka with `--fast --save-note`
- **THEN** the system runs without intake prompts and saves the final analysis without asking an additional save question

### Requirement: Support process-defined intake questions
The system SHALL allow process YAML files to define optional `intake_questions`.

#### Scenario: Process defines intake questions
- **WHEN** a process YAML file contains `intake_questions`
- **THEN** each intake question MUST include `id` and `question`

#### Scenario: Process has no intake questions
- **WHEN** a process YAML file omits `intake_questions`
- **THEN** the process remains valid and runs without intake prompts

### Requirement: Run intake loop for interactive process sessions
The system SHALL ask process-defined intake questions before LLM step execution when running interactively unless fast mode is enabled.

#### Scenario: Interactive Goldratt run
- **WHEN** the user runs Sepulka in a TTY with a problem routed to `goldratt_conflict_cloud` and without `--fast`
- **THEN** the system asks the Goldratt intake questions before running the LLM process steps

#### Scenario: Non-interactive Goldratt run
- **WHEN** the user runs Sepulka in a non-TTY context with a problem routed to `goldratt_conflict_cloud`
- **THEN** the system skips intake questions and runs the LLM process steps directly

### Requirement: Store intake answers in working memory
The system SHALL store intake answers in working memory and include them in LLM prompts and saved notes.

#### Scenario: User answers intake questions
- **WHEN** the user provides intake answers
- **THEN** the system includes those answers in the working memory context sent to each LLM process step

#### Scenario: Result saved after intake
- **WHEN** the analysis is saved after intake answers were collected
- **THEN** the saved markdown note includes the intake questions and answers

## MODIFIED Requirements

### Requirement: Offer note saving interactively
The system SHALL make result saving discoverable while preserving non-interactive CLI behavior and fast mode behavior.

#### Scenario: Save flag provided
- **WHEN** the user runs the CLI with `--save-note`
- **THEN** the system saves the final analysis to `notes/` without asking an additional question

#### Scenario: Interactive run without save flag
- **WHEN** the user runs the CLI in an interactive terminal without `--save-note`
- **THEN** the system asks whether to save the result as a markdown note after any applicable intake loop and final analysis are complete

#### Scenario: Non-interactive run without save flag
- **WHEN** the user runs the CLI in a non-interactive context without `--save-note`
- **THEN** the system does not prompt and instead prints how to rerun with `--save-note`

#### Scenario: Fast run without save flag
- **WHEN** the user runs the CLI with `--fast` in an interactive terminal without `--save-note`
- **THEN** the system skips intake prompts but may still ask whether to save the final result as a markdown note

### Requirement: Limit external actions to markdown notes
The system SHALL NOT introduce shell execution or external-world action tools as part of the interactive intake improvements.

#### Scenario: Interactive intake completed
- **WHEN** the change is implemented
- **THEN** the only external actions available in the MVP remain reading markdown notes and writing markdown notes
