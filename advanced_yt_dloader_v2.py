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
        print(f"\r[*] Progress: {percent} | Speed: {speed} | ETA: {eta}    ", end="", flush=True)
    elif d['status'] == 'finished':
        print("\n[+] Download complete! Processing final file...")

def run_cli():
    print("=" * 50)
    print("    YOUTUBE CLI DOWNLOADER (QUALITY SELECTOR)   ")
    print("=" * 50)

    try:
        url_input = input("\nPaste your YouTube link (or 'q' to quit): ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n[-] Operation cancelled.")
        sys.exit(0)

    if url_input.lower() in ('q', 'quit', 'exit', ''):
        sys.exit(0)

    print("\n[*] Fetching available video qualities...")

    # Fetch metadata first without downloading
    info_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(info_opts) as ydl:
        try:
            info = ydl.extract_info(url_input, download=False)
        except yt_dlp.utils.DownloadError:
            print("[✘] Error: Invalid URL or video unavailable.")
            return

    # Extract unique available video heights (resolutions)
    formats = info.get('formats', [])
    resolutions = set()
    for f in formats:
        height = f.get('height')
        # Keep valid video formats
        if height and f.get('vcodec') != 'none':
            resolutions.add(height)

    sorted_res = sorted(list(resolutions), reverse=True)
    
    if not sorted_res:
        print("[-] Could not parse resolution list. Defaulting to best available.")
        format_choice = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    else:
        print(f"\nTitle: {info.get('title')}")
        print("\nSelect Quality:")
        print(" [0] Best Available (Highest Quality)")
        for idx, res in enumerate(sorted_res, 1):
            print(f" [{idx}] {res}p")

        try:
            choice = input(f"\nEnter choice (0-{len(sorted_res)}): ").strip()
            choice_idx = int(choice)
            
            if choice_idx == 0 or choice_idx > len(sorted_res):
                # Highest quality selected
                format_choice = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            else:
                target_height = sorted_res[choice_idx - 1]
                # Target exact selected resolution or lower fallback
                format_choice = f"bestvideo[height<={target_height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={target_height}][ext=mp4]/best"
        except (ValueError, IndexError):
            print("[!] Invalid selection. Defaulting to Best Available.")
            format_choice = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

    save_dir = get_download_path()
    ydl_opts = {
        'format': format_choice,
        'outtmpl': str(save_dir / '%(title)s (%(height)sp).%(ext)s'),
        'progress_hooks': [download_progress_hook],
        'quiet': True,
        'no_warnings': True,
    }

    print(f"\n[*] Starting download...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url_input])
            print(f"\n[✔] Download completed successfully!")
        except Exception as e:
            print(f"\n[✘] Download failed: {e}")

if __name__ == "__main__":
    run_cli()