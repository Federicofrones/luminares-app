const express = require('express');
const cors = require('cors');
const { EdgeTTS } = require('node-edge-tts');
const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid'); // Install uuid to avoid file collisions

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.static('public'));

// Ensure temp directory exists
const tempDir = path.join(__dirname, 'temp_audio');
if (!fs.existsSync(tempDir)) {
    fs.mkdirSync(tempDir);
}

// Helper: Split text into chunks
const MAX_CHUNK_LENGTH = 2000;

function splitTextIntoChunks(text) {
    const chunks = [];
    let currentChunk = '';
    const sentences = text.match(/[^.!?]+[.!?]+[\])'"`’”]*|.+/g) || [text];

    for (const sentence of sentences) {
        if (currentChunk.length + sentence.length <= MAX_CHUNK_LENGTH) {
            currentChunk += sentence;
        } else {
            if (sentence.length > MAX_CHUNK_LENGTH) {
                const words = sentence.split(' ');
                for (const word of words) {
                    if (currentChunk.length + word.length + 1 <= MAX_CHUNK_LENGTH) {
                        currentChunk += (currentChunk.length > 0 ? ' ' : '') + word;
                    } else {
                        if (currentChunk) chunks.push(currentChunk.trim());
                        currentChunk = word;
                    }
                }
            } else {
                chunks.push(currentChunk.trim());
                currentChunk = sentence;
            }
        }
    }
    if (currentChunk) chunks.push(currentChunk.trim());
    return chunks;
}

// Helper: generate a single chunk with retries
async function generateChunkWithRetry(tts, chunkText, filePath, maxRetries = 3) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            await tts.ttsPromise(chunkText, filePath);
            return fs.readFileSync(filePath);
        } catch (err) {
            console.warn(`  Attempt ${attempt}/${maxRetries} failed: ${err.message}`);
            // Clean up partial file if it exists
            if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
            if (attempt === maxRetries) throw err;
            // Wait a bit before retrying
            await new Promise(r => setTimeout(r, 2000 * attempt));
        } finally {
            if (fs.existsSync(filePath)) {
                try { fs.unlinkSync(filePath); } catch (_) { }
            }
        }
    }
}

app.post('/api/generate-tts', async (req, res) => {
    // Disable request timeout for long generations
    req.setTimeout(0);
    res.setTimeout(0);

    try {
        const { text, voice = 'es-MX-JorgeNeural' } = req.body;

        if (!text || text.trim() === '') {
            return res.status(400).json({ error: 'Text is required' });
        }

        const chunks = splitTextIntoChunks(text);
        console.log(`Split text into ${chunks.length} chunks. Using voice: ${voice} | Pitch: -11% | Rate: -14%`);

        const audioBuffers = [];
        const sessionId = Date.now().toString() + '_' + Math.floor(Math.random() * 10000);

        // Process sequentially with retry logic
        for (let i = 0; i < chunks.length; i++) {
            console.log(`Generating chunk ${i + 1}/${chunks.length} (${chunks[i].length} chars)...`);
            const tempFilePath = path.join(tempDir, `chunk_${sessionId}_${i}.mp3`);

            // Create a fresh TTS instance per chunk to avoid stale connections
            const tts = new EdgeTTS({
                voice: voice,
                lang: voice.substring(0, 5),
                outputFormat: 'audio-24khz-96kbitrate-mono-mp3',
                pitch: '-11%',
                rate: '-14%',
                timeout: 120000 // 2 minutes per chunk
            });

            const buffer = await generateChunkWithRetry(tts, chunks[i], tempFilePath);
            audioBuffers.push(buffer);
        }

        // Concatenate all MP3 buffers
        const finalBuffer = Buffer.concat(audioBuffers);

        // Send back
        res.set('Content-Type', 'audio/mpeg');
        res.set('Content-Disposition', 'attachment; filename="horror_story.mp3"');
        res.send(finalBuffer);

        console.log('Successfully generated cinematic audio!');

    } catch (error) {
        console.error('TTS Generation Error:', error);
        if (!res.headersSent) {
            res.status(500).json({
                error: 'Failed to generate audio',
                details: error.message
            });
        }
    }
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
