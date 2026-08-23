import time
from pathlib import Path
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# File extension categories
EXTENSIONS_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".xlsx", ".csv", ".pptx", ".epub"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".iso", ".deb"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Audio_Video": [".mp3", ".wav", ".flac", ".mp4", ".mkv", ".mov", ".avi"],
    "Code_Scripts": [".py", ".js", ".html", ".css", ".json", ".cpp", ".c", ".sh", ".ps1"],
}

class DownloadOrganizerHandler(FileSystemEventHandler):
    def __init__(self, downloads_dir):
        self.downloads_dir = Path(downloads_dir)

    def on_created(self, event):
        """Triggers automatically when a new file or directory is created."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        self.process_file(file_path)

    def process_file(self, file_path):
        # Ignore temporary download files (.crdownload, .tmp, .part)
        if file_path.suffix.lower() in [".crdownload", ".tmp", ".part", ".download"]:
            return

        # Give active downloads or file transfers a brief moment to finish writing
        time.sleep(1)

        if not file_path.exists():
            return

        file_extension = file_path.suffix.lower()
        matched_category = "Other"

        # Match extension to folder category
        for category, extensions in EXTENSIONS_MAP.items():
            if file_extension in extensions:
                matched_category = category
                break

        # Prevent moving files that are inside the category subfolders
        if file_path.parent != self.downloads_dir:
            return

        destination_dir = self.downloads_dir / matched_category
        destination_dir.mkdir(exist_ok=True)

        destination_file = self.resolve_collision(destination_dir / file_path.name)

        try:
            shutil.move(str(file_path), str(destination_file))
            print(f"[+] Instantly organized: '{file_path.name}' ➔ '{matched_category}/'")
        except Exception as e:
            print(f"[-] Error moving '{file_path.name}': {e}")

    def resolve_collision(self, target_path):
        """Appends a numerical counter if a file with the same name exists."""
        if not target_path.exists():
            return target_path

        stem = target_path.stem
        suffix = target_path.suffix
        parent = target_path.parent
        counter = 1

        while target_path.exists():
            target_path = parent / f"{stem}_{counter}{suffix}"
            counter += 1

        return target_path

if __name__ == "__main__":
    downloads_path = Path.home() / "Downloads"
    event_handler = DownloadOrganizerHandler(downloads_path)
    observer = Observer()
    observer.schedule(event_handler, path=str(downloads_path), recursive=False)

    print(f"[*] Real-time folder monitor active on: {downloads_path}")
    print("[*] Press Ctrl+C to stop listening.")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[*] Folder monitoring stopped.")
    
    observer.join()