# Sepulka

Sepulka is a minimal educational cognitive assistant / intelligence amplifier.
It helps a person reason through complex problems by applying explicit thinking
processes.

Sepulka is not a tool-using agent for acting in the physical world. It does not
run shell commands, operate devices, send messages, or make external changes.
In this MVP its only external actions are reading and writing local markdown
notes.

## What It Does

- Accepts a problem from the CLI.
- Routes the problem to a thinking process.
- Loads the selected process from YAML.
- Generates contextual intake questions first when used interactively and supported by the selected process.
- Runs each process step through an OpenAI-compatible chat completions API.
- Keeps intake answers and intermediate results in working memory.
- Prints the selected process, intermediate analysis, and final recommendations.
- Can save the result as a markdown note.

## Install

With `uv`:

```bash
uv sync
cp .env.example .env
```

Or with standard `venv` and `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```env
LLM_BASE_URL=https://api.openai.com
LLM_API_KEY=your-api-key
LLM_MODEL=gpt-4.1-mini
```

Any OpenAI-compatible provider should work if it supports:

```text
POST /v1/chat/completions
```

## Run

In a terminal, Sepulka can generate contextual intake questions before analysis when the selected process supports them:

```bash
uv run python -m sepulka "Я не знаю, уходить ли мне с текущей работы или остаться ради стабильности"
```

You can also use the installed script:

```bash
uv run sepulka "Я не знаю, уходить ли мне с текущей работы или остаться ради стабильности"
```

For a one-shot draft without intake questions, use `--fast`:

```bash
uv run sepulka --fast "Я не знаю, уходить ли мне с текущей работы или остаться ради стабильности"
```

Non-interactive runs, such as scripts and pipes, automatically use fast mode and never wait for prompts. Contextual intake generation is also skipped in fast mode.

Expected output includes:

- selected process;
- selection reason, including matched conflict keywords when relevant;
- contextual intake questions when running interactively and supported by the selected process;
- intermediate analysis structure;
- final recommendations;
- an interactive offer to save the result when running in a terminal.

To save the final result automatically, use `--save-note`. Saved analysis notes include a timestamp in the filename so repeated saves do not overwrite earlier results:

```bash
uv run python -m sepulka "Я не знаю, уходить ли мне с текущей работы или остаться ради стабильности" --save-note
```

## Thinking Processes

Processes live in `processes/` as YAML files.

Current processes:

- `problem_framing`
- `goldratt_conflict_cloud`

Each process contains:

- `id`
- `name`
- `description`
- `suitable_for`
- optional `contextual_intake_prompt`
- optional `intake_questions` fallback questions
- `steps`
- `expected_outputs`

## Add A New Process

Create a new file in `processes/`, for example:

```yaml
id: decision_matrix
name: Decision Matrix
description: Compares options against weighted criteria.
suitable_for:
  - decisions with multiple options
contextual_intake_prompt: >
  Generate concrete intake questions from the user problem.
intake_questions:
  - id: context
    question: What context should Sepulka know before analysis?
steps:
  - id: options
    name: Identify Options
    prompt: List the realistic options.
  - id: criteria
    name: Define Criteria
    prompt: Define criteria for evaluating the options.
expected_outputs:
  - options
  - criteria
  - recommendation
```

Then update `sepulka/router.py` so Sepulka can choose the new process and explain that choice in the CLI output.

## Notes

Markdown notes live in `notes/`.

The available note functions are:

- `read_notes(query)`: keyword search over markdown files.
- `write_note(title, content)`: saves markdown content into `notes/`.

This is intentionally simple. There is no vector search in the MVP.
