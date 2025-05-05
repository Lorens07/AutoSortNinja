import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Folder to monitor
WATCHED_FOLDER = os.path.expanduser("~/Downloads")

# List of extension and folder to move by the sort ninja
EXTENSIONS_MAP = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.docx', '.txt', '.pptx', '.xlsx'],
    'Music': ['.mp3', '.wav'],
    'Videos': ['.mp4', '.mov', '.avi'],
    'Installers': ['.exe', '.msi', '.apk', '.zip'],
}

# This class handles file system events (like file creation/modification)
class AutoSortHandler(FileSystemEventHandler):
    # Triggered when files are modified in the watched folder
    def on_modified(self, event):
        # List all files in the target directory
        for filename in os.listdir(WATCHED_FOLDER):
            src_path = os.path.join(WATCHED_FOLDER, filename)

            # Proceed only if it's a file not a folder
            if os.path.isfile(src_path):
                file_ext = os.path.splitext(filename)[1].lower()  # Get the file extension

                # Match the file extension to the correct folder
                for folder_name, extensions in EXTENSIONS_MAP.items():
                    if file_ext in extensions:
                        target_folder = os.path.join(WATCHED_FOLDER, folder_name)
                        os.makedirs(target_folder, exist_ok=True)  # Create folder if not exists
                        dst_path = os.path.join(target_folder, filename)

                        # Move the file
                        try:
                            shutil.move(src_path, dst_path)
                            print(f"Moved {filename} to {folder_name}")
                        except Exception as e:
                            print(f"Error moving {filename}: {e}")
                        break  # No need to check other types once matched

if __name__ == "__main__":
    print("AutoSort Ninja is now watching your folder...")

    # Create handler instance
    event_handler = AutoSortHandler()

    # Create and start observer
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(10)  # Keeps script running
    except KeyboardInterrupt:
        observer.stop()  # Stop if Ctrl+C is pressed

    observer.join()  # Wait until the observer thread stops

# Sorry for the limited design i create only this for less 30 mins
