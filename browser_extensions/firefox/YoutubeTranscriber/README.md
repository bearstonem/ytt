# YouTube Transcriber Firefox Extension

A Firefox extension that allows you to easily extract and copy transcripts from YouTube videos.

## Features

- Extract transcripts from any YouTube video that has captions available
- Copy the entire transcript to clipboard with one click
- Clean, user-friendly interface
- Works with multiple languages (if available on the video)

## Installation Guide

### Method 1: Installing from Firefox Add-ons Store (Recommended)
1. Visit the Firefox Add-ons Store (link to be added when published)
2. Click on "Add to Firefox"
3. Click "Add" when prompted
4. The extension will be automatically installed and ready to use

### Method 2: Installing Temporarily for Development
1. Open Firefox browser
2. Type `about:debugging` in the URL bar
3. Click on "This Firefox" in the left sidebar
4. Click on "Load Temporary Add-on"
5. Navigate to your extension directory
6. Select the `manifest.json` file
7. The extension will be loaded temporarily (will be removed when Firefox is closed)

### Method 3: Installing from Source
1. Clone the repository:
   ```bash
   git clone [repository-url]
   ```
2. Open Firefox browser
3. Type `about:addons` in the URL bar
4. Click the gear icon and select "Install Add-on From File"
5. Navigate to the extension directory
6. Select the packaged `.xpi` file
7. Click "Add" when prompted

## Usage

1. Navigate to any YouTube video
2. Click on the YouTube Transcriber extension icon in your browser toolbar
3. If transcripts are available, they will be automatically loaded
4. Click the "Copy" button to copy the transcript to your clipboard

## Requirements

- Firefox Browser (Latest version recommended)
- YouTube video must have captions available

## Development

To contribute to the development:

1. Clone the repository
2. Make your changes
3. Test the extension using the temporary installation method
4. Submit a pull request

## Troubleshooting

- If the extension icon is not responding, refresh the YouTube page
- Ensure the video has captions available (check YouTube's CC button)
- Make sure you're on a valid YouTube video page

## Privacy

This extension:
- Only works on YouTube domains
- Does not collect any personal data
- Does not modify any video content
- Only accesses publicly available transcript data

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For issues and feature requests, please create an issue in the GitHub repository.
