"""
agent/stt_service.py
Groq Whisper STT wrapper — ultra-fast transcription via Groq API.
Uses whisper-large-v3-turbo for best speed/quality balance.
"""
import os
import io
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

MODEL = "whisper-large-v3-turbo"   # Faster than v3, nearly same accuracy


async def transcribe(audio_bytes: bytes, mime_type: str = "audio/wav") -> str:
    """
    Transcribe audio bytes to text using Groq Whisper.

    Args:
        audio_bytes: Raw audio bytes (WAV, WebM, MP3, etc.)
        mime_type: MIME type of the audio (default: audio/wav)

    Returns:
        Transcribed text string, or empty string on failure.
    """
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

    # Determine file extension from mime type
    ext_map = {
        "audio/wav": "audio.wav",
        "audio/webm": "audio.webm",
        "audio/mp3": "audio.mp3",
        "audio/mpeg": "audio.mp3",
        "audio/ogg": "audio.ogg",
        "audio/flac": "audio.flac",
    }
    filename = ext_map.get(mime_type, "audio.wav")

    try:
        transcription = await client.audio.transcriptions.create(
            file=(filename, io.BytesIO(audio_bytes), mime_type),
            model=MODEL,
            language="en",
            response_format="text",
        )
        return transcription.strip()
    except Exception as e:
        print(f"[STT] Transcription failed: {e}")
        return ""


if __name__ == "__main__":
    import asyncio

    async def _test():
        from agent.tts_service import synthesize
        # Round-trip test: synthesize something → transcribe it back
        print("Generating test audio...")
        wav = await synthesize("My name is Divya and I have three years of experience in machine learning.")
        print("Transcribing...")
        text = await transcribe(wav)
        print(f"Transcribed: {text}")

    asyncio.run(_test())
