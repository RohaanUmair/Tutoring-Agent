// src/web/static/js/voice-agent.js
class VoiceMathTutor {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.isSpeaking = false;
        
        this.initElements();
        this.initSpeechRecognition();
        this.setupEventListeners();
    }

    initElements() {
        this.chatMessages = document.getElementById('chatMessages');
        this.textInput = document.getElementById('textInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.voiceBtn = document.getElementById('voiceBtn');
        this.stopSpeakingBtn = document.getElementById('stopSpeakingBtn');
        this.status = document.getElementById('status');
    }

    initSpeechRecognition() {
        // Check browser support
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('Your browser doesn\'t support speech recognition. Please use Chrome or Edge.');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';

        this.recognition.onstart = () => {
            this.isListening = true;
            this.voiceBtn.classList.add('listening');
            this.updateStatus('Listening... Speak now!', 'listening');
        };

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            this.textInput.value = transcript;
            this.sendMessage(transcript);
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.updateStatus(`Error: ${event.error}`, 'error');
            this.stopListening();
        };

        this.recognition.onend = () => {
            this.stopListening();
        };
    }

    setupEventListeners() {
        // Send button
        this.sendBtn.addEventListener('click', () => {
            const message = this.textInput.value.trim();
            if (message) {
                this.sendMessage(message);
            }
        });

        // Enter key
        this.textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const message = this.textInput.value.trim();
                if (message) {
                    this.sendMessage(message);
                }
            }
        });

        // Voice button (hold to speak)
        this.voiceBtn.addEventListener('mousedown', () => this.startListening());
        this.voiceBtn.addEventListener('mouseup', () => this.stopListening());
        this.voiceBtn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.startListening();
        });
        this.voiceBtn.addEventListener('touchend', (e) => {
            e.preventDefault();
            this.stopListening();
        });

        // Stop speaking button
        this.stopSpeakingBtn.addEventListener('click', () => this.stopSpeaking());
    }

    startListening() {
        if (this.recognition && !this.isListening) {
            this.recognition.start();
        }
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
            this.isListening = false;
            this.voiceBtn.classList.remove('listening');
            this.updateStatus('');
        }
    }

    async sendMessage(message) {
        // Add user message
        this.addMessage(message, 'user');
        this.textInput.value = '';
        
        this.updateStatus('Thinking<span class="loading"></span>', 'processing');

        try {
            const response = await fetch('/api/agent/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            
            // Add agent response
            this.addMessage(data.text, 'agent');
            
            // Speak the response
            this.speak(data.speech_text);
            
            this.updateStatus('');
        } catch (error) {
            console.error('Error:', error);
            this.addMessage('Sorry, I encountered an error. Please try again.', 'agent');
            this.updateStatus('');
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = text;
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    speak(text) {
        // Stop any ongoing speech
        this.synthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        utterance.lang = 'en-US';

        utterance.onstart = () => {
            this.isSpeaking = true;
            this.stopSpeakingBtn.style.display = 'block';
            this.updateStatus('Speaking...', 'speaking');
        };

        utterance.onend = () => {
            this.isSpeaking = false;
            this.stopSpeakingBtn.style.display = 'none';
            this.updateStatus('');
        };

        this.synthesis.speak(utterance);
    }

    stopSpeaking() {
        this.synthesis.cancel();
        this.isSpeaking = false;
        this.stopSpeakingBtn.style.display = 'none';
        this.updateStatus('');
    }

    updateStatus(message, type = '') {
        this.status.innerHTML = message;
        this.status.className = `status ${type}`;
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    new VoiceMathTutor();
});