## ADDED Requirements

### Requirement: Generate contextual intake questions
The system SHALL generate concrete intake questions from the user's original problem when the selected process defines contextual intake generation and intake mode is active.

#### Scenario: Contextual Goldratt intake
- **WHEN** the user runs Sepulka interactively with a problem routed to `goldratt_conflict_cloud` and without `--fast`
- **THEN** the system performs a contextual intake generation LLM call before asking intake questions

#### Scenario: Concrete dilemma wording
- **WHEN** contextual intake generation succeeds for a problem about whether to quit or stay at a job
- **THEN** the generated intake questions refer to the concrete choices instead of generic labels like "first side" and "other side"

#### Scenario: Fast mode skips contextual generation
- **WHEN** the user runs Sepulka with `--fast`
- **THEN** the system does not perform contextual intake generation

### Requirement: Fall back to static intake questions
The system SHALL fall back to static process-defined intake questions when contextual intake generation is unavailable or invalid.

#### Scenario: Process lacks contextual intake prompt
- **WHEN** a process has `intake_questions` but no contextual intake generation prompt
- **THEN** the system asks the static intake questions

#### Scenario: Contextual intake returns invalid JSON
- **WHEN** contextual intake generation returns invalid JSON or no valid questions
- **THEN** the system asks the static intake questions

### Requirement: Timestamp analysis note filenames
The system SHALL save analysis notes with timestamped filenames to avoid overwriting earlier analysis results.

#### Scenario: Save analysis result
- **WHEN** the user saves an analysis result
- **THEN** the generated note title includes the current local timestamp and process id

#### Scenario: Repeated saves
- **WHEN** the user saves two analysis results for the same process at different times
- **THEN** the system writes two different markdown files instead of overwriting the first file

## MODIFIED Requirements

### Requirement: Preserve user language in LLM output
The system SHALL instruct the LLM to respond in the same language as the user's problem unless the user explicitly requests another language, including contextual intake generation prompts.

#### Scenario: Russian problem
- **WHEN** the user submits a Russian-language problem
- **THEN** the prompts sent to the LLM include an instruction to respond in Russian

#### Scenario: English problem
- **WHEN** the user submits an English-language problem
- **THEN** the prompts sent to the LLM include an instruction to respond in English

#### Scenario: Russian contextual intake
- **WHEN** contextual intake questions are generated for a Russian-language problem
- **THEN** the generated questions are requested in Russian

### Requirement: Support process-defined intake questions
The system SHALL allow process YAML files to define optional `intake_questions` and optional contextual intake generation prompts.

#### Scenario: Process defines intake questions
- **WHEN** a process YAML file contains `intake_questions`
- **THEN** each intake question MUST include `id` and `question`

#### Scenario: Process has no intake questions
- **WHEN** a process YAML file omits `intake_questions`
- **THEN** the process remains valid and runs without intake prompts

#### Scenario: Process defines contextual intake prompt
- **WHEN** a process YAML file contains a contextual intake generation prompt
- **THEN** the process remains valid and can use the prompt to generate intake questions in interactive mode

### Requirement: Run intake loop for interactive process sessions
The system SHALL ask contextual or static process-defined intake questions before LLM step execution when running interactively unless fast mode is enabled.

#### Scenario: Interactive Goldratt run
- **WHEN** the user runs Sepulka in a TTY with a problem routed to `goldratt_conflict_cloud` and without `--fast`
- **THEN** the system asks contextual Goldratt intake questions when generation succeeds

#### Scenario: Interactive Goldratt fallback
- **WHEN** the user runs Sepulka in a TTY with a problem routed to `goldratt_conflict_cloud`, without `--fast`, and contextual generation fails
- **THEN** the system asks the static Goldratt intake questions

#### Scenario: Non-interactive Goldratt run
- **WHEN** the user runs Sepulka in a non-TTY context with a problem routed to `goldratt_conflict_cloud`
- **THEN** the system skips intake question generation, skips intake prompts, and runs the LLM process steps directly
