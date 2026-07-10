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
- Runs each process step through an OpenAI-compatible chat completions API.
- Keeps intermediate results in working memory.
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

```bash
uv run python -m sepulka "Я не знаю, уходить ли мне с текущей работы или остаться ради стабильности"
```

You can also use the installed script:

```bash
uv run sepulka "Я не знаю, уходить ли мне с текущей работы или остаться ради стабильности"
```

Expected output includes:

- selected process;
- intermediate analysis structure;
- final recommendations;
- a suggestion to save the result to a note.

To save the final result:

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

Then update `sepulka/router.py` so Sepulka can choose the new process.

## Notes

Markdown notes live in `notes/`.

The available note functions are:

- `read_notes(query)`: keyword search over markdown files.
- `write_note(title, content)`: saves markdown content into `notes/`.

This is intentionally simple. There is no vector search in the MVP.
