import os
from pathlib import Path
import yt_dlp

def download_audio_from_search(query, output_folder="MusicDownloads"):
    """
    Searches YouTube for a query, takes the first matching result,
    and downloads it as an MP3 file.
    """
    # Create the output directory if it doesn't exist
    download_path = Path.home() / "Music" / output_folder
    download_path.mkdir(parents=True, exist_ok=True)

    # yt-dlp Configuration Options
    ydl_opts = {
        # 'ytsearch1:' tells yt-dlp to search YouTube and grab the 1st result
        'default_search': 'ytsearch1',
        
        # Audio extraction configuration
        'format': 'bestaudio/best',
        #'postprocessors': [{
         #   'key': 'FFmpegExtractAudio',
       #     'preferredcodec': 'mp3',
        #    'preferredquality': '192',
        #}],
        
        # Output template: saves file as "Song Title.mp3"
        'outtmpl': str(download_path / '%(title)s.%(ext)s'),
        
        # Console output verbosity
        'quiet': False,
        'no_warnings': True,
    }

    print(f"[*] Searching YouTube for: '{query}'...")
    print(f"[*] Download destination: {download_path}\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Execute download pass using the search query string
            info = ydl.extract_info(query, download=True)
            
            # If search returned results, extract metadata
            if 'entries' in info and len(info['entries']) > 0:
                video_data = info['entries'][0]
                title = video_data.get('title', 'Unknown Title')
                duration = video_data.get('duration', 0)
                print(f"\n[+] Successfully downloaded: '{title}' ({duration // 60}m {duration % 60}s)")
            else:
                print("[-] No results found for query.")

        except Exception as e:
            print(f"[-] Error downloading audio: {e}")

if __name__ == "__main__":
    search_query = "Kendrick Lamar - m.a.a.d city"
    download_audio_from_search(search_query)