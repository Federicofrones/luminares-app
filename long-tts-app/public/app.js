document.addEventListener('DOMContentLoaded', () => {
    const storyText = document.getElementById('story-text');
    const charCount = document.getElementById('char-count');
    const voiceSelect = document.getElementById('voice-select');
    const generateBtn = document.getElementById('generate-btn');

    const progressBox = document.getElementById('progress-container');
    const resultBox = document.getElementById('result-container');
    const errorBox = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');

    const audioPlayer = document.getElementById('audio-player');
    const downloadLink = document.getElementById('download-link');

    // Update Character Count
    storyText.addEventListener('input', () => {
        const text = storyText.value;
        const length = text.length;
        // Chunk size in backend is 2000
        const chunks = Math.ceil(length / 2000);
        charCount.textContent = `${length.toLocaleString()} characters (approx. ${chunks} chunks) - True Crime Mode Active`;
    });

    // Handle Generation
    generateBtn.addEventListener('click', async () => {
        const text = storyText.value.trim();
        const voice = voiceSelect.value;

        if (!text) {
            showError('Please paste your story text first.');
            return;
        }

        // UI State: Loading
        hideError();
        resultBox.classList.add('hidden');
        progressBox.classList.remove('hidden');
        generateBtn.disabled = true;

        try {
            // 60-minute timeout for very long texts (full books)
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 60 * 60 * 1000);

            const response = await fetch('/api/generate-tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    voice: voice
                }),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Unknown error occurred on the server.');
            }

            // Get Audio Blob
            const blob = await response.blob();
            const audioUrl = URL.createObjectURL(blob);

            // UI State: Success
            audioPlayer.src = audioUrl;
            downloadLink.href = audioUrl;

            progressBox.classList.add('hidden');
            resultBox.classList.remove('hidden');

            audioPlayer.play(); // Auto-play!

        } catch (error) {
            console.error('Error:', error);
            showError('Generation failed. ' + error.message);
            progressBox.classList.add('hidden');
        } finally {
            generateBtn.disabled = false;
        }
    });

    function showError(msg) {
        errorMessage.textContent = msg;
        errorBox.classList.remove('hidden');
    }

    function hideError() {
        errorBox.classList.add('hidden');
    }
});
