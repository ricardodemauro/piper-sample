<!-- Copilot instructions for piper-sample repository -->
# Copilot Instructions

These instructions help an AI coding agent become productive in this small speech-synthesis sample.

- **Project purpose:** This repo demonstrates using `piper-tts` to synthesize WAV audio from text using an ONNX voice model. Primary code lives in `voice/` and a model file (`en_US-lessac-medium.onnx`) + metadata JSON are at the repo root.

- **How to run locally:** use Poetry (project uses `pyproject.toml`)

  - Install dependencies: `poetry install`
  - Run the example: `poetry run python -m voice` (this executes `voice/__main__.py` which calls `voice/main.py:run`)

- **Key files to inspect or modify:**
  - `voice/main.py` — example usage showing `PiperVoice.load(...)`, `SynthesisConfig`, and `voice.synthesize_wav(...)`.
  - `voice/__main__.py` — trivial entrypoint that calls `run()`.
  - `pyproject.toml` — declares `piper-tts` and Python version (3.10).
  - `en_US-lessac-medium.onnx.json` — model metadata (sample rate, inference defaults). Use it to choose sensible default `SynthesisConfig` values.

- **Coding patterns & conventions (explicit to this repo):**
  - Voice model is loaded with an absolute or repo-root path: `PiperVoice.load("/home/radmin/projects/piper-sample/en_US-lessac-medium.onnx")`. Prefer using a path relative to the repo root (e.g. `Path(__file__).resolve().parents[1] / "en_US-lessac-medium.onnx"`) when editing.
  - `SynthesisConfig` fields frequently control loudness and timing: `volume`, `length_scale`, `noise_scale`, `noise_w_scale`, `normalize_audio`. The JSON contains `inference` defaults you should respect unless intentionally changing behavior.
  - Audio is written via Python's `wave` module to a file-like object. Keep that approach when writing tests or small scripts; return `bytes` only when explicitly needed.

- **Testing / CI / building notes:**
  - There are no tests or CI configs in the repo. Use the `poetry run python -m voice` command to validate runtime changes.
  - When adding tests, use the model JSON (`en_US-lessac-medium.onnx.json`) to assert expected sample rate or inference defaults rather than loading the ONNX binary in unit tests (to keep tests small). Use integration tests sparingly because the ONNX model is large.

- **External integrations & constraints:**
  - The primary external dependency is `piper-tts` (declared in `pyproject.toml`). Changes to voice loading or synthesis should conform to that API (see `voice/main.py`).
  - The ONNX file is a large binary in the repo root—avoid modifying it. If you need a different model, add it and update the loader path in `voice/main.py`.

- **What AI agents should avoid changing:**
  - Do not hard-delete or replace the ONNX model in the repo. Prefer adding new models under a `models/` directory.
  - Keep `voice/__main__.py` simple; it's the module entrypoint. Modify `voice/main.py` for behavior changes.

- **Common quick edits the repo expects an agent to make:**
  - Add a CLI wrapper that accepts `--model` and `--out` and calls the `run()` synthesis code.
  - Replace the hardcoded model path with a relative path or environment variable and update README or run instructions.
  - Add a small integration test that verifies `en_US-lessac-medium.onnx.json` sample rate is `22050`.

If anything in these instructions is unclear or you want the agent to follow a different convention (for example, moving models into `models/` or adding CLI flags), say so and I will revise this file.
