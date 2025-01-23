from yt_dlp import YoutubeDL
from sys import argv

if len(argv) < 2:
    print("Please provide a URL as command line argument")
    exit(1)   # exit(1) ensures that the program stops and doesn't try to continue and crash with an error


link = argv[1]

# ydl_opts is a dictionary that contains configuration options for the YoutubeDL instance
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': 'F:/YouTube/%(title)s.%(ext)s',        # output template
    'merge_output_format': 'mp4',                     # merge the best video and audio into a single mp4 file
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download(link)