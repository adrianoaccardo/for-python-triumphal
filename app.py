# mini-suno-mvp - Gradio app con TTS (Silero) e integrazione MusicGen (opzionale).
import os
import tempfile
from typing import Any

import numpy as np
import soundfile as sf
import gradio as gr

try:
    import torch
    _TORCH_AVAILABLE = True
except Exception:
    _TORCH_AVAILABLE = False

def save_wave_np(wave: np.ndarray, sr: int = 22050) -> str:
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    sf.write(path, wave, samplerate=sr, subtype='PCM_16')
    return path

# Silero TTS (via torch.hub)
_silero_loaded: bool = False
_silero_model: Any = None
_silero_utils: Any = None
_silero_sample_rate: int = 48000

def ensure_silero_loaded(language: str = "en", speaker: str = "v3_en") -> None:
    """Lazy-load Silero TTS model via torch.hub.

    Raises RuntimeError when torch isn't available.
    """
    global _silero_loaded, _silero_model, _silero_utils, _silero_sample_rate

    if _silero_loaded:
        return

    if not _TORCH_AVAILABLE:
        raise RuntimeError(
            "torch non disponibile. Installa torch prima di usare Silero TTS."
        )

    # Wrap arguments to keep line lengths under 79 chars for flake8
    _silero_model, _silero_utils = torch.hub.load(
        repo_or_dir="snakers4/silero-models",
        model="silero_tts",
        language=language,
        speaker=speaker,
    )

    _silero_sample_rate = 48000
    _silero_loaded = True

def silero_tts(text: str, language: str = "en", speaker: str = "v3_en") -> str:
    ensure_silero_loaded(language=language, speaker=speaker)

    wav = _silero_model.apply_tts(
        texts=text, speaker=speaker, sample_rate=_silero_sample_rate
    )

    if not isinstance(wav, np.ndarray):
        wav = wav.cpu().numpy()

    if wav.dtype != np.float32:
        wav = wav.astype(np.float32)

    return save_wave_np(wav, sr=_silero_sample_rate)

# MusicGen integration (optional)
_musicgen_available: bool = False
_musicgen_model: Any = None

def ensure_musicgen_loaded(model_size: str = "small", device: str = "cuda") -> None:
    """Lazy-load MusicGen model when available.

    This function imports the optional `musicgen` package at runtime so the
    repository can be used without that dependency installed.
    """

    global _musicgen_available, _musicgen_model

    if _musicgen_available:
        return

    from musicgen import MusicGen

    _musicgen_model = MusicGen.get_pretrained(model_size)
    _musicgen_model.to(device)
    _musicgen_available = True

def musicgen_generate(
    prompt: str, duration: int = 8, model_size: str = "small", device: str = "cuda"
) -> str:
    ensure_musicgen_loaded(model_size=model_size, device=device)

    wav = _musicgen_model.generate([prompt], duration=duration)

    # wav can be a list/tuple of arrays or a single array
    arr = wav[0] if isinstance(wav, (list, tuple)) else wav

    sr = 32000

    if not isinstance(arr, np.ndarray):
        arr = arr.cpu().numpy()

    return save_wave_np(arr, sr=sr)

with gr.Blocks(title="mini-suno-mvp") as demo:
    gr.Markdown("<h2>mini-suno-mvp — TTS reale + MusicGen (opzionale)</h2>")
    with gr.Tab("TTS"):
        txt = gr.Textbox(label="Testo", value="Ciao, questo è un test", lines=3)
        lang = gr.Dropdown(choices=["en","it","es","ru"], value="en")
        speaker = gr.Textbox(label="Speaker (Silero)", value="v3_en")
        btn = gr.Button("Genera parlato")
        out = gr.Audio()
        def run_tts(t, language, sp):
            try:
                return silero_tts(t, language=language, speaker=sp)
            except Exception:
                # swallow the error for the UI; this keeps the exception
                # variable from being unused (flake8 F841)
                return None
        btn.click(run_tts, inputs=[txt, lang, speaker], outputs=[out])

    with gr.Tab("Text→Music"):
        prompt = gr.Textbox(
            label="Prompt musicale",
            value="Calm ambient pad with soft melody",
            lines=3,
        )

        duration = gr.Slider(2, 30, value=8, step=1)

        model_size = gr.Dropdown(
            choices=["small", "medium", "large"], value="small"
        )

        device = gr.Dropdown(choices=["cuda", "cpu"], value="cuda")
        btn2 = gr.Button("Genera musica")
        out2 = gr.Audio()
        status = gr.Textbox(interactive=False)
        def run_music(p, d, ms, dev):
            try:
                return musicgen_generate(p, duration=int(d), model_size=ms, device=dev), ""
            except Exception as e:
                return None, str(e)
        btn2.click(run_music, inputs=[prompt, duration, model_size, device], outputs=[out2, status])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=False)
