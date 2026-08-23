import os
import shutil
from pathlib import Path

# Define target folder categories and their corresponding file extensions
EXTENSIONS_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".xlsx", ".csv", ".pptx", ".epub"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".iso", ".deb"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Audio_Video": [".mp3", ".wav", ".flac", ".mp4", ".mkv", ".mov", ".avi"],
    "Code_Scripts": [".py", ".js", ".html", ".css", ".json", ".cpp", ".c", ".sh", ".ps1"],
}

def get_downloads_path():
    """Returns the absolute path to the user's Downloads folder."""
    return Path.home() / "Downloads"

def resolve_filename_collision(target_path):
    """Prevents overwriting files by appending a counter if a duplicate exists."""
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

def organize_downloads():
    downloads_dir = get_downloads_path()

    if not downloads_dir.exists():
        print(f"[-] Directory not found: {downloads_dir}")
        return

    print(f"[*] Organizing: {downloads_dir}\n")

    # Iterate over all items in the Downloads directory
    for item in downloads_dir.iterdir():
        # Skip subdirectories to prevent moving created category folders
        if item.is_dir():
            continue

        file_extension = item.suffix.lower()
        matched_category = "Other"

        # Match extension to folder category
        for category, extensions in EXTENSIONS_MAP.items():
            if file_extension in extensions:
                matched_category = category
                break

        # Create destination directory if it doesn't exist
        destination_dir = downloads_dir / matched_category
        destination_dir.mkdir(exist_ok=True)

        # Handle duplicate filenames safely
        destination_file = resolve_filename_collision(destination_dir / item.name)

        # Move the file
        try:
            shutil.move(str(item), str(destination_file))
            print(f"[+] Moved '{item.name}' ➔ '{matched_category}/'")
        except Exception as e:
            print(f"[-] Failed to move '{item.name}': {e}")

    print("\n[+] Cleanup complete!")

if __name__ == "__main__":
    organize_downloads()