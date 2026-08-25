from pathlib import Path
import yt_dlp

def download_video_from_search(query, output_folder="VideoDownloads"):
    """
    Searches YouTube for a query, grabs the first matching result,
    and downloads it as an MP4 video file.
    """
    # Create the output directory inside your default Videos folder
    download_path = Path.home() / "Videos" / output_folder
    download_path.mkdir(parents=True, exist_ok=True)

    # yt-dlp Configuration Options for MP4 Video
    ydl_opts = {
        'default_search': 'ytsearch1',
        
        # 1. Tries best single pre-merged stream (video+audio together)
        # 2. Falls back to any format that doesn't strictly require merging
        #'format': 'best[ext=mp4]/best',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        
        # Output template: saves file as "Video Title.mp4"
        'outtmpl': str(download_path / '%(title)s.%(ext)s'),
        
        'quiet': False,
        'no_warnings': True,
    }

    print(f"[*] Searching YouTube for video: '{query}'...")
    print(f"[*] Save location: {download_path}\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=True)
            
            if 'entries' in info and len(info['entries']) > 0:
                video_data = info['entries'][0]
                title = video_data.get('title', 'Unknown Title')
                duration = video_data.get('duration', 0)
                print(f"\n[+] Successfully downloaded: '{title}' ({duration // 60}m {duration % 60}s)")
            else:
                print("[-] No video results found for query.")

        except Exception as e:
            print(f"[-] Error downloading video: {e}")

if __name__ == "__main__":
    search_query = "A$AP Rocky - DMB"
    download_video_from_search(search_query)