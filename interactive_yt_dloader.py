import sys
from pathlib import Path
import yt_dlp

def get_download_path():
    """Returns path to VideoDownloads folder in system default Videos directory."""
    download_path = Path.home() / "Videos" / "VideoDownloads"
    download_path.mkdir(parents=True, exist_ok=True)
    return download_path

def download_progress_hook(d):
    """Callback function to report progress cleanly in terminal."""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        eta = d.get('_eta_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        print(f"\r[*] Progress: {percent} | Speed: {speed} | ETA: {eta}    ", end="", flush=True)
    elif d['status'] == 'finished':
        print("\n[+] Download complete! Processing final file...")

def run_cli():
    print("=" * 50)
    print("       YOUTUBE INTERACTIVE CLI DOWNLOADER       ")
    print("=" * 50)

    # 1. Prompt user for input
    try:
        url_input = input("\nPaste your YouTube link (or type 'q' to quit): ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n[-] Operation cancelled.")
        sys.exit(0)

    if url_input.lower() in ('q', 'quit', 'exit', ''):
        print("Exiting downloader.")
        sys.exit(0)

    save_dir = get_download_path()

    # 2. Configure yt-dlp options
    ydl_opts = {
        # Best video + audio merged (requires FFmpeg) with single MP4 fallback
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        
        # Save output in default Videos directory
        'outtmpl': str(save_dir / '%(title)s.%(ext)s'),
        
        # Attach custom progress callback
        'progress_hooks': [download_progress_hook],
        
        # Keep logs clean
        'quiet': True,
        'no_warnings': True,
    }

    print(f"\n[*] Target save location: {save_dir}")
    print(f"[*] Fetching media information for: {url_input}\n")

    # 3. Execute download with error handling
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Perform download pass directly on the provided URL
            info = ydl.extract_info(url_input, download=True)
            
            title = info.get('title', 'Video')
            duration = info.get('duration', 0)
            mins, secs = divmod(duration, 60)
            
            print(f"\n[✔] Success: Saved '{title}' ({mins}m {secs}s)")

        except yt_dlp.utils.DownloadError as e:
            print("\n[✘] Download Error: Invalid URL or the video is restricted/unavailable.")
            print(f"    Details: {e}")
        except Exception as e:
            print(f"\n[✘] Unexpected Error: {e}")

if __name__ == "__main__":
    run_cli()