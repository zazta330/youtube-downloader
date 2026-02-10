import customtkinter as ctk
from tkinter import filedialog
import threading
from downloader import VideoDownloader

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader")
        self.geometry("600x400")

        self.downloader = VideoDownloader()
        self.downloader.set_progress_callback(self.update_progress)

        # UI Elements
        self.label_url = ctk.CTkLabel(self, text="YouTube Video or Channel URL:")
        self.label_url.pack(pady=10)

        self.entry_url = ctk.CTkEntry(self, width=400, placeholder_text="Paste link here...")
        self.entry_url.pack(pady=5)

        self.btn_folder = ctk.CTkButton(self, text="Select Output Folder", command=self.select_folder)
        self.btn_folder.pack(pady=10)

        self.label_folder = ctk.CTkLabel(self, text="No folder selected", text_color="gray")
        self.label_folder.pack(pady=5)
        
        self.btn_download = ctk.CTkButton(self, text="Download", command=self.start_download_thread)
        self.btn_download.pack(pady=20)

        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.label_status = ctk.CTkLabel(self, text="Ready")
        self.label_status.pack(pady=10)

        # Quality Status
        if self.downloader.is_ffmpeg_available():
            self.label_quality = ctk.CTkLabel(self, text="High Quality Enabled (FFmpeg found)", text_color="green")
        else:
            self.label_quality = ctk.CTkLabel(self, text="Standard Quality (FFmpeg missing)\nInstall FFmpeg for 1080p+", text_color="orange")
        self.label_quality.pack(pady=5)

        self.output_path = ""

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_path = folder_selected
            self.label_folder.configure(text=f"Folder: {self.output_path}", text_color="white")

    def start_download_thread(self):
        url = self.entry_url.get()
        if not url:
            self.label_status.configure(text="Please enter a URL", text_color="red")
            return
        
        self.btn_download.configure(state="disabled")
        self.label_status.configure(text="Starting download...", text_color="white")
        self.progress_bar.set(0)
        
        thread = threading.Thread(target=self.download_task, args=(url,))
        thread.start()

    def download_task(self, url):
        # This runs in a separate thread
        try:
            success, message = self.downloader.download_video(url, self.output_path)
            self.after(0, self.update_status, success, message)
        except Exception as e:
            self.after(0, self.update_status, False, str(e))

    def update_progress(self, percent, status_text):
        # This is called from the download thread, so we must schedule the UI update
        self.after(0, self._update_progress_ui, percent, status_text)

    def _update_progress_ui(self, percent, status_text):
        self.progress_bar.set(percent)
        self.label_status.configure(text=f"{status_text} ({int(percent*100)}%)")

    def update_status(self, success, message):
        self.btn_download.configure(state="normal")
        if success:
            self.label_status.configure(text=message, text_color="green")
            self.progress_bar.set(1)
        else:
            self.label_status.configure(text=f"Error: {message}", text_color="red")
            self.progress_bar.set(0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
