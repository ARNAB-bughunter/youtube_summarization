import whisper

def transcribe_audio(audio_file):
    model = whisper.load_model("tiny")
    return model.transcribe(audio_file)["text"]