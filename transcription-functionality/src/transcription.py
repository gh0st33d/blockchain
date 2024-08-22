import whisper
import torch

def load_whisper_model(model_name="base"):
    # Load Whisper model 
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    model = whisper.load_model(model_name, device=device)
    return model

def transcribe_audio(model, audio_path):
    result = model.transcribe(audio_path, verbose=True)
    segments = result['segments']
    
    formatted_transcription = []
    for segment in segments:
        start = segment['start']
        end = segment['end']
        text = segment['text']
        formatted_line = f"[{start:.2f} - {end:.2f}] {text}"
        formatted_transcription.append(formatted_line)
    
    return formatted_transcription
