## 1. Process Schema And Goldratt Prompt

- [x] 1.1 Add optional contextual intake prompt validation to process loading.
- [x] 1.2 Add contextual intake prompt to `goldratt_conflict_cloud.yaml`.
- [x] 1.3 Preserve static `intake_questions` as fallback questions.

## 2. Contextual Intake Generation

- [x] 2.1 Add an LLM-backed contextual intake question generator.
- [x] 2.2 Require generated intake questions to use the existing language hint.
- [x] 2.3 Parse the generator response as JSON and extract valid `id` / `question` items.
- [x] 2.4 Fall back to static intake questions when generation fails or returns no valid questions.
- [x] 2.5 Ensure `--fast` and non-TTY runs skip contextual generation.

## 3. Timestamped Analysis Notes

- [x] 3.1 Add helper for timestamped analysis note titles.
- [x] 3.2 Update analysis saving to use timestamped titles.
- [x] 3.3 Keep `write_note(title, content)` deterministic for non-analysis note writes.

## 4. Tests

- [x] 4.1 Add fake LLM tests for successful contextual intake generation.
- [x] 4.2 Add tests for invalid JSON fallback to static intake questions.
- [x] 4.3 Add tests that contextual intake prompts include the user's language instruction.
- [x] 4.4 Add tests for timestamped analysis note title generation.
- [x] 4.5 Add tests that `--fast` skips contextual intake generation.

## 5. Documentation And Verification

- [x] 5.1 Update README with contextual intake behavior and timestamped note filenames.
- [x] 5.2 Run unit tests and compile checks.
- [x] 5.3 Verify no shell execution or external action tools are introduced.
