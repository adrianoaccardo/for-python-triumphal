import numpy as np
import pytest

from audio_utils import stereo_from_mono, save_wave_np, TTS_SAMPLE_RATE


def test_stereo_from_mono():
    """Tests that a mono channel is correctly duplicated to stereo."""
    # Create a simple mono audio segment (10 samples)
    mono_array = np.linspace(0, 1, 10, dtype=np.float32)
    assert mono_array.shape == (10,)

    # Convert to stereo
    stereo_array = stereo_from_mono(mono_array)

    # Check new shape
    assert stereo_array.shape == (10, 2)

    # Check that the two channels are identical
    assert np.array_equal(stereo_array[:, 0], stereo_array[:, 1])

    # Check that the content is the same as the original mono array
    assert np.array_equal(stereo_array[:, 0], mono_array)


def test_stereo_from_mono_already_stereo():
    """Tests that a stereo array is returned unchanged."""
    # Create a stereo array
    stereo_array = np.random.rand(10, 2).astype(np.float32)
    assert stereo_array.shape == (10, 2)

    # Pass it to the function
    result_array = stereo_from_mono(stereo_array)

    # Check that the array is identical to the original
    assert np.array_equal(result_array, stereo_array)
