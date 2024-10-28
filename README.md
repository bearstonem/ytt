# YouTube Transcriber

A Python application that downloads YouTube videos, transcribes them using Groq's Whisper model, and provides summaries using Cerebras LLM.

## Features

- Download YouTube videos
- Extract and process audio
- Speed up audio for faster processing
- Transcribe audio using Groq's Whisper model
- Generate summaries using Cerebras LLM
- REST API endpoints for video processing
- Web interface support via CORS

## Prerequisites

- Python 3.8 or higher
- FFmpeg
- yt-dlp
- Poetry (Python package manager)
- Groq API key
- Cerebras API key

## Installation

### Quick Install

#### Windows

Run the setup script (requires administrator privileges):
```powershell
.\setup.ps1
```

#### Linux/MacOS

Make the setup script executable and run it with sudo:
```bash
chmod +x setup.sh
sudo ./setup.sh
```

### Manual Installation

1. Install FFmpeg and yt-dlp:

   Windows:
   ```powershell
   choco install ffmpeg
   choco install yt-dlp
   ```

   Ubuntu/Debian:
   ```bash
   sudo apt-get install ffmpeg python3-pip
   sudo pip3 install --upgrade yt-dlp
   ```

   MacOS:
   ```bash
   brew install ffmpeg
   brew install yt-dlp
   ```

2. Install Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install project dependencies:
   ```bash
   poetry install
   ```

4. (Optional) Install as a System Service:

   Windows:
   ```powershell
   # Run as Administrator
   .\install_service.bat
   ```

   Linux:
   ```bash
   sudo ./install_service_linux.sh
   ```

## Configuration

1. Create a `.env` file in the project root or rename `.env.example` to `.env` and fill in the values:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   CEREBRAS_API_KEY=your_cerebras_api_key_here
   ```

## Usage

### CLI Mode
```bash
poetry run python app.py "https://youtube.com/watch?v=your_video_id"
```

### Server Mode

#### Running Directly
```bash
poetry run python server.py
```

#### Using System Service

Windows:
```powershell
# Start service
net start YTTranscriberService

# Stop service
net stop YTTranscriberService

# Restart service
.\restart_service.bat
```

Linux:
```bash
# Start service
sudo systemctl start youtube-transcriber

# Stop service
sudo systemctl stop youtube-transcriber

# Restart service
sudo systemctl restart youtube-transcriber

# View service status
sudo systemctl status youtube-transcriber

# View logs
sudo journalctl -u youtube-transcriber
```

The server will start on port 5000 with the following endpoints:

- POST `/download`: Download a YouTube video
  ```json
  {
    "url": "https://youtube.com/watch?v=your_video_id"
  }
  ```

- POST `/transcribe`: Transcribe and summarize a YouTube video
  ```json
  {
    "url": "https://youtube.com/watch?v=your_video_id",
    "speed_factor": 2.0
  }
  ```

## Project Structure
youtube-transcriber/
├── app.py                    # CLI application
├── server.py                 # Flask server
├── setup.sh                  # Linux/MacOS setup script
├── setup.ps1                 # Windows setup script
├── install_service.bat       # Windows service installer
├── install_service_linux.sh  # Linux service installer
├── restart_service.bat       # Windows service restart utility
├── youtube-transcriber.service # Linux systemd service configuration
├── pyproject.toml           # Poetry configuration
├── .env                     # Environment variables
└── README.md               # This file

## Development

1. Install development dependencies:
   ```bash
   poetry install --with dev
   ```

2. Run tests:
   ```bash
   poetry run pytest
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. FFmpeg not found:
   - Ensure FFmpeg is installed and available in your system PATH
   - Try reinstalling FFmpeg using your package manager

2. yt-dlp errors:
   - Update yt-dlp to the latest version:
     ```bash
     pip install --upgrade yt-dlp
     ```

3. API Key Issues:
   - Verify your API keys are correctly set in the .env file
   - Ensure the .env file is in the project root directory

4. Service Installation Issues:

   Windows:
   - Ensure you're running the installation scripts as Administrator
   - Check the service logs in `C:\ProgramData\YTTranscriber\logs\service.log`
   - Use Event Viewer to check for service-related errors

   Linux:
   - Check service status: `sudo systemctl status youtube-transcriber`
   - View service logs: `sudo journalctl -u youtube-transcriber`
   - Verify permissions in `/opt/youtube-transcriber`

### Getting Help

If you encounter any issues:
1. Check the error messages in the console
2. Verify all prerequisites are installed
3. Ensure all environment variables are set correctly
4. Check the project's issue tracker for similar problems

## Security Notes

- Keep your API keys secure and never commit them to version control
- Use environment variables for sensitive configuration
- Regularly update dependencies to patch security vulnerabilities