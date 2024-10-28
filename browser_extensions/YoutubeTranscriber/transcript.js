// transcript.js
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const result = await browser.storage.local.get(['currentTranscript', 'currentSummary']);
        
        if (result.currentTranscript) {
            document.getElementById('transcript').textContent = result.currentTranscript;
        } else {
            document.getElementById('transcript').textContent = 'No transcript found.';
        }
        
        if (result.currentSummary) {
            // Use marked directly without checking for its existence
            const renderedContent = marked.parse(result.currentSummary);
            document.getElementById('summary').innerHTML = renderedContent;
        } else {
            document.getElementById('summary').textContent = 'No summary available.';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('transcript').textContent = 'Error loading content: ' + error.message;
        document.getElementById('summary').textContent = 'Error loading content: ' + error.message;
    }
});

document.getElementById('copyBtn').addEventListener('click', async () => {
    try {
        const result = await browser.storage.local.get(['currentTranscript', 'currentSummary']);
        const summary = result.currentSummary || document.getElementById('summary').textContent;
        const transcript = result.currentTranscript || document.getElementById('transcript').textContent;
        
        const fullText = `Summary:\n${summary}\n\nFull Transcript:\n${transcript}`;
        await navigator.clipboard.writeText(fullText);
        alert('Content copied to clipboard!');
    } catch (err) {
        alert('Failed to copy text: ' + err.message);
    }
});

document.getElementById('downloadBtn').addEventListener('click', async () => {
    try {
        const result = await browser.storage.local.get(['currentTranscript', 'currentSummary']);
        const summary = result.currentSummary || document.getElementById('summary').textContent;
        const transcript = result.currentTranscript || document.getElementById('transcript').textContent;
        
        const fullText = `Summary:\n${summary}\n\nFull Transcript:\n${transcript}`;
        const blob = new Blob([fullText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'transcript-with-summary.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (err) {
        alert('Failed to download: ' + err.message);
    }
});