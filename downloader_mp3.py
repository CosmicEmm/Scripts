from yt_dlp import YoutubeDL
from sys import argv

if len(argv) < 2:
    print("Please provide a URL as command line argument")
    exit(1)

link = argv[1]

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'F:/YouTube/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])