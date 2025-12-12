# Piper TTS Sample

A Python project demonstrating text-to-speech synthesis using [Piper TTS](https://github.com/rhasspy/piper) with an ONNX voice model. This sample includes multiple executor modes for different synthesis and playback strategies.

## Features

- **Text-to-Speech Synthesis**: Convert text to natural-sounding speech using pre-trained voice models
- **Multiple Execution Modes**: Choose between different synthesis and playback strategies
- **Relative Path Configuration**: Model paths automatically resolve relative to the project root
- **Audio Control**: Customize volume, speed, and voice variation parameters

## Installation

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

### Setup

1. Install project dependencies using Poetry:

```bash
poetry install
```

This will install all required packages:
- `piper-tts` (^1.3.0) - Text-to-speech synthesis engine
- `pydub` (^0.25.1) - Audio processing library
- `playsound` (^1.3.0) - Audio playback utility

## Usage

Run the project with Poetry:

```bash
# Default executor (main)
poetry run python -m voice

# Use stream executor
poetry run python -m voice --executor stream

# Use stream_memory executor
poetry run python -m voice --executor stream_memory

# View available options
poetry run python -m voice --help
```

## Executors

### `main` (Default)
Synchronous text-to-speech synthesis that converts sample text to a WAV file (`test.wav`) with configurable audio parameters (volume, speed, variation).

### `stream`
Asynchronous streaming synthesis with file-based playback. Synthesizes multiple text samples, queues them as temporary WAV files, and plays them sequentially in the background.

### `stream_memory`
Asynchronous streaming synthesis with in-memory playback. Synthesizes text samples and stores audio in memory as byte buffers, then plays them sequentially without creating temporary files.

## Project Structure

```
piper-sample/
├── voice/
│   ├── __main__.py        # Entry point with executor selection
│   ├── main.py            # Synchronous TTS synthesis
│   ├── stream.py          # Async streaming with file-based playback
│   └── stream_memory.py   # Async streaming with in-memory playback
├── en_US-lessac-medium.onnx      # Pre-trained voice model
├── en_US-lessac-medium.onnx.json # Model metadata and configuration
├── pyproject.toml         # Project dependencies and metadata
└── README.md              # This file
```

## Model Information

The project uses the `en_US-lessac-medium.onnx` voice model with the following specifications:

- **Sample Rate**: 22050 Hz
- **Default Inference Parameters**:
  - `noise_scale`: 0.667 (audio variation)
  - `length_scale`: 1.0 (speech speed)
  - `noise_w`: 0.8 (speech variation)

## Notes

- Output audio files are saved as WAV format at the project root
- The `stream` executor creates temporary audio files that are cleaned up after playback
- The `stream_memory` executor requires sufficient RAM for in-memory audio buffers
- Relative model paths ensure the project works from any directory

## License

This project is a sample implementation for educational purposes.
