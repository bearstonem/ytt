from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import yt_dlp
import subprocess
from groq import Groq
import tempfile
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Replace hardcoded API key with environment variable
CEREBRAS_API_KEY = os.getenv('CEREBRAS_API_KEY')

def summarize_transcript(transcript):
    """Summarize transcript and extract key points"""
    client = Cerebras(api_key=CEREBRAS_API_KEY)
    
    prompt = f"""Please analyze the following transcript and provide:
1. A concise summary (2-3 sentences)
2. 3-5 main key points
3. Main takeaway
4. When encountering contatent that is technical, speicific in detail, or instructional, please ensure to include and preserve all of the details and create list of this extracted knowledge from the content.

Transcript:
{transcript}"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3.1-70b",
    )
    
    return chat_completion.choices[0].message.content

def download_video(url, output_path):
    """Download video from YouTube."""
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info['title']

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
        '-ar', '16000',
        '-ac', '1',
        '-y',
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
    
    return transcription

def transcribe_youtube_video(video_url, groq_api_key, speed_factor=2.0):
    """Main function to handle the entire transcription process."""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            print("Downloading YouTube audio...")
            original_audio = download_youtube_audio(video_url, 
                                                 os.path.join(temp_dir, "audio"))
            
            print(f"Processing audio (speed factor: {speed_factor}x)...")
            processed_audio = os.path.join(temp_dir, "processed_audio.mp3")
            speed_up_audio(original_audio, processed_audio, speed_factor)
            
            print("Transcribing audio...")
            transcript = transcribe_audio(processed_audio, groq_api_key)
            
            print("Generating summary...")
            summary = summarize_transcript(transcript)
            
            return {
                'transcript': transcript,
                'summary': summary
            }
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

@app.route('/download', methods=['POST'])
def download_only():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400
        
    try:
        downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'YTTranscriber')
        os.makedirs(downloads_dir, exist_ok=True)
        
        output_template = os.path.join(downloads_dir, '%(title)s.%(ext)s')
        title = download_video(video_url, output_template)
        
        return jsonify({
            'success': True,
            'message': f'Video downloaded successfully to Downloads/YTTranscriber folder',
            'title': title
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.json
    video_url = data.get('url')
    groq_api_key = os.getenv('GROQ_API_KEY')  # Get from environment instead of request
    speed_factor = data.get('speed_factor', 2.0)
    
    result = transcribe_youtube_video(video_url, groq_api_key, speed_factor)
    
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Transcription failed'}), 400

if __name__ == '__main__':
    app.run(port=5000)