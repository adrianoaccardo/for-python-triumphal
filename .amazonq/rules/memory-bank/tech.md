# Technology Stack

## Programming Languages
- **Python 3.x**: Primary language for all components
- **HTML/CSS/JavaScript**: Implicit via Gradio framework

## Core Dependencies
- **gradio>=3.20**: Web UI framework for ML applications
- **torch>=1.12**: PyTorch for deep learning model execution
- **torchaudio**: Audio processing extensions for PyTorch
- **numpy**: Numerical computing and array operations
- **soundfile**: Audio file I/O operations
- **librosa**: Audio analysis and processing
- **ffmpeg-python**: Audio/video processing wrapper

## AI/ML Frameworks
- **transformers**: Hugging Face transformers for MusicGen
- **accelerate**: Model acceleration and optimization
- **Silero TTS**: Via torch.hub for text-to-speech
- **MusicGen**: Facebook's music generation model (optional)

## Development Tools
- **pytest**: Testing framework
- **pytest-cov**: Test coverage reporting
- **Docker**: Development container support via .devcontainer

## Development Commands

### Local Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### Running the Application
```bash
python app.py
# Access at http://localhost:7860
```

### Testing
```bash
pytest
pytest --cov=audio_utils  # With coverage
```

### Optional MusicGen Installation
```bash
pip install "git+https://github.com/facebookresearch/musicgen.git"
```

## Deployment Environments
- **Local Development**: CPU-based TTS, optional GPU for music generation
- **GitHub Codespaces**: CPU-only environment, TTS functional
- **Google Colab**: GPU environment recommended for MusicGen
- **Docker**: Via .devcontainer configuration

## System Requirements
- **Minimum**: Python 3.8+, 4GB RAM for TTS
- **Recommended**: Python 3.9+, 8GB+ RAM, GPU for music generation
- **Storage**: ~2GB for models (downloaded automatically)