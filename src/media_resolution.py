import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: Key not found. Check your .env file.")
    exit()

client = genai.Client(api_key=api_key)

def run_demo():
    # Upload files
    if not os.path.exists("../media/my_video.mp4"):
        print("❌ Error: my_video.mp4 not found. Run get_video.py first!")
        return

    video_file = client.files.upload(file="../media/my_video.mp4")

    if not os.path.exists("../media/my_image.png"):
        print("❌ Error: my_image.png not found.")
        return

    image_file = client.files.upload(file="../media/my_image.png")

    # Processing
    while video_file.state.name == "PROCESSING":
        time.sleep(2)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name != "ACTIVE":
        print("❌ Video processing failed.")
        return

    print("✅ Files ready. Asking Gemini...")

    # Media resolution low
    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=[
            "look at this image and find when in the video this scene occurs.",
            types.Part(
                file_data=types.FileData(
                    file_uri=image_file.uri,
                    mime_type=image_file.mime_type,
                ),
                media_resolution=types.PartMediaResolution(
                    level=types.PartMediaResolutionLevel.MEDIA_RESOLUTION_HIGH
                ),
            ),
            types.Part(
                file_data=types.FileData(
                    file_uri=video_file.uri,
                    mime_type=video_file.mime_type,
                ),
                media_resolution=types.PartMediaResolution(
                    level=types.PartMediaResolutionLevel.MEDIA_RESOLUTION_LOW
                ),
            ),
        ],
    )

    print("🤖 Gemini:\n", response.text)

if __name__ == "__main__":
    run_demo()
