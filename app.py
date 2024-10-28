import os
import sys
import yt_dlp
import subprocess
from groq import Groq
import tempfile
from dotenv import load_dotenv

def download_youtube_audio(url, output_path):
    """Download audio from YouTube video."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': output_path,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return f"{output_path}.mp3"

def speed_up_audio(input_path, output_path, speed_factor=1.5):
    """Speed up audio using ffmpeg."""
    command = [
        'ffmpeg', '-i', input_path,
        '-filter:a', f'atempo={speed_factor}',
        '-ar', '16000',  # Set sample rate to 16kHz as required by Whisper
        '-ac', '1',      # Convert to mono
        '-y',            # Overwrite output file if exists
        output_path
    ]
    subprocess.run(command, check=True)

def transcribe_audio(audio_path, groq_api_key):
    """Transcribe audio using Groq API."""
    client = Groq(api_key=groq_api_key)
    
    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audio_path, file.read()),
            model="whisper-large-v3",
            response_format="text"
        )
    
    # The response is already a string when response_format="text"
    return transcription

def transcribe_youtube_video(video_url, groq_api_key, speed_factor=2.0):
    """Main function to handle the entire transcription process."""
    try:
        # Create temporary directory for audio files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download YouTube audio
            print("Downloading YouTube audio...")
            original_audio = download_youtube_audio(video_url, 
                                                 os.path.join(temp_dir, "audio"))
            
            # Speed up and process audio
            print(f"Processing audio (speed factor: {speed_factor}x)...")
            processed_audio = os.path.join(temp_dir, "processed_audio.mp3")
            speed_up_audio(original_audio, processed_audio, speed_factor)
            
            # Transcribe the processed audio
            print("Transcribing audio...")
            transcript = transcribe_audio(processed_audio, groq_api_key)
            
            return transcript
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <youtube_url>")
        sys.exit(1)

    # Load environment variables from .env file
    load_dotenv()
    
    VIDEO_URL = sys.argv[1]
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    
    if not GROQ_API_KEY:
        print("Please set the GROQ_API_KEY in your .env file")
        sys.exit(1)
    
    # Speed factor (1.0 = normal speed, 2.0 = double speed)
    SPEED_FACTOR = 2.0
    
    transcript = transcribe_youtube_video(VIDEO_URL, GROQ_API_KEY, SPEED_FACTOR)
    
    if transcript:
        print("\nTranscription:")
        print(transcript)
        
        # Save to file
        with open("transcript.txt", "w", encoding="utf-8") as f:
            f.write(transcript)
        print("\nTranscript saved to transcript.txt")