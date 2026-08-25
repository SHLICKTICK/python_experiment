import sys
from pathlib import Path
import yt_dlp

def get_download_path():
    download_path = Path.home() / "Videos" / "VideoDownloads"
    download_path.mkdir(parents=True, exist_ok=True)
    return download_path

def download_progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        eta = d.get('_eta_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        print(f"\r[*] Downloading: {percent} | Speed: {speed} | ETA: {eta}    ", end="", flush=True)
    elif d['status'] == 'finished':
        print("\n[+] Download complete! Finalizing file...")

def select_quality():
    """Displays a resolution choice menu and returns the corresponding yt-dlp format string."""
    options = {
        "1": ("Best Available (Highest Quality / 4K)", "bestvideo+bestaudio/best"),
        "2": ("1080p Full HD", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"),
        "3": ("720p HD", "bestvideo[height<=720]+bestaudio/best[height<=720]"),
        "4": ("480p Standard", "bestvideo[height<=480]+bestaudio/best[height<=480]"),
        "5": ("360p Low", "bestvideo[height<=360]+bestaudio/best[height<=360]"),
        "6": ("Audio Only (MP3 format)", "bestaudio/best")
    }

    print("\nSelect Download Quality:")
    for key, (label, _) in options.items():
        print(f"  [{key}] {label}")

    while True:
        choice = input("\nEnter choice (1-6) [Default: 1]: ").strip()
        if choice == "":
            return options["1"][1], False
        if choice in options:
            is_audio_only = (choice == "6")
            return options[choice][1], is_audio_only
        print("[-] Invalid choice. Please enter a number between 1 and 6.")

def run_cli():
    print("=" * 55)
    print("      YOUTUBE QUALITY-SELECTABLE CLI DOWNLOADER      ")
    print("=" * 55)

    try:
        url_input = input("\nPaste YouTube URL (or 'q' to quit): ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n[-] Cancelled.")
        sys.exit(0)

    if url_input.lower() in ('q', 'quit', 'exit', ''):
        print("Exiting downloader.")
        sys.exit(0)

    # 1. Prompt for Quality Selection
    format_selector, is_audio_only = select_quality()
    save_dir = get_download_path()

    # 2. Build Options Dynamic to Choice
    ydl_opts = {
        'format': format_selector,
        'outtmpl': str(save_dir / '%(title)s.%(ext)s'),
        'progress_hooks': [download_progress_hook],
        'quiet': True,
        'no_warnings': True,
    }

    # If Audio Only was chosen, append FFmpeg postprocessor to output MP3
    if is_audio_only:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    print(f"\n[*] Target directory: {save_dir}")
    print(f"[*] Fetching media metadata...")

    # 3. Execute Download with Error Handling
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url_input, download=True)
            title = info.get('title', 'Media File')
            print(f"\n[✔] Successfully downloaded: '{title}'")

        except yt_dlp.utils.DownloadError as e:
            print(f"\n[✘] Download Error: Invalid link or restricted video.\n    Details: {e}")
        except Exception as e:
            print(f"\n[✘] Unexpected Error: {e}")

if __name__ == "__main__":
    run_cli()