from downloader import VideoDownloader
import os

def test_callback(progress, status):
    print(f"Progress: {progress:.2f}, Status: {status}")

def test_downloader():
    print("Initializing downloader...")
    downloader = VideoDownloader()
    downloader.set_progress_callback(test_callback)
    
    # Test with a known short video or just check if class works. 
    # Since we can't guarantee network or a specific video, we'll just check if it instantiates 
    # and maybe try to fetch info (but fetch info method is not exposed yet).
    # We will try to download a non-existent URL to check error handling.
    
    print("Testing error handling with invalid URL...")
    success, message = downloader.download_video("https://www.youtube.com/watch?v=invalid", ".")
    
    if not success:
        print(f"Caught expected error: {message}")
        print("Backend error handling verification passed.")
    else:
        print("Unexpected success on invalid URL.")

if __name__ == "__main__":
    test_downloader()
