from downloader import VideoDownloader
import os

def test_callback(progress, status):
    print(f"Status: {status} ({progress*100:.1f}%)")

def test_channel_support():
    print("Testing Channel Support Logic...")
    dl = VideoDownloader()
    dl.set_progress_callback(test_callback)
    
    # Check if 'outtmpl' is correctly set to include uploader
    outtmpl = dl.ydl_opts['outtmpl']
    print(f"Output Template: {outtmpl}")
    
    if "%(uploader)s" in outtmpl:
        print("Verification PASSED: Output template includes uploader folder.")
    else:
        print("Verification FAILED: Output template missing uploader.")

    # Check that noplaylist is False
    noplaylist = dl.ydl_opts.get('noplaylist')
    print(f"No Playlist option: {noplaylist}")
    
    if noplaylist is False:
        print("Verification PASSED: Playlist downloading is enabled.")
    else:
        print("Verification FAILED: Playlist downloading might be disabled.")

if __name__ == "__main__":
    test_channel_support()
