# Development Guidelines

## Code Quality Standards

### Import Organization (3/3 files)
- Standard library imports first
- Third-party imports second  
- Local module imports last
- Use `from typing import` for type hints
- Group imports logically with blank lines between groups

```python
from typing import Any
import traceback

import numpy as np
import gradio as gr
from audio_utils import save_wave_np, TTS_SAMPLE_RATE
```

### Line Length and Formatting (3/3 files)
- Keep lines under 79 characters for flake8 compliance
- Break long function calls across multiple lines with proper indentation
- Use trailing commas in multi-line function calls

```python
res = torch.hub.load(
    repo_or_dir="snakers4/silero-models",
    model="silero_tts",
    language=language,
    speaker=speaker,
)
```

### Type Annotations (3/3 files)
- Use type hints for all function parameters and return values
- Use `Any` from typing for complex ML model objects
- Specify numpy array types as `np.ndarray`
- Use Union types when appropriate

```python
def save_wave_np(wave: np.ndarray, sr: int = TTS_SAMPLE_RATE) -> str:
def ensure_silero_loaded(language: str = "en", speaker: str = "v3_en") -> None:
```

## Documentation Standards

### Docstring Format (3/3 files)
- Use triple quotes for all docstrings
- Include brief description of function purpose
- Document exceptions that may be raised
- Keep module docstrings descriptive but concise

```python
def ensure_silero_loaded(language: str = "en", speaker: str = "v3_en") -> None:
    """Lazy-load Silero TTS model via torch.hub.

    Raises RuntimeError when torch isn't available.
    """
```

### Inline Comments (3/3 files)
- Explain complex logic and data transformations
- Document shape changes in audio processing
- Clarify flake8 compliance decisions
- Use comments to explain business logic

```python
# The output is a batch, so we take the first element
audio_numpy = audio_numpy[0]
# Wrap arguments to keep line lengths under 79 chars for flake8
```

## Architectural Patterns

### Lazy Loading Pattern (2/3 files)
- Use global variables with type annotations for model state
- Implement `ensure_*_loaded()` functions for each model
- Check loading state before proceeding with operations
- Handle missing dependencies gracefully

```python
_silero_loaded: bool = False
_silero_model: Any = None

def ensure_silero_loaded(language: str = "en", speaker: str = "v3_en") -> None:
    global _silero_loaded, _silero_model
    if _silero_loaded:
        return
```

### Error Handling Strategy (2/3 files)
- Use try/except blocks for optional dependencies
- Provide detailed error messages with traceback
- Return meaningful error states to UI components
- Handle model loading failures gracefully

```python
try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False
```

### Constants Management (2/3 files)
- Define sample rates as module-level constants
- Use ALL_CAPS naming for constants
- Import constants from utility modules
- Group related constants together

```python
TTS_SAMPLE_RATE = 48000
MUSIC_SAMPLE_RATE = 32000
```

## Testing Patterns

### Test Structure (1/3 files)
- Use descriptive test function names with `test_` prefix
- Include docstrings explaining test purpose
- Test both normal and edge cases
- Use pytest fixtures and assertions

```python
def test_stereo_from_mono():
    """Tests that a mono channel is correctly duplicated to stereo."""
```

### Array Testing (1/3 files)
- Use `np.array_equal()` for numpy array comparisons
- Test array shapes explicitly with assertions
- Create test data with `np.linspace()` and `np.random.rand()`
- Verify data types with `.astype()` conversions

```python
assert stereo_array.shape == (10, 2)
assert np.array_equal(stereo_array[:, 0], mono_array)
```

## Audio Processing Conventions

### Data Type Handling (2/3 files)
- Convert to `np.float32` for audio processing
- Handle tensor to numpy conversions with `.cpu().numpy()`
- Flatten batch dimensions when needed
- Ensure correct audio array shapes

```python
if not isinstance(wav, np.ndarray):
    wav = wav.cpu().numpy()
if wave.dtype != np.float32:
    wave = wave.astype(np.float32)
```

### File I/O Patterns (1/3 files)
- Use `tempfile.mkstemp()` for temporary audio files
- Write audio as PCM_16 format for compatibility
- Close file descriptors properly
- Return file paths for UI consumption

```python
fd, path = tempfile.mkstemp(suffix=".wav")
os.close(fd)
sf.write(path, wave, samplerate=sr, subtype="PCM_16")
```