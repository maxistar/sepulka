## ADDED Requirements

### Requirement: Explain selected process
The system SHALL display the selected thinking process and a concise reason for the selection before showing the analysis.

#### Scenario: Conflict process selected by keywords
- **WHEN** the user submits a problem containing conflict or dilemma keywords
- **THEN** the system displays `goldratt_conflict_cloud` as the selected process and includes the matched keyword evidence in the selection reason

#### Scenario: Default process selected
- **WHEN** the user submits a problem without conflict or dilemma keywords
- **THEN** the system displays `problem_framing` as the selected process and explains that no conflict signal was detected

### Requirement: Preserve user language in LLM output
The system SHALL instruct the LLM to respond in the same language as the user's problem unless the user explicitly requests another language.

#### Scenario: Russian problem
- **WHEN** the user submits a Russian-language problem
- **THEN** the prompts sent to the LLM include an instruction to respond in Russian

#### Scenario: English problem
- **WHEN** the user submits an English-language problem
- **THEN** the prompts sent to the LLM include an instruction to respond in English

### Requirement: Validate process YAML before running
The system SHALL validate required process YAML fields before executing any process step.

#### Scenario: Missing top-level field
- **WHEN** a process YAML file is missing a required top-level field
- **THEN** loading the process fails with an error naming the missing field and process file

#### Scenario: Missing step field
- **WHEN** a process step is missing `id`, `name`, or `prompt`
- **THEN** loading the process fails with an error naming the step index, missing field, and process file

### Requirement: Offer note saving interactively
The system SHALL make result saving discoverable while preserving non-interactive CLI behavior.

#### Scenario: Save flag provided
- **WHEN** the user runs the CLI with `--save-note`
- **THEN** the system saves the final analysis to `notes/` without asking an additional question

#### Scenario: Interactive run without save flag
- **WHEN** the user runs the CLI in an interactive terminal without `--save-note`
- **THEN** the system asks whether to save the result as a markdown note

#### Scenario: Non-interactive run without save flag
- **WHEN** the user runs the CLI in a non-interactive context without `--save-note`
- **THEN** the system does not prompt and instead prints how to rerun with `--save-note`

### Requirement: Limit external actions to markdown notes
The system SHALL NOT introduce shell execution or external-world action tools as part of the usability improvements.

#### Scenario: Usability improvements completed
- **WHEN** the change is implemented
- **THEN** the only external actions available in the MVP remain reading markdown notes and writing markdown notes
