## 1. Routing Transparency

- [x] 1.1 Change router output to include selected process id, reason text, and matched keywords.
- [x] 1.2 Update CLI output to display the routing reason before intermediate analysis.
- [x] 1.3 Add smoke coverage for conflict-keyword routing and default routing.

## 2. Process Validation

- [x] 2.1 Add validation for required top-level process YAML fields.
- [x] 2.2 Add validation for each process step requiring `id`, `name`, and `prompt`.
- [x] 2.3 Ensure validation errors include the process file path and missing field context.

## 3. LLM Prompt Language Behavior

- [x] 3.1 Update runner prompts to instruct the LLM to answer in the user's language unless explicitly requested otherwise.
- [x] 3.2 Add a lightweight language hint helper for Russian and English inputs.
- [x] 3.3 Add prompt construction coverage using a fake LLM client.

## 4. Note Save Workflow

- [x] 4.1 Preserve existing `--save-note` behavior as a non-interactive save path.
- [x] 4.2 Add an interactive save prompt when running in a TTY without `--save-note`.
- [x] 4.3 Keep non-interactive runs prompt-free and print the rerun-with-`--save-note` instruction.

## 5. Documentation And Verification

- [x] 5.1 Update README examples to mention routing explanations and interactive save behavior.
- [x] 5.2 Verify `uv run python -m sepulka ...` still starts and reports missing LLM settings clearly when `.env` is absent.
- [x] 5.3 Verify the MVP still has no shell execution or external action tools beyond markdown notes.
