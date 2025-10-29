import torch
import torchaudio

# Load Silero TTS model
model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language='en',
                                     speaker='v3_en')

# Test text
text = "Hello, this is a test of text to speech synthesis."

# Generate audio
audio = model.apply_tts(text=text,
                       speaker='en_0',
                       sample_rate=48000)

# Save to file
torchaudio.save('test_output.wav', audio.unsqueeze(0), 48000)
print("Audio saved to test_output.wav")
print(f"Audio tensor shape: {audio.shape}")