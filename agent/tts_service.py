"""
agent/tts_service.py
edge-tts wrapper — Microsoft neural voices, pure Python, free, Python 3.13 compatible.
No API key required. Uses Microsoft Azure TTS public endpoint.

Available voices for en-US (neural, natural quality):
  en-US-AriaNeural      — warm, natural female
  en-US-JennyNeural     — friendly female
  en-US-GuyNeural       — natural male
  en-US-AndrewNeural    — clear male (great for professional contexts)

To add voice cloning later: swap this module for Chatterbox TTS
once you have a voice sample recorded.
"""
import io
import asyncio
import edge_tts
import soundfile as sf
import numpy as np

DEFAULT_VOICE = "en-US-AriaNeural"   # Natural female voice, warm tone
SAMPLE_RATE = 24000


async def synthesize(text: str, voice: str = DEFAULT_VOICE) -> bytes:
    """
    Convert text to speech using Microsoft neural TTS via edge-tts.
    Returns WAV bytes (PCM 24kHz mono).
    """
    if not text or not text.strip():
        return b""

    communicate = edge_tts.Communicate(text, voice)

    # Collect all MP3 chunks
    mp3_chunks: list[bytes] = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            mp3_chunks.append(chunk["data"])

    if not mp3_chunks:
        return b""

    mp3_bytes = b"".join(mp3_chunks)

    # Convert MP3 → WAV using soundfile (via BytesIO)
    import tempfile, os
    # edge-tts returns MP3; soundfile can read it if libsndfile supports MP3
    # Safest approach: write to temp file and read back as WAV
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_mp3:
        tmp_mp3.write(mp3_bytes)
        tmp_mp3_path = tmp_mp3.name

    try:
        audio_data, orig_sr = sf.read(tmp_mp3_path, dtype="float32")
        # Resample to 24kHz if needed
        if orig_sr != SAMPLE_RATE:
            from scipy.signal import resample_poly
            from math import gcd
            g = gcd(SAMPLE_RATE, orig_sr)
            audio_data = resample_poly(audio_data, SAMPLE_RATE // g, orig_sr // g)
    except Exception:
        # soundfile may not support MP3 — use scipy.io.wavfile with pydub fallback
        audio_data, orig_sr = _mp3_to_numpy(mp3_bytes)
    finally:
        os.unlink(tmp_mp3_path)

    # Ensure mono
    if audio_data.ndim > 1:
        audio_data = audio_data[:, 0]

    # Write as WAV
    wav_buf = io.BytesIO()
    sf.write(wav_buf, audio_data, SAMPLE_RATE, format="WAV", subtype="PCM_16")
    wav_buf.seek(0)
    return wav_buf.read()


def _mp3_to_numpy(mp3_bytes: bytes) -> tuple[np.ndarray, int]:
    """Fallback MP3 → numpy using pydub (if available) or scipy."""
    try:
        from pydub import AudioSegment
        seg = AudioSegment.from_mp3(io.BytesIO(mp3_bytes))
        seg = seg.set_channels(1).set_frame_rate(SAMPLE_RATE)
        samples = np.array(seg.get_array_of_samples(), dtype=np.float32) / 32768.0
        return samples, SAMPLE_RATE
    except ImportError:
        raise RuntimeError(
            "Cannot decode MP3 audio. Install pydub: pip install pydub"
        )


async def synthesize_stream(text: str, voice: str = DEFAULT_VOICE):
    """
    Async generator that yields (mp3_chunk: bytes) as they arrive.
    Suitable for streaming TTS output without waiting for the full response.
    """
    communicate = edge_tts.Communicate(text, voice)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio" and chunk["data"]:
            yield chunk["data"]


if __name__ == "__main__":
    async def _test():
        print(f"Synthesizing with {DEFAULT_VOICE}...")
        wav = await synthesize(
            "Hi, I'm Divya Sharma. I'm an ML engineer with three years of experience. "
            "I really enjoy working on NLP and voice AI systems."
        )
        with open("test_output.wav", "wb") as f:
            f.write(wav)
        print(f"Saved test_output.wav ({len(wav):,} bytes)")

    asyncio.run(_test())
