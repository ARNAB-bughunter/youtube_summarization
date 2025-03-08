import yt_dlp
from src.config import Config

def download_audio(urls, video_id):
    backend_audio_path = Config.get_corpus("folder_paths","backend_audio_file_path")
    output_filename = f"{backend_audio_path}/{video_id}.mp3"

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': f'{backend_audio_path}/{video_id}.%(ext)s',  # Ensures the base filename is video_id
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'postprocessor_args': ['-y'],  # Overwrite if exists
        'keepvideo': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([urls])
        if error_code:
            return None
    
    return output_filename


  
def get_video_iframe(video_url):
    with yt_dlp.YoutubeDL({}) as ydl:
        info = ydl.extract_info(video_url, download=False)
        video_id = info.get("id")
        if video_id:
            iframe_code = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
            return iframe_code
    return ""