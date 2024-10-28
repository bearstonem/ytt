// popup.js
const GROQ_API_KEY = "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";
const SPEED_FACTOR = 2.0;

async function getYouTubeUrl() {
    const tabs = await browser.tabs.query({active: true, currentWindow: true});
    const url = tabs[0].url;
    
    if (!url.includes('youtube.com/watch')) {
        throw new Error('Please navigate to a YouTube video.');
    }
    return url;
}

function updateStatus(message) {
    document.getElementById('status').textContent = message;
}

document.getElementById('transcribe').addEventListener('click', async () => {
    const button = document.getElementById('transcribe');
    const downloadBtn = document.getElementById('downloadBtn');
    
    button.disabled = true;
    downloadBtn.disabled = true;
    updateStatus('Transcribing and generating summary...');
    
    try {
        const url = await getYouTubeUrl();
        
        const response = await fetch('http://localhost:5000/transcribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                api_key: GROQ_API_KEY,
                speed_factor: SPEED_FACTOR
            })
        });
        
        const data = await response.json();
        if (data.transcript) {
            updateStatus('Processing complete!');
            await browser.storage.local.set({
                currentTranscript: data.transcript,
                currentSummary: data.summary
            });
            await browser.runtime.sendMessage({
                type: 'openTranscript',
                transcript: data.transcript,
                summary: data.summary
            });
        } else {
            updateStatus('Processing failed: ' + data.error);
        }
    } catch (error) {
        updateStatus('Error: ' + error.message);
    } finally {
        button.disabled = false;
        downloadBtn.disabled = false;
    }
});

// Download button handler remains the same
document.getElementById('downloadBtn').addEventListener('click', async () => {
    const button = document.getElementById('downloadBtn');
    const transcribeBtn = document.getElementById('transcribe');
    
    button.disabled = true;
    transcribeBtn.disabled = true;
    updateStatus('Starting download...');
    
    try {
        const url = await getYouTubeUrl();
        
        const response = await fetch('http://localhost:5000/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url
            })
        });
        
        const data = await response.json();
        if (data.success) {
            updateStatus(data.message);
        } else {
            updateStatus('Download failed: ' + data.error);
        }
    } catch (error) {
        updateStatus('Error: ' + error.message);
    } finally {
        button.disabled = false;
        transcribeBtn.disabled = false;
    }
});