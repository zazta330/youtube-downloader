from downloader import VideoDownloader
import shutil

def test_quality_settings():
    print("Testing Quality Settings...")
    dl = VideoDownloader()
    
    ffmpeg_present = shutil.which('ffmpeg') is not None
    print(f"FFmpeg present in system: {ffmpeg_present}")
    print(f"Downloader detected ffmpeg: {dl.is_ffmpeg_available()}")
    
    expected_format = 'bestvideo+bestaudio/best' if ffmpeg_present else 'best'
    actual_format = dl.ydl_opts['format']
    
    print(f"Format selected: {actual_format}")
    
    if dl.is_ffmpeg_available() == ffmpeg_present and actual_format == expected_format:
        print("Verification PASSED: Quality settings match environment.")
    else:
        print("Verification FAILED: Quality settings do not match environment.")

if __name__ == "__main__":
    test_quality_settings()
