<h1 align="center">JARVIS — AI Voice Assistant</h1>

<p align="center">
  Voice-activated assistant powered by OpenAI and Google Gemini.<br>
  Wake word detection, realtime audio, function calling, and more.
</p>

---

## How It Works

You say **"Hey Jarvis"** → the assistant wakes up, listens to your question, thinks, and responds with voice. Depending on which project you run, it can also search the web, check weather, control lights, or use a camera.

All projects use [OpenWakeWord](https://github.com/dscripka/openWakeWord) for hands-free wake word detection.

---

## Projects

### `OpenAI/GPT-Jarvis` — Full Voice Assistant

The main project. A complete loop: **wake word → record → transcribe → think → speak**.

- Configurable via `config.json` (model, voice, thresholds, prompts — no code changes needed)
- Camera/vision support in the code (disabled by default — uncomment the capture command for your OS)
- Conversation history saved between cycles
- Cross-platform audio recording via [SoX](https://sox.sourceforge.net/)

```bash
pip install openai sounddevice numpy openwakeword
# + install SoX: brew install sox (macOS) / apt install sox (Linux)
python OpenAI/GPT-Jarvis/main.py
```

### `OpenAI/GPT-Jarvis Realtime` — Low-Latency Voice via WebSocket

Uses OpenAI's **Realtime API** for continuous, low-latency conversation over WebSocket. No recording/transcribing steps — audio streams directly to the model and back.

- Server-side voice activity detection (VAD) — no manual push-to-talk
- Auto-mutes mic while the assistant speaks (prevents echo loops)
- Says "bye" → connection closes automatically

```bash
pip install websocket-client sounddevice numpy openwakeword certifi
python "OpenAI/GPT-Jarvis Realtime/main.py"
```

### `Google/Realtime` — Gemini Live API Voice Assistant

The most feature-rich project. Uses Google's **Gemini models** with native audio streaming.

- **Function calling** — weather (via [Open-Meteo](https://open-meteo.com/)), smart lights
- **Google Search** — built-in tool, model can search the web mid-conversation
- **Thinking mode** — configurable depth (`minimal` / `low` / `medium` / `high`)
- **Affective dialog** — adapts tone to match how you sound
- **Session resumption** — reconnects and remembers context for up to 2 hours
- **Context compression** — sliding window so the session never dies from token limits

```bash
pip install google-genai pyaudio numpy openwakeword requests
python Google/Realtime/main.py
```

> `old.py` is an earlier, simpler version without tools or advanced config — useful as a starting point.

### `OpenAI/GPT-STT` — Speech-to-Text

Transcribes an audio file using Whisper. Drop in an `audio.mp3` and run it.

```bash
pip install openai
python OpenAI/GPT-STT/STT.py
```

### `OpenAI/GPT-Text` — Text Chatbot

Minimal interactive chatbot in the terminal. Good for testing the API or as a starting template.

```bash
pip install openai
python OpenAI/GPT-Text/main.py
```

---

## Setup

**1.** Clone the repo:
```bash
git clone https://github.com/podieos/jarvis_assistant.git
cd jarvis_assistant
```

**2.** Get your API key:

| Provider | Link |
|---|---|
| OpenAI | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| Google | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |

**3.** Replace `"API_KEY"` in the source code or config file with your actual key.

**4.** Install dependencies for the project you want to run (see commands above) and start it.

---

## Repo Structure

```
├── OpenAI/
│   ├── GPT-Jarvis/              # Full pipeline: wake → record → STT → LLM → TTS
│   │   ├── main.py
│   │   ├── config.json          # All settings in one place
│   │   ├── generate_yes.py      # Generate confirmation sound
│   │   └── history.json         # Conversation log
│   ├── GPT-Jarvis Realtime/     # WebSocket streaming voice
│   │   └── main.py
│   ├── GPT-STT/                 # Whisper transcription
│   │   └── STT.py
│   └── GPT-Text/                # Terminal chatbot
│       └── main.py
└── Google/
    └── Realtime/                # Gemini Live API
        ├── main.py              # Full version with tools & session mgmt
        └── old.py               # Simple version
```
