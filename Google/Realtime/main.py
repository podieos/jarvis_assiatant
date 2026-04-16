import asyncio
import numpy as np
import pyaudio
from google import genai
from google.genai import types
from openwakeword.model import Model

import requests
from datetime import datetime

CLIENT = genai.Client(api_key="API_KEY", http_options={"api_version": "v1alpha"})
MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"
VOICE  = "Charon"

WAKE_WORD_MODEL = Model(wakeword_models=["hey_jarvis"], inference_framework="tflite")
WAKE_WORD_THRESHOLD = 0.5

total_tokens = 0
session_handle = None

tools = [
    # add "behavior": "NON_BLOCKING" to a function to run it async (model keeps talking while it runs)
    {"google_search": {}},
    {
        "function_declarations": [
            {
                "name": "set_lights",
                "description": "Turns lights on or off.",
                "behavior": "NON_BLOCKING", 
                "parameters": {
                    "type": "object",
                    "properties": {
                        "state": {"type": "string", "description": "on or off"}
                    },
                    "required": ["state"]
                }
            },
            {
                "name": "get_weather",
                "description": "Gets the current weather for a given city.",
                "behavior": "NON_BLOCKING", 
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "The city name."}
                    },
                    "required": ["city"]
                }
            }
        ]
    }
]


def build_config():
    PROMPT = f"""You are Jarvis, a sophisticated AI assistant inspired by Jarvis from Iron Man.
        Personality:
        - Address the user as "Sir" at all times
        - Be witty, calm, and slightly dry in humor — like the original Jarvis
        - Keep responses concise — you are a voice assistant, not a chatbot
        - Never use lists or bullet points in speech, speak naturally

        Context:
        - The user is located in Prague, Czech Republic
        - Use Celsius for temperature, metric for distances
        - Current date and time: {datetime.now().strftime("%Y-%m-%d %H:%M")}
        - Current date/time awareness: always consider the time of day in greetings

        Behavior:
        - For simple questions, be brief — one or two sentences
        - For complex topics, explain clearly but don't ramble
        - When using tools, briefly acknowledge what you're doing ("Checking the weather, Sir.")
        - If you don't know something, say so honestly with Jarvis-like charm

        When the conversation naturally concludes — such as the user saying goodbye, thanking you, indicating they're done, or there's nothing left to discuss — respond with [DONE] in your message.
    """
    return types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        output_audio_transcription=types.AudioTranscriptionConfig(),
        input_audio_transcription=types.AudioTranscriptionConfig(),
        system_instruction=PROMPT,
        tools=tools,
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=VOICE)
            )
        ),
        # "minimal" → fastest | "low" → better facts | "medium" → complex | "high" → deepest, slowest
        # include_thoughts=True → model sends a summary of what it was thinking before responding
        thinking_config=types.ThinkingConfig(
            thinking_level="minimal",
            include_thoughts=True,
        ),
        # model adapts its tone to match how you sound
        enable_affective_dialog=True,
        # model stays silent if input isn't directed at it
        proactivity=types.ProactivityConfig(
            proactive_audio=True
        ),
        # compresses old history so session never dies from the 15min/2min context limit
        context_window_compression=types.ContextWindowCompressionConfig(
            sliding_window=types.SlidingWindow(),
        ),
        # passes saved handle on reconnect so model remembers full history — valid for 2hr
        session_resumption=types.SessionResumptionConfig(
            handle=session_handle  # None = fresh session
        ),
        realtime_input_config=types.RealtimeInputConfig(
            # NO_INTERRUPTION → model finishes before processing new input (prevents self-hearing)
            # INTERRUPTION    → user can barge in at any time
            activity_handling=types.ActivityHandling.NO_INTERRUPTION,
            automatic_activity_detection=types.AutomaticActivityDetection(
                disabled=False,  # True = push-to-talk, send activityStart/activityEnd manually
                # HIGH → triggers easily | LOW → needs clear voice, fewer false triggers
                start_of_speech_sensitivity=types.StartSensitivity.START_SENSITIVITY_LOW,
                # HIGH → cuts off quickly | LOW → waits longer, allows mid-sentence pauses
                end_of_speech_sensitivity=types.EndSensitivity.END_SENSITIVITY_LOW,
                prefix_padding_ms=20,     # ms before speech start — increase if first word gets clipped
                silence_duration_ms=500,  # ms of silence to end turn — increase if model cuts you off
            ),
        ),
    )

