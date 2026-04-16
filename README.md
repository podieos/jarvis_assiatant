<p align="center">
  <img src="https://img.shields.io/badge/J.A.R.V.I.S.-AI%20Assistant-0A0A0A?style=for-the-badge&logo=openai&logoColor=white" alt="JARVIS AI Assistant" />
</p>

<h1 align="center">JARVIS AI Assistant</h1>

<p align="center">
  <em>A collection of AI-powered voice and text assistant projects inspired by Iron Man's JARVIS</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat-square&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Google-Gemini%202.5-4285F4?style=flat-square&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" />
</p>

---

## Overview

This repository contains multiple implementations of a voice-activated AI assistant, ranging from simple text chatbots to full-featured realtime voice assistants with wake word detection, function calling, and web search capabilities.

All projects use **"Hey Jarvis"** as the wake word via [OpenWakeWord](https://github.com/dscripka/openWakeWord).

---

## Quick Start

**1. Clone the repo**
```bash
git clone https://github.com/podieos/jarvis_assiatant.git
cd jarvis_assiatant
```

**2. Set your API key**

Replace `"API_KEY"` in the source files or config with your actual key:

| Provider | Where to get your key |
|---|---|
| OpenAI | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| Google | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |

**3. Install dependencies and run**
```bash
pip install -r requirements.txt  # or install per-project (see below)
python main.py
```

---

## Projects

### OpenAI

<details>
<summary><b>GPT-Jarvis</b> — Full voice assistant pipeline</summary>

<br>

The most complete OpenAI-based assistant. Chains together wake word detection, audio recording (via SoX), speech-to-text, LLM reasoning, and text-to-speech in a continuous loop. Includes optional camera/vision support.

```
OpenAI/GPT-Jarvis/
├── main.py            # Main assistant loop
├── config.json        # All settings (models, thresholds, prompts)
├── generate_yes.py    # Generates confirmation audio clip
└── history.json       # Conversation history (auto-managed)
```

**Dependencies**
```bash
pip install openai sounddevice numpy openwakeword
# System: SoX (brew install sox / apt install sox)
```

**Config highlights** (`config.json`):
- `API_KEY` — your OpenAI key
- `LLM_MODEL` — which model to use (default: `gpt-4o-mini`)
- `TTS_VOICE` — voice for speech output
- `THRESHOLD` — wake word sensitivity

</details>

<details>
<summary><b>GPT-Jarvis Realtime</b> — WebSocket-based realtime voice</summary>

<br>

Uses OpenAI's **Realtime API** over WebSocket for low-latency, continuous voice conversation. Server-side VAD handles turn detection automatically.

```
OpenAI/GPT-Jarvis Realtime/
└── main.py
```

**Dependencies**
```bash
pip install websocket-client sounddevice numpy openwakeword certifi
```

**Key features:**
- Direct WebSocket connection to OpenAI Realtime API
- Server-side Voice Activity Detection (VAD)
- Mic muting during assistant speech (prevents echo)
- Automatic conversation ending on "bye"

</details>

<details>
<summary><b>GPT-STT</b> — Speech-to-text with Whisper</summary>

<br>

A minimal script that transcribes audio files using OpenAI's Whisper model.

```
OpenAI/GPT-STT/
└── STT.py
```

```bash
pip install openai
python STT.py  # expects audio.mp3 in the same directory
```

</details>

<details>
<summary><b>GPT-Text</b> — Simple text chatbot</summary>

<br>

A minimal interactive chatbot using GPT-4o-mini. Good starting point for understanding the OpenAI API.

```
OpenAI/GPT-Text/
└── main.py
```

```bash
pip install openai
python main.py
```

</details>

---

### Google

<details open>
<summary><b>Gemini Realtime</b> — Advanced voice assistant with Gemini Live API</summary>

<br>

The most advanced project in the repo. Uses Google's **Gemini 2.5 Flash** with native audio for a realtime voice assistant featuring function calling, Google Search, thinking mode, and session persistence.

```
Google/Realtime/
├── main.py    # Full-featured assistant
└── old.py     # Earlier, simpler version
```

**Dependencies**
```bash
pip install google-genai pyaudio numpy openwakeword requests
```

**Features:**

| Feature | Description |
|---|---|
| Wake Word | "Hey Jarvis" via OpenWakeWord |
| Function Calling | Weather (Open-Meteo API), smart lights |
| Google Search | Built-in search tool |
| Thinking Mode | Configurable depth (minimal → high) |
| Affective Dialog | Matches your tone of voice |
| Session Resumption | 2-hour memory across reconnects |
| Context Compression | Sliding window prevents context overflow |
| Proactive Audio | Model stays silent if not addressed |

</details>

---

## Repository Structure

```
.
├── README.md
├── OpenAI/
│   ├── GPT-Jarvis/              # Full voice assistant pipeline
│   ├── GPT-Jarvis Realtime/     # WebSocket realtime voice
│   ├── GPT-STT/                 # Speech-to-text (Whisper)
│   └── GPT-Text/                # Simple text chatbot
└── Google/
    └── Realtime/                # Gemini Live API voice assistant
```

---

## `.gitignore`

This repo includes a `.gitignore` file that tells Git which files to **ignore** — meaning they won't be tracked or uploaded to GitHub, even if they exist on your computer. This is important for keeping secrets and junk out of your repo.

Here's what's excluded and why:

| Pattern | Why it's ignored |
|---|---|
| `.DS_Store` | macOS system file — irrelevant metadata |
| `api.txt` / `ApiKey.txt` / `*.env` | **API keys and secrets** — never push these to GitHub |
| `__pycache__/` / `*.pyc` | Python bytecode cache — auto-generated, not source code |
| `venv/` / `.venv/` | Virtual environments — large, machine-specific, recreated via `pip install` |
| `*.mp3` / `*.wav` / `*.jpg` | Temporary audio/image files generated at runtime |

> **Tip:** If you add your API key to a file like `api.txt` locally, Git will automatically ignore it thanks to this `.gitignore`. Your key stays on your machine and never gets pushed.

---

## Tech Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/PyAudio-FF6F00?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/WebSocket-010101?style=for-the-badge&logo=websocket&logoColor=white" />
</p>

---

<p align="center">
  <sub>Built with caffeine and curiosity</sub>
</p>
