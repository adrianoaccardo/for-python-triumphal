# Product Overview

## Project Purpose
A minimal Suno-like MVP that provides AI-powered audio generation capabilities through a web interface. This project serves as both a learning exercise and a functional prototype for text-to-speech and text-to-music generation.

## Key Features
- **CPU-based Text-to-Speech**: Real TTS using Silero models via torch.hub, optimized for CPU execution in Codespaces/local environments
- **Text-to-Music Generation**: MusicGen integration ready for GPU environments or Colab deployment
- **Web Interface**: Gradio-based UI for easy local testing and deployment
- **Cross-platform Support**: Works on Linux, Mac, and Windows with proper environment setup

## Target Users
- Developers learning AI/ML audio processing
- Students exploring text-to-speech and music generation
- Researchers prototyping audio generation workflows
- Anyone wanting to experiment with open-source audio AI models

## Use Cases
- Generate speech from text for accessibility applications
- Create background music from text descriptions
- Prototype audio-based applications
- Educational exploration of AI audio models
- Testing audio generation workflows before scaling to production

## Value Proposition
- No proprietary weights required - uses open-source models
- CPU-friendly TTS for immediate testing
- GPU-ready music generation for when resources are available
- Simple deployment via Gradio web interface
- Educational codebase with clear separation of concerns