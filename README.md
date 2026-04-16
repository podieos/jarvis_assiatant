# AI Assistant Projects

A collection of AI-powered voice and text assistant projects built with OpenAI and Google Gemini APIs.

## Setup

All projects require an API key. Replace `"API_KEY"` in the source files or config with your actual key before running.

- **OpenAI projects**: Get your key at [platform.openai.com](https://platform.openai.com/)
- **Google projects**: Get your key at [aistudio.google.com](https://aistudio.google.com/)

---

## OpenAI

### GPT-Jarvis

A full-featured voice assistant with wake word detection ("Hey Jarvis"), speech-to-text, LLM responses, text-to-speech, and optional camera/vision support. Uses SoX for audio recording and OpenWakeWord for activation.

- **Config**: Edit `config.json` to set your API key, models, TTS voice, and other parameters.
- **Dependencies**: `openai`, `sounddevice`, `numpy`, `openwakeword`, SoX (system)
- **Run**: `python main.py`

**Files:**
| File | Description |
|---|---|
| `main.py` | Main assistant loop (wake word, record, STT, LLM, TTS) |
| `config.json` | All configuration (models, thresholds, prompts) |
| `generate_yes.py` | Generates a "Yes." confirmation audio clip |
| `history.json` | Conversation history (auto-managed) |

### GPT-Jarvis Realtime

A real-time voice assistant using OpenAI's Realtime API over WebSocket. Supports continuous conversation with server-side VAD (voice activity detection) and wake word activation.

- **Dependencies**: `websocket-client`, `sounddevice`, `numpy`, `openwakeword`, `certifi`
- **Run**: `python main.py`

### GPT-STT

A simple speech-to-text script using OpenAI's Whisper model.

- **Dependencies**: `openai`
- **Run**: `python STT.py` (expects an `audio.mp3` file in the same directory)

### GPT-Text

A minimal text-based chatbot using GPT-4o-mini.

- **Dependencies**: `openai`
- **Run**: `python main.py`

---

## Google

### Realtime

A real-time voice assistant using Google Gemini's Live API with native audio. Features wake word detection, function calling (weather, lights), Google Search integration, session resumption, and context window compression.

- **Model**: `gemini-2.5-flash-native-audio-preview`
- **Dependencies**: `google-genai`, `pyaudio`, `numpy`, `openwakeword`, `requests`
- **Run**: `python main.py`

**Files:**
| File | Description |
|---|---|
| `main.py` | Full-featured assistant with tools, thinking, and session resumption |
| `old.py` | Earlier, simpler version without tools or advanced config |

**Key features in `main.py`:**
- Wake word activation ("Hey Jarvis")
- Function calling (weather via Open-Meteo, smart lights)
- Google Search tool
- Thinking mode (configurable depth)
- Affective dialog (tone matching)
- Session resumption (2-hour memory)
- Context window compression (sliding window)
