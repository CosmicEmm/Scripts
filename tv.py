import shutil
import subprocess
import sys

CHANNELS = {
    "alarabiya": (
        "hls",
        "https://live.alarabiya.net/alarabiapublish/alarabiya.smil/playlist.m3u8",
    ),
    "alqahera": (
        "yt",
        "https://www.youtube.com/live/E3e0iVSFgPI?si=E9ASzSuHp0ODwQd5",
    ),
}

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <channel>")
    print("Channels:", ", ".join(sorted(CHANNELS)))
    sys.exit(1)

try:
    stream_type, url = CHANNELS[sys.argv[1].lower()]
except KeyError:
    print("Unknown channel.")
    sys.exit(1)

if stream_type == "yt":
    url = subprocess.check_output(
        ["yt-dlp", "-g", url],
        text=True
    ).splitlines()[0]

vlc = shutil.which("vlc") or r"C:\Program Files\VideoLAN\VLC\vlc.exe"

subprocess.Popen([
    vlc,
    "--fullscreen",
    "--network-caching=1000",
    url,
])