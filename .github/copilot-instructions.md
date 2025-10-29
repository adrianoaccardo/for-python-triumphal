# AI Agent Instructions for for-python-triumphal

## Project Overview
This repository serves two distinct purposes:

1. **Suno-like MVP Application** (`app.py`)
   - Text-to-Speech (TTS) using Silero (CPU-compatible)
   - Text-to-Music generation using MusicGen (GPU required)
   - Gradio web UI for interactive usage

2. **Learning Journey Documentation**
   - Structured progression through computer science fundamentals
   - Focus on Python, data structures, algorithms, and ML
   - Organized documentation of learning process

## Key Components and Patterns

### Text-to-Speech (TTS) Component
- Uses Silero models via `torch.hub`
- CPU-friendly implementation for accessibility
- Key functions:
  - `ensure_silero_loaded()` - Model initialization with lazy loading
  - `silero_tts()` - Core TTS generation function
  - Sample rate: 48000Hz

### Music Generation Component
- Optional MusicGen integration
- GPU required for practical use
- Key configuration options in `musicgen_generate()`:
  - `model_size`: "small", "medium", "large"
  - `device`: "cuda", "cpu"
  - Default sample rate: 32000Hz

### Web Interface
- Built with Gradio (`gr.Blocks`)
- Two main tabs: TTS and Text→Music
- Server configuration: `server_name="0.0.0.0", share=False`

## Development Workflows

### Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Running the Application
```bash
python app.py
# Access at http://localhost:7860
```

### Dependencies
- Core requirements in `requirements.txt`
- MusicGen (optional): Install from GitHub if GPU available
- All models are downloaded on-demand from respective hubs

## Project Structure
- `/courses` - Course materials and exercises
- `/projects` - Self-contained experiments
- `/snippets` - Reusable code patterns
- `/docs` - Technical documentation
- `/Notes` - Learning reflections and notes

## Best Practices
1. When modifying audio processing code:
   - Preserve the sample rate constants (48000Hz for TTS, 32000Hz for music)
   - Handle numpy array type conversion explicitly
   - Use tempfile for audio output storage

2. Error handling:
   - Follow existing pattern of try/except with clear error messages
   - Check for optional dependencies (e.g., `_TORCH_AVAILABLE`)
   - Provide user-friendly feedback in UI components

3. Model management:
   - Use lazy loading pattern for all ML models
   - Check for required hardware (CPU/GPU) before operations
   - Clean up temporary files after use

## License
MIT License - modifications and improvements welcome.