def handle_function_call(name: str, args: dict) -> str:
    if name == "set_lights":
        print(f"Function: {name}")
        return f"Lights turned {args.get('state')}."
    
    elif name == "get_weather":
        city = args.get("city", "unknown")
        try:
            print(f"Function: {name}")
            geo = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1}, timeout=5).json()

            if not geo.get("results"):
                return f"City '{city}' not found."

            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]
            name_found = geo["results"][0]["name"]

            weather = requests.get("https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                }, timeout=5).json()

            cur = weather["current"]
            return (
                f"Weather in {name_found}: "
                f"{cur['temperature_2m']}°C, "
                f"humidity {cur['relative_humidity_2m']}%, "
                f"wind {cur['wind_speed_10m']} km/h, "
                f"code {cur['weather_code']}"
            )
        except Exception:
            return f"Failed to fetch weather for {city}."

    else:
        return f"Unknown function: {name}"


async def wake_word():
    WAKE_WORD_MODEL.reset()
    while True:
        chunk = await asyncio.to_thread(MICROPHONE.read, 1280, exception_on_overflow=False)
        audio_data = np.frombuffer(chunk, dtype=np.int16)
        predictions = await asyncio.to_thread(WAKE_WORD_MODEL.predict, audio_data)
        for score in predictions.values():
            if score >= WAKE_WORD_THRESHOLD:
                print("Wake word")
                return


async def send_audio(session, stop_event: asyncio.Event, turn_lock: asyncio.Lock):
    while not stop_event.is_set():
        chunk = await asyncio.to_thread(MICROPHONE.read, 1024, exception_on_overflow=False)
        if not turn_lock.locked():
            await session.send_realtime_input(
                audio=types.Blob(data=chunk, mime_type="audio/pcm;rate=16000")
            )


async def receive_responses(session, stop_event: asyncio.Event, turn_lock: asyncio.Lock):
    global total_tokens, session_handle
    transcript = []
    while True:
        async for response in session.receive():

            if response.usage_metadata:
                total_tokens = response.usage_metadata.total_token_count

            if response.session_resumption_update:
                update = response.session_resumption_update
                if update.resumable and update.new_handle:
                    session_handle = update.new_handle

            if response.go_away is not None:
                print(f"Connection closing in {response.go_away.time_left}")

            if response.tool_call:
                function_responses = []
                for fc in response.tool_call.function_calls:
                    result = await asyncio.to_thread(handle_function_call, fc.name, fc.args)
                    function_responses.append(types.FunctionResponse(
                        id=fc.id,
                        name=fc.name,
                        # response={"result": result}
                        
                        # for NON_BLOCKING functions set scheduling in the tool_call response:
                        #   "INTERRUPT" → announces result immediately | "WHEN_IDLE" → waits to finish | "SILENT" → absorbs silently
                        response={"result": result, "scheduling": "WHEN_IDLE"}
                    ))
                await session.send_tool_response(function_responses=function_responses)

            content = response.server_content
            if not content:
                continue

            if content.input_transcription:
                print(content.input_transcription.text, end="", flush=True)

            if content.output_transcription:
                transcript.append(content.output_transcription.text)
                print(content.output_transcription.text, end="", flush=True)

            if content.model_turn:
                for part in content.model_turn.parts:
                    if part.thought:
                        print(f"Thought {part.text}", flush=True)
                    elif part.inline_data:
                        async with turn_lock:
                            await asyncio.to_thread(SPEAKER.write, part.inline_data.data)

            if content.turn_complete:
                print(f"Tokens: {total_tokens}")
                print()
                if "[DONE]" in "".join(transcript).strip():
                    print("Stop")
                    stop_event.set()
                    return
                transcript = []
                break

async def main():
    global MICROPHONE, SPEAKER
    audio = pyaudio.PyAudio()
    MICROPHONE = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1280)
    SPEAKER    = audio.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    try:
        while True:
            print("Start")
            await wake_word()
            async with CLIENT.aio.live.connect(model=MODEL, config=build_config()) as session:
                print("Connected")
                stop_event = asyncio.Event()
                turn_lock  = asyncio.Lock()
                await asyncio.gather(
                    send_audio(session, stop_event, turn_lock),
                    receive_responses(session, stop_event, turn_lock),
                )
    finally:
        audio.terminate()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
