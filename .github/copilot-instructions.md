<!-- Copilot instructions for piper-sample repository -->
# Copilot Instructions

These instructions help an AI coding agent become productive in this small speech-synthesis sample.

## Project Purpose
This repo demonstrates using `piper-tts` to synthesize WAV audio from text using an ONNX voice model. Primary code lives in `voice/` and a model file (`en_US-lessac-medium.onnx`) + metadata JSON are at the repo root.

## How to Run Locally
Use Poetry (project uses `pyproject.toml`):
- Install dependencies: `poetry install`
- Run example: `poetry run python -m voice` (executes `voice/__main__.py`)
- Dependencies: `piper-tts ^1.3.0`, `pydub ^0.25.1`, `playsound ^1.3.0`, Python `^3.10`

## Architecture & Code Patterns

### Model Loading & Configuration
- Voice models are loaded via `PiperVoice.load(path)` and return a voice object with a `.synthesize_wav(text, wav_file, syn_config)` method.
- Model paths are currently absolute (see `voice/main.py` and `voice/stream_memory.py`). Prefer relative paths: `Path(__file__).resolve().parents[1] / "en_US-lessac-medium.onnx"`.
- Model metadata (`en_US-lessac-medium.onnx.json`) contains audio sample rate (22050 Hz) and inference defaults: `noise_scale: 0.667`, `length_scale: 1`, `noise_w: 0.8`.

### Synthesis Configuration
`SynthesisConfig` parameters control output quality and timing:
- `volume` (0.5 in `main.py` = half loudness)
- `length_scale` (1.0 = normal speed)
- `noise_scale` / `noise_w_scale` (audio & speech variation; defaults from model JSON)
- `normalize_audio` (False = raw voice output; True normalizes amplitude)

Respect model JSON inference defaults unless intentionally changing voice behavior.

### Audio Output
Audio is written via Python's `wave` module to file-like objects:
```python
with wave.open("output.wav", "wb") as wav_file:
    voice.synthesize_wav(text, wav_file, syn_config=syn_config)
```
Keep this approach; only return `bytes` if explicitly needed.

### Async Streaming Patterns
- `voice/stream_memory.py` (not yet implemented fully): demonstrates async synthesis patterns with audio queuing.
- Uses `asyncio.Queue` / `deque`, `pydub.AudioSegment` for playback, UUID for temp file naming.
- Playback worker runs in background, consuming synthesized WAV files sequentially.

## Module Entry Point (`voice/__main__.py`)
Currently imports from both `main` and `stream`. Keep this file simple; main behavior lives in `voice/main.py` or `voice/stream_memory.py`.

## Testing & Validation
- No test suite or CI present. Validate changes with: `poetry run python -m voice`
- For unit tests: use model JSON metadata (sample rate, inference defaults) instead of loading ONNX binary to keep tests small.
- Integration tests should be rare because the ONNX model is large (~50 MB).

## What to Avoid
- Do not hard-delete or replace the ONNX model. Add new models under `models/` directory if needed.
- Keep `voice/__main__.py` simple; it's the module entrypoint.
- Avoid hardcoded absolute paths; use `Path(__file__).resolve().parents[1]` for repo-root-relative paths.

## Common Edits
- Add CLI flags (`--model`, `--out`, `--length-scale`, etc.) to wrap synthesis functions.
- Replace hardcoded model paths with environment variables or CLI arguments.
- Implement complete async streaming in `voice/stream_memory.py` with real-time playback.
- Add model selection logic to swap voice models dynamically.
