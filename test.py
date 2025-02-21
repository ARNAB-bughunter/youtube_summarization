import logging
import os
import yt_dlp
import whisper
import time
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate



def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def download_audio(urls, output_filename="output_file.mp3"):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': 'output_file.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(urls)
        if error_code:
            logger.error("Failed to download audio.")
            return None
    
    return output_filename

def transcribe_audio(audio_file):
    model = whisper.load_model("tiny")
    return model.transcribe(audio_file)["text"]

def summarize_text(text):
    model = OllamaLLM(model="llama3.2:1b")
    prompt = ChatPromptTemplate.from_template("You task is to summarizing the following text content: {content}.")
    chain = prompt | model
    return chain.invoke({"content": text})

if __name__ == "__main__":
    s_ = time.time()
    logger = setup_logger()
    
    URLS = ['https://www.youtube.com/watch?v=Y8Tko2YC5hA']
    
    logger.info("Starting audio download...")
    audio_file = download_audio(URLS)
    
    if audio_file:
        logger.info("Transcribing audio...")
        transcript = transcribe_audio(audio_file)
        
        logger.info("Summarizing transcript...")
        summary = summarize_text(transcript)
        
        logger.info("Summary:")
        print(summary)
    else:
        logger.error("Audio processing failed.")
    
    print(time.time() - s_)
