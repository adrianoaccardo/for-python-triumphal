# mini-suno-mvp - Gradio app: TTS (Silero) and MusicGen integration (optional).
from typing import Any
import traceback

import numpy as np
import gradio as gr
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from audio_utils import save_wave_np, TTS_SAMPLE_RATE, MUSIC_SAMPLE_RATE
import scipy

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
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")


def musicgen_generate(
    prompt: str,
    duration: int = 8,
) -> str:

    inputs = processor(
        text=[prompt],
        padding=True,
        return_tensors="pt",
    )

    audio_values = model.generate(**inputs, max_new_tokens=int(duration * 256 / 50))
    
    sampling_rate = model.config.audio_encoder.sampling_rate
    audio_numpy = audio_values.cpu().numpy()
    
    # The output is a batch, so we take the first element
    audio_numpy = audio_numpy[0]

    # The output of the model is mono, so we don't need to average channels.
    # The shape is (num_channels, num_samples), but since it's mono, it's (1, num_samples)
    # We need to flatten it to (num_samples,)
    audio_numpy = audio_numpy.flatten()

    return save_wave_np(audio_numpy, sr=sampling_rate)


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
            value="A beautiful piano melody",
            lines=3,
        )

        duration = gr.Slider(2, 30, value=8, step=1)

        btn2 = gr.Button("Genera musica")
        out2 = gr.Audio()
        status_music = gr.Textbox(interactive=False, label="Status")

        def run_music(p, d):
            try:
                res = musicgen_generate(
                    p, duration=int(d)
                )
                return res, "Successo!"
            except Exception:
                detailed_error = traceback.format_exc()
                return None, f"Errore: {detailed_error}"

        btn2.click(
            run_music,
            inputs=[prompt, duration],
            outputs=[out2, status_music],
        )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=False)