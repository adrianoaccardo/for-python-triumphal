# mini-suno-mvp - Gradio app: TTS (Silero) and MusicGen integration (optional).
from typing import Any
import traceback

import numpy as np
import gradio as gr

from audio_utils import save_wave_np, TTS_SAMPLE_RATE, MUSIC_SAMPLE_RATE

try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False


# Silero TTS (via torch.hub)
_silero_loaded: bool = False
_silero_model: Any = None
_silero_utils: Any = None


def ensure_silero_loaded(language: str = "en", speaker: str = "v3_en") -> None:
    """Lazy-load Silero TTS model via torch.hub.

    Raises RuntimeError when torch isn't available.
    """
    global _silero_loaded, _silero_model, _silero_utils

    if _silero_loaded:
        return

    if not _TORCH_AVAILABLE:
        raise RuntimeError(
            "torch non disponibile. Installa torch prima di usare Silero TTS."
        )

    # Wrap arguments to keep line lengths under 79 chars for flake8
    res = torch.hub.load(
        repo_or_dir="snakers4/silero-models",
        model="silero_tts",
        language=language,
        speaker=speaker,
    )

    if isinstance(res, (list, tuple)) and len(res) >= 2:
        _silero_model, _silero_utils = res[0], res[1]
    else:
        _silero_model = res
        _silero_utils = None
    _silero_loaded = True


def silero_tts(text: str, language: str = "en", speaker: str = "v3_en") -> str:
    ensure_silero_loaded(language=language, speaker=speaker)

    wav = _silero_model.apply_tts(
        texts=text, speaker=speaker, sample_rate=TTS_SAMPLE_RATE
    )

    if not isinstance(wav, np.ndarray):
        wav = wav.cpu().numpy()

    return save_wave_np(wav, sr=TTS_SAMPLE_RATE)


# MusicGen integration (optional)
_musicgen_available: bool = False
_musicgen_model: Any = None


def ensure_musicgen_loaded(
    model_size: str = "small",
    device: str = "cuda",
) -> None:
    """Lazy-load MusicGen model when available.

    This function imports the optional `musicgen` package at runtime so the
    repository can be used without that dependency installed.
    """

    global _musicgen_available, _musicgen_model

    if _musicgen_available:
        return

    try:
        from musicgen import MusicGen
    except ImportError:
        raise RuntimeError(
            "Pacchetto musicgen non trovato. Installalo da GitHub per usare questa funzionalità."
        )

    _musicgen_model = MusicGen.get_pretrained(model_size)
    _musicgen_model.to(device)
    _musicgen_available = True


def musicgen_generate(
    prompt: str,
    duration: int = 8,
    model_size: str = "small",
    device: str = "cuda",
) -> str:
    ensure_musicgen_loaded(model_size=model_size, device=device)

    wav = _musicgen_model.generate([prompt], duration=duration)

    # wav can be a list/tuple of arrays or a single array
    arr = wav[0] if isinstance(wav, (list, tuple)) else wav

    if not isinstance(arr, np.ndarray):
        arr = arr.cpu().numpy()

    return save_wave_np(arr, sr=MUSIC_SAMPLE_RATE)


with gr.Blocks(title="mini-suno-mvp") as demo:
    gr.Markdown("<h2>mini-suno-mvp — TTS reale + MusicGen (opzionale)</h2>")
    with gr.Tab("TTS"):
        txt = gr.Textbox(
            label="Testo",
            value="Ciao, questo è un test",
            lines=3,
        )

        lang = gr.Dropdown(choices=["en", "it", "es", "ru"], value="en")
        speaker = gr.Textbox(label="Speaker (Silero)", value="v3_en")
        btn = gr.Button("Genera parlato")
        out = gr.Audio()
        status_tts = gr.Textbox(interactive=False, label="Status")

        def run_tts(t, language, sp):
            try:
                path = silero_tts(t, language=language, speaker=sp)
                return path, "Successo!"
            except Exception:
                # Use traceback to get detailed error for the status
                detailed_error = traceback.format_exc()
                return None, f"Errore: {detailed_error}"
        btn.click(run_tts, inputs=[txt, lang, speaker], outputs=[out, status_tts])

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
        status_music = gr.Textbox(interactive=False, label="Status")

        def run_music(p, d, ms, dev):
            try:
                res = musicgen_generate(
                    p, duration=int(d), model_size=ms, device=dev
                )
                return res, "Successo!"
            except Exception:
                detailed_error = traceback.format_exc()
                return None, f"Errore: {detailed_error}"

        btn2.click(
            run_music,
            inputs=[prompt, duration, model_size, device],
            outputs=[out2, status_music],
        )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=False)
