import os
import yt_dlp

def download_youtube_video(url):
    print(f"Downloading video from {url} in the highest quality available as MP4...")
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  # Загрузка лучшего видео и аудио в формате MP4
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',  # Объединение видео и аудио в MP4
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=3octNnZfVaM"
    download_youtube_video(url)
