import { v4 as uuidv4 } from 'https://esm.sh/uuid';

const BASE_PATH = window.appConfig?.BASE_PATH;

const doSynthesis = true;
const vadEnabled = true;
const volumeThreshold = 20;
const startThreshold = 5000;
const silenceThreshold = 2000;
const maxRecordingDuration = 15000;

const startBtn = document.getElementById('startBtn');
const transcriptDisplay = document.getElementById('transcript');
const statusDisplay = document.getElementById('status');

startBtn.onclick = async () => {
    startBtn.disabled = true;
    startBtn.innerText = '🔄 Listening...';
    transcriptDisplay.innerText = '';

    await startVoiceLoop();

    startBtn.disabled = false;
    startBtn.innerText = '▶️ Start Conversation';
};

async function startVoiceLoop() {
    const sessionId = uuidv4();

    while (true) {
        statusDisplay.innerText = '🎤 Waiting for speech...';

        const audioBlob = vadEnabled ? await recordAudioWithVAD() : await recordAudio(5000);
        if (audioBlob?.size == 0) {
            statusDisplay.innerText = '🤔 No speech detected';
            break;
        }

        const base64Audio = await blobToBase64(audioBlob);

        const data = await queryBot(sessionId, base64Audio);

        const bot_text = data.bot_text || '🤔 No response';
        transcriptDisplay.innerText = bot_text;

        if (data.bot_audio) {
            statusDisplay.innerText = '🤖 Bot Speaking...';
            await playBase64Audio(data.bot_audio);
        }

        if (!data.flow_active) {
            statusDisplay.innerText = '✅ Conversation complete';
            break;
        }

        statusDisplay.innerText = '🔁 Listening again...';
    }
}

async function queryBot(sessionId, base64Audio) {
    statusDisplay.innerText = '⏳ Querying the Bot...';

    const response = await fetch(BASE_PATH + '/bot/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, user_audio: base64Audio, do_synthesis: doSynthesis })
    });

    return await response.json();
}

function recordAudio(duration = 5000) {
    return new Promise(async (resolve) => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        const chunks = [];

        mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
        mediaRecorder.onstop = () => {
            const blob = new Blob(chunks, { type: 'audio/wav' });
            resolve(blob);
        };

        statusDisplay.innerText = '🎤 Recording...';

        mediaRecorder.start();
        setTimeout(() => mediaRecorder.stop(), duration);
    });
}
function recordAudioWithVAD() {
    return new Promise(async (resolve) => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        const chunks = [];

        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const analyser = audioContext.createAnalyser();
        const microphone = audioContext.createMediaStreamSource(stream);

        analyser.fftSize = 512;
        analyser.smoothingTimeConstant = 0.8;
        microphone.connect(analyser);

        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        let isRecording = false;
        let recordingStart = 0;
        let silenceStart = 0;
        let timeoutId = null;
        let overallTimeoutId = null;

        function cleanup() {
            if (timeoutId) {
                clearTimeout(timeoutId);
            }
            if (overallTimeoutId) {
                clearTimeout(overallTimeoutId);
            }
            stream.getTracks().forEach(track => track.stop());
            audioContext.close();
        }

        overallTimeoutId = setTimeout(() => {
            statusDisplay.innerText = '⏰ No speech detected, timing out...';
            cleanup();
            resolve(new Blob([], { type: 'audio/wav' }));
        }, startThreshold);

        mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
        mediaRecorder.onstop = () => {
            const blob = new Blob(chunks, { type: 'audio/wav' });
            cleanup();
            resolve(blob);
        };

        function detectVoice() {
            analyser.getByteFrequencyData(dataArray);

            let sum = 0;
            for (let i = 0; i < bufferLength; i++) {
                sum += dataArray[i];
            }
            const average = sum / bufferLength;

            const currentTime = Date.now();

            if (average > volumeThreshold) {
                if (!isRecording) {
                    if (overallTimeoutId) {
                        clearTimeout(overallTimeoutId);
                        overallTimeoutId = null;
                    }

                    statusDisplay.innerText = '🎤 Recording speech...';
                    isRecording = true;
                    recordingStart = currentTime;
                    mediaRecorder.start();

                    timeoutId = setTimeout(() => {
                        statusDisplay.innerText = '⏰ Recording timeout reached...';
                        mediaRecorder.stop();
                    }, maxRecordingDuration);
                }
                silenceStart = currentTime;
            } else if (isRecording) {
                if (currentTime - silenceStart > silenceThreshold) {
                    statusDisplay.innerText = '⏹️ Stopping recording...';
                    mediaRecorder.stop();
                    return;
                }
            }

            if (isRecording && currentTime - recordingStart > maxRecordingDuration) {
                statusDisplay.innerText = '⏰ Maximum recording time reached...';
                mediaRecorder.stop();
                return;
            }

            requestAnimationFrame(detectVoice);
        }

        detectVoice();
    });
}

function blobToBase64(blob) {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result.split(',')[1]);
        reader.readAsDataURL(blob);
    });
}

function playBase64Audio(base64Audio) {
    return new Promise((resolve) => {
        const byteChars = atob(base64Audio);
        const byteNumbers = new Array(byteChars.length).fill(0).map((_, i) => byteChars.charCodeAt(i));
        const byteArray = new Uint8Array(byteNumbers);
        const audioBlob = new Blob([byteArray], { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.onended = resolve;
        audio.play();
    });
}
