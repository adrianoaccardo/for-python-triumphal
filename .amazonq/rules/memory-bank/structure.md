# Project Structure

## Directory Organization
```
/workspaces/for-python-triumphal/
├── .amazonq/rules/memory-bank/     # AI assistant memory bank
├── .devcontainer/                  # Development container configuration
├── .github/                        # GitHub-specific files and instructions
├── Notes/                          # Learning notes and documentation
├── tests/                          # Test suite
├── app.py                          # Main Gradio web application
├── audio_utils.py                  # Audio processing utilities
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## Core Components

### Main Application (`app.py`)
- Gradio web interface with two main tabs: TTS and Text→Music
- Lazy-loading of AI models for memory efficiency
- Error handling and status reporting
- Integration point for both Silero TTS and MusicGen

### Audio Utilities (`audio_utils.py`)
- Audio file I/O operations
- Sample rate constants and audio format handling
- Utility functions for saving numpy arrays as audio files

### Configuration Files
- `requirements.txt`: Python package dependencies with optional MusicGen
- `.devcontainer/`: Docker-based development environment setup
- `tests/`: Unit tests for audio utilities

## Architectural Patterns

### Lazy Loading Pattern
Models are loaded only when first used to minimize startup time and memory usage:
- Silero TTS model loaded on first speech generation request
- MusicGen model loaded on first music generation request

### Separation of Concerns
- UI logic isolated in `app.py`
- Audio processing utilities in separate module
- Model management encapsulated with global state tracking

### Error Handling Strategy
- Graceful degradation when dependencies are missing
- Detailed error reporting in UI status fields
- Exception handling with full traceback for debugging

## Dependencies Architecture
- **Core**: gradio, torch, numpy for basic functionality
- **Audio**: torchaudio, soundfile, librosa for audio processing
- **Optional**: MusicGen via git installation for music generation
- **Testing**: pytest and pytest-cov for test coverage