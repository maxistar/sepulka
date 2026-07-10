## 1. CLI Mode Selection

- [x] 1.1 Add `--fast` CLI option.
- [x] 1.2 Determine intake mode from `--fast` and TTY state.
- [x] 1.3 Preserve non-interactive no-prompt behavior.

## 2. Process YAML Support

- [x] 2.1 Add optional `intake_questions` support to process validation.
- [x] 2.2 Validate each intake question requires `id` and `question`.
- [x] 2.3 Add focused intake questions to `goldratt_conflict_cloud.yaml`.

## 3. Working Memory And Runner

- [x] 3.1 Add intake question/answer storage to working memory.
- [x] 3.2 Include intake answers in LLM prompt context.
- [x] 3.3 Include intake answers in saved markdown notes.

## 4. Interactive Intake Flow

- [x] 4.1 Ask process-defined intake questions before LLM steps in interactive mode.
- [x] 4.2 Skip intake questions in `--fast` mode.
- [x] 4.3 Keep final save prompt behavior compatible with intake and fast mode.

## 5. Verification And Docs

- [x] 5.1 Add tests for `--fast`, non-interactive mode, and intake mode decision.
- [x] 5.2 Add tests for intake question validation and prompt inclusion.
- [x] 5.3 Update README with default interactive behavior and `--fast` examples.
- [x] 5.4 Verify no shell execution or external action tools are introduced.
