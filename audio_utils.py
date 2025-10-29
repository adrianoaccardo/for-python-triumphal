"""Small audio helper utilities used by the Gradio UI.

This module keeps minimal, dependency-light helpers that operate with numpy
arrays and write temporary WAV files. It intentionally does not import heavy
ML packages.
"""
from typing import Tuple
import tempfile
import os

import numpy as np
import soundfile as sf

# Sample rate constants used across the project
TTS_SAMPLE_RATE = 48000
MUSIC_SAMPLE_RATE = 32000


def save_wave_np(wave: np.ndarray, sr: int = TTS_SAMPLE_RATE) -> str:
    """Write a float32 numpy array to a temporary WAV file and return path.

    The file is written as PCM_16 which is a common format for playback.
    """
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    # Ensure correct dtype
    if wave.dtype != np.float32:
        wave = wave.astype(np.float32)
    sf.write(path, wave, samplerate=sr, subtype="PCM_16")
    return path


def stereo_from_mono(arr: np.ndarray) -> np.ndarray:
    """Convert a mono array (N,) to stereo (N,2) by duplicating channel.

    If input already has 2 dims or 2 channels, returns it unchanged.
    """
    if arr.ndim == 1:
        return np.stack([arr, arr], axis=-1)
    return arr
