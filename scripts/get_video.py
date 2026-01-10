import urllib.request
import os

video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
filename = "my_video.mp4"

try:
    urllib.request.urlretrieve(video_url, filename)
    
    file_size = os.path.getsize(filename) / 1024 / 1024
    print(f"✅ Success! Video saved as '{filename}'")
    print(f"   Size: {file_size:.2f} MB")
    
except Exception as e:
    print(f"❌ Error downloading video: {e}")