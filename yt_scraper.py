import pandas as pd
from datetime import datetime
from yt_dlp import YoutubeDL
import os

def fetch_channel_to_sheet(channel_url, channel_name, n_videos=10, output_excel="all_channels.xlsx"):
    """
    Fetch last `n_videos` from a YouTube channel and save/append them to a specific sheet in an Excel workbook.

    Args:
        channel_url (str): YouTube channel URL.
        channel_name (str): Sheet name in Excel to store this channel's videos.
        n_videos (int): Number of latest videos to fetch.
        output_excel (str): Excel workbook path.
    """
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
        "no_warnings": True   # hide warnings
    }

    # Load existing sheet if it exists
    if os.path.exists(output_excel):
        try:
            df_existing = pd.read_excel(output_excel, sheet_name=channel_name)
            existing_urls = set(df_existing["URL"].tolist())
        except ValueError:  # Sheet doesn't exist yet
            df_existing = pd.DataFrame(columns=["Title", "URL", "Upload Date", "Duration"])
            existing_urls = set()
    else:
        df_existing = pd.DataFrame(columns=["Title", "URL", "Upload Date", "Duration"])
        existing_urls = set()

    with YoutubeDL(ydl_opts) as ydl:
        # Fetch last n_videos
        data = ydl.extract_info(channel_url, download=False)
        last_videos = data["entries"][:n_videos]

        new_videos = []
        for video in last_videos:
            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            if video_url in existing_urls:
                continue  # skip already saved videos

            info = ydl.extract_info(video_url, download=False)

            # Format upload date
            upload_date = info.get("upload_date")
            if upload_date:
                upload_date = datetime.strptime(upload_date, "%Y%m%d").strftime("%Y-%m-%d")

            # Format duration
            duration = info.get("duration")
            if duration is not None:
                minutes, seconds = divmod(duration, 60)
                duration = f"{minutes}m {seconds}s"

            new_videos.append({
                "Title": info.get("title"),
                "URL": video_url,
                "Upload Date": upload_date,
                "Duration": duration
            })

    # Append new videos
    if new_videos:
        df_new = pd.DataFrame(new_videos)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)

        # Save to Excel with multiple sheets
        with pd.ExcelWriter(output_excel, mode='a' if os.path.exists(output_excel) else 'w', engine='openpyxl') as writer:
            df_final.to_excel(writer, sheet_name=channel_name, index=False)

        print(f"Added {len(new_videos)} new videos to sheet '{channel_name}'. Total videos: {len(df_final)}")
    else:
        print(f"No new videos to add to sheet '{channel_name}'.")


# Example usage:
fetch_channel_to_sheet(
    channel_url="https://www.youtube.com/@abubakrzoud/videos",
    channel_name="Abu Bakr Zoud",
    n_videos=5,
    output_excel="all_channels.xlsx"
)

fetch_channel_to_sheet(
    channel_url="https://www.youtube.com/@belal.assaad/videos",
    channel_name="Belal Assaad",
    n_videos=5,
    output_excel="all_channels.xlsx"
)

fetch_channel_to_sheet(
    channel_url="https://www.youtube.com/@Arabic101/videos",
    channel_name="Arabic 101",
    n_videos=5,
    output_excel="all_channels.xlsx"
)

fetch_channel_to_sheet(
    channel_url="https://www.youtube.com/@KhalidMehmoodAbbasiOfficial/videos",
    channel_name="Khalid Mehmood Abbasi",
    n_videos=5,
    output_excel="all_channels.xlsx"
)

fetch_channel_to_sheet(
    channel_url="https://www.youtube.com/@yaqeeninstituteofficial/videos",
    channel_name="Yaqeen Institute",
    n_videos=5,
    output_excel="all_channels.xlsx"
)

fetch_channel_to_sheet(
    channel_url="https://www.youtube.com/@tarteelai/videos",
    channel_name="Tarteel AI",
    n_videos=5,
    output_excel="all_channels.xlsx"
)

fetch_channel_to_sheet(
    channel_url="https://www.youtube.com/@Ali.Hammuda/videos",
    channel_name="Ali Hammuda",
    n_videos=5,
    output_excel="all_channels.xlsx"
)

fetch_channel_to_sheet(
    channel_url="https://www.youtube.com/@TowardsEternity/videos",
    channel_name="Towards Eternity",
    n_videos=5,
    output_excel="all_channels.xlsx"
)

fetch_channel_to_sheet(
    channel_url="https://www.youtube.com/@EngineerMuhammadAliMirzaClips/videos",
    channel_name="Engineer Muhammad Ali Mirza",
    n_videos=5,
    output_excel="all_channels.xlsx"
)