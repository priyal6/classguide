# classguide

Practice code from working through Python design and reliability patterns. Each folder covers one topic and can be read on its own.

## Contents

### `retry/` — retrying failed operations

Builds up a retry strategy step by step, using a Chuck Norris joke API as the flaky operation:

| File | What it shows |
| --- | --- |
| `1naive.py` | A plain API call with no error handling |
| `2retry_function.py` | A generic `retry()` helper with a fixed delay |
| `3exponential_backoff.py` | Retry with exponential backoff between attempts |
| `retry_decorator.py` | The same logic packaged as a reusable `@retry_decorator` |
| `llm_api.py` | Applying the retry decorator to an OpenAI API call |

### `god/` — breaking up a "god class"

| File | What it shows |
| --- | --- |
| `before.py` | `ChurnExperiment`, one class that validates config, loads data, trains and saves a model |
| `after.py` | The same experiment split into focused pieces, starting with a validated `TrainingConfig` dataclass |
| `con.py` | Passing a config object and an `httpx.Client` into an API client (dependency injection) |
| `con2.py` | Injecting config and a logger into a service class |
| `con_error.py` | Adding retries and error handling to the injected API client |

### `email_tools/` and `before.py`

A small `EmailService` class and a `before.py` script that uses it alongside some dataclasses (`Stats`, `Address`, ...). The email values in `before.py` are placeholders.

## Setup

The project uses [uv](https://docs.astral.sh/uv/) as a workspace (`retry` and `god` are members) and needs Python 3.12+.

```bash
uv sync
uv run retry/1naive.py
```

`god/` also needs `pandas`, `scikit-learn` and `joblib`, which aren't listed in its `pyproject.toml` yet.

`retry/llm_api.py` reads an OpenAI key from a `.env` file:

```
OPENAI_API_KEY=your-key-here
```

`.env` is git-ignored, so the key stays local.
