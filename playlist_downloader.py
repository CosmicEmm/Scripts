from yt_dlp import YoutubeDL
from sys import argv

if len(argv) < 2:
    print("Please provide a playlist or video URL as a command-line argument.")
    exit(1)

link = argv[1]

# Configuration options for 360p playlist downloads
ydl_opts = {
    # Force best video up to 360p + best audio
    'format': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]/best',
    
    # Output template — saves inside a folder named after the playlist
    'outtmpl': 'F:/YouTube/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s',

    # Merge video + audio into MP4
    'merge_output_format': 'mp4',

    # Resume partially downloaded files
    'continuedl': True,

    # Download entire playlist (not just a single video)
    'yes_playlist': True,

    # Skip already-downloaded videos (optional but recommended)
    'download_archive': 'F:/YouTube/downloaded.txt',

    # Quiet mode: reduces clutter in the console (optional)
    'quiet': False,
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])