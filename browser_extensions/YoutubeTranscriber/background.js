browser.runtime.onMessage.addListener(async (message) => {
  if (message.type === 'openTranscript') {
    // Store transcript first
    await browser.storage.local.set({ currentTranscript: message.transcript });
    
    // Then open window
    browser.windows.create({
      url: 'transcript.html',
      type: 'popup',
      width: 800,
      height: 600
    });
  }
  return true;
});