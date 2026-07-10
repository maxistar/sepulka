## Requirements

### Requirement: Explain selected process
The system SHALL display the selected thinking process and a concise reason for the selection before showing the analysis.

#### Scenario: Conflict process selected by keywords
- **WHEN** the user submits a problem containing conflict or dilemma keywords
- **THEN** the system displays `goldratt_conflict_cloud` as the selected process and includes the matched keyword evidence in the selection reason

#### Scenario: Default process selected
- **WHEN** the user submits a problem without conflict or dilemma keywords
- **THEN** the system displays `problem_framing` as the selected process and explains that no conflict signal was detected

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

### Requirement: Validate process YAML before running
The system SHALL validate required process YAML fields before executing any process step.

#### Scenario: Missing top-level field
- **WHEN** a process YAML file is missing a required top-level field
- **THEN** loading the process fails with an error naming the missing field and process file

#### Scenario: Missing step field
- **WHEN** a process step is missing `id`, `name`, or `prompt`
- **THEN** loading the process fails with an error naming the step index, missing field, and process file

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

### Requirement: Support fast mode override
The system SHALL provide a `--fast` CLI option that forces one-shot analysis without intake prompts.

#### Scenario: Fast mode in terminal
- **WHEN** the user runs Sepulka in a TTY with `--fast`
- **THEN** the system skips all intake questions and runs the selected process directly

#### Scenario: Fast mode with save flag
- **WHEN** the user runs Sepulka with `--fast --save-note`
- **THEN** the system runs without intake prompts and saves the final analysis without asking an additional save question

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

### Requirement: Store intake answers in working memory
The system SHALL store intake answers in working memory and include them in LLM prompts and saved notes.

#### Scenario: User answers intake questions
- **WHEN** the user provides intake answers
- **THEN** the system includes those answers in the working memory context sent to each LLM process step

#### Scenario: Result saved after intake
- **WHEN** the analysis is saved after intake answers were collected
- **THEN** the saved markdown note includes the intake questions and answers

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
