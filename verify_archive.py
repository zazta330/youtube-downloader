from downloader import VideoDownloader
import os

def test_archive_option():
    dl = VideoDownloader()
    output_path = os.path.abspath("test_output")
    
    # We can't easily invoke download_video without a real URL and triggering a download.
    # But we can verify the logic by temporarily subclassing or mocking,
    # or just checking if we can instantiate it and if the logic *would* run.
    # Since download_video modifies self.ydl_opts IN PLACE (which might be a bug if called multiple times with different folders),
    # let's check that behavior.
    
    # Actually, inspecting download_video, it modifies self.ydl_opts. 
    # Let's verify that behavior.
    
    print("Testing VideoDownloader archive option...")
    try:
        # We will mock yt_dlp.YoutubeDL to avoid actual download and just check options
        import yt_dlp
        original_init = yt_dlp.YoutubeDL.__init__
        
        captured_opts = {}
        
        def mock_init(self, opts, *args, **kwargs):
            nonlocal captured_opts
            captured_opts.update(opts)
            # We don't call original init to avoid initialization overhead/errors
            pass
            
        def mock_download(self, urls):
            print("Mock download called")
            pass
            
        def mock_enter(self):
            return self
            
        def mock_exit(self, exc_type, exc_val, exc_tb):
            pass

        yt_dlp.YoutubeDL.__init__ = mock_init
        yt_dlp.YoutubeDL.download = mock_download
        yt_dlp.YoutubeDL.__enter__ = mock_enter
        yt_dlp.YoutubeDL.__exit__ = mock_exit
        
        dl.download_video("http://example.com", output_path)
        
        expected_archive = os.path.join(output_path, 'download_history.txt')
        if 'download_archive' in captured_opts:
            print(f"Success: download_archive set to: {captured_opts['download_archive']}")
            if captured_opts['download_archive'] == expected_archive:
                print("Path matches expected path.")
            else:
                print(f"FAIL: Path mismatch. Expected {expected_archive}")
        else:
            print("FAIL: download_archive option not found.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Restore (though script ends anyway)
        yt_dlp.YoutubeDL.__init__ = original_init

if __name__ == "__main__":
    test_archive_option()
