import yt_dlp
import os
import sys

import shutil

class VideoDownloader:
    def __init__(self):
        # Check standard PATH
        self.ffmpeg_available = shutil.which('ffmpeg') is not None
        self.ffmpeg_location = None

        # Check for bundled FFmpeg (PyInstaller)
        if hasattr(sys, '_MEIPASS'):
            bundled_ffmpeg = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
            if os.path.exists(bundled_ffmpeg):
                self.ffmpeg_available = True
                self.ffmpeg_location = sys._MEIPASS # yt-dlp expects directory or executable path? 
                # yt-dlp 'ffmpeg_location' can be a directory or file. 
                # If directory, it looks for ffmpeg.exe inside.
        
        # Check Winget path if not found
        if not self.ffmpeg_available:
            local_app_data = os.environ.get('LOCALAPPDATA')
            if local_app_data:
                winget_path = os.path.join(local_app_data, 'Microsoft', 'WinGet', 'Links')
                ffmpeg_exe = os.path.join(winget_path, 'ffmpeg.exe')
                if os.path.exists(ffmpeg_exe):
                    os.environ["PATH"] += os.pathsep + winget_path
                    self.ffmpeg_available = True

        self.ydl_opts = {

            'format': 'bestvideo+bestaudio/best' if self.ffmpeg_available else 'best',
            'outtmpl': '%(uploader)s/%(title)s.%(ext)s',
            'noplaylist': False,
            'progress_hooks': [self.progress_hook],
        }
        if self.ffmpeg_location:
            self.ydl_opts['ffmpeg_location'] = self.ffmpeg_location

        self.progress_callback = None

    def set_progress_callback(self, callback):
        self.progress_callback = callback

    def progress_hook(self, d):
        if not self.progress_callback:
            return

        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%','')
                filename = os.path.basename(d.get('filename', ''))
                self.progress_callback(float(p) / 100, f"Downloading: {filename}")
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_callback(1.0, "Download Complete")

    def download_video(self, url, output_path):
        if output_path:
             # We only set the root directory here, the filename template is already set in __init__
             # to include the uploader folder. We need to respect that.
             # yt-dlp 'paths' option is better for this than modifying outtmpl directly if we want subfolders.
             self.ydl_opts['paths'] = {'home': output_path}
             # Add download archive to track downloaded videos
             self.ydl_opts['download_archive'] = os.path.join(output_path, 'download_history.txt')
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
            return True, "Download successful!"
        except Exception as e:
            return False, str(e)

    def is_ffmpeg_available(self):
        return self.ffmpeg_available
