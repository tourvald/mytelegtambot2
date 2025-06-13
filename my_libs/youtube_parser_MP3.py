import os
import yt_dlp
from pydub import AudioSegment

def download_youtube_audio(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'cookiefile': 'www.youtube.com_cookies.txt',  # Укажите путь к вашему файлу куки
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            downloaded_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')

        output_file = f"{video_title}.mp3"
        os.rename(downloaded_file, output_file)

        print(f"Audio saved as {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Пример использования
download_youtube_audio("https://www.youtube.com/watch?v=sXC6AUbY69A&t=14179s")