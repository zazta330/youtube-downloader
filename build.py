import PyInstaller.__main__
import customtkinter
import os
import shutil

def build():
    # 1. Find CustomTkinter path
    ctk_path = os.path.dirname(customtkinter.__file__)
    print(f"Found CustomTkinter at: {ctk_path}")

    # 2. Find FFmpeg path
    ffmpeg_path = shutil.which('ffmpeg')
    
    # Fallback to known Winget path if not in env
    if not ffmpeg_path:
        local_app_data = os.environ.get('LOCALAPPDATA')
        if local_app_data:
            possible_path = os.path.join(local_app_data, 'Microsoft', 'WinGet', 'Links', 'ffmpeg.exe')
            if os.path.exists(possible_path):
                ffmpeg_path = possible_path

    if not ffmpeg_path:
        print("ERROR: FFmpeg not found! Cannot bundle.")
        return

    print(f"Found FFmpeg at: {ffmpeg_path}")

    # 3. Construct PyInstaller arguments
    separator = ';' if os.name == 'nt' else ':'
    
    args = [
        'app.py',                                   # Script to convert
        '--name=YouTubeDownloader',                 # Name of the executable
        '--onefile',                                # Create a single executable
        '--windowed',                               # Hide the console
        '--noconfirm',                              # Overwrite output directory
        f'--add-data={ctk_path}{separator}customtkinter', # Add CustomTkinter data
        f'--add-binary={ffmpeg_path}{separator}.',  # Add FFmpeg binary to root
        '--clean',                                  # Clean cache
    ]

    print("Running PyInstaller with args:", args)
    
    # 4. Run PyInstaller
    PyInstaller.__main__.run(args)
    print("Build complete! executable should be in 'dist' folder.")

if __name__ == "__main__":
    build()
