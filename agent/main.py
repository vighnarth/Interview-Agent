"""
agent/main.py
LiveKit voice agent worker — livekit-agents v1.5.0 API.

Run with:
  python -m agent.main dev
"""
import os
import sys
import asyncio
import logging
import io
import wave
import numpy as np
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    NOT_GIVEN,
    NotGivenOr,
    DEFAULT_API_CONNECT_OPTIONS,
    APIConnectOptions,
)
from livekit.agents import llm, stt, tts
from livekit.agents.voice import Agent, AgentSession
from agent.retrieval import get_relevant_context
from agent.persona import build_system_prompt
from livekit.plugins import cartesia, openai, silero
from openai import AsyncOpenAI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("agent.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Custom Free Fallback: Edge-TTS (No Key, Unlimited)
# ---------------------------------------------------------------------------
class EdgeTTS(tts.TTS):
    def __init__(self, voice: str = "en-US-AvaMultilingualNeural"):
        super().__init__(
            capabilities=tts.TTSCapabilities(streaming=False),
            sample_rate=48000,
            num_channels=1
        )
        self._voice = voice

    def synthesize(self, text: str) -> tts.SynthesizeStream:
        return EdgeSynthesizeStream(tts=self, text=text, voice=self._voice)

class EdgeSynthesizeStream(tts.SynthesizeStream):
    def __init__(self, tts: tts.TTS, text: str, voice: str):
        super().__init__(tts=tts, conn_options=DEFAULT_API_CONNECT_OPTIONS)
        self._text = text
        self._voice = voice

    async def _run(self):
        import io
        import av
        import edge_tts
        from livekit import rtc
        
        try:
            communicate = edge_tts.Communicate(self._text, self._voice)
            mp3_buffer = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    mp3_buffer.write(chunk["data"])
            
            mp3_buffer.seek(0)
            if mp3_buffer.getbuffer().nbytes == 0:
                return

            container = av.open(mp3_buffer)
            resampler = av.AudioResampler(format='s16', layout='mono', rate=48000)
            
            for frame in container.decode(audio=0):
                for resampled_frame in resampler.resample(frame):
                    self._event_ch.send_nowait(tts.SynthesizeEvent(
                        type=tts.SynthesizeEventType.AUDIO,
                        audio=rtc.AudioFrame(
                            data=resampled_frame.to_ndarray().tobytes(),
                            sample_rate=48000,
                            num_channels=1,
                            samples_per_channel=resampled_frame.samples
                        )
                    ))
            
            # Flush resampler
            for resampled_frame in resampler.resample(None):
                self._event_ch.send_nowait(tts.SynthesizeEvent(
                    type=tts.SynthesizeEventType.AUDIO,
                    audio=rtc.AudioFrame(
                        data=resampled_frame.to_ndarray().tobytes(),
                        sample_rate=48000,
                        num_channels=1,
                        samples_per_channel=resampled_frame.samples
                    )
                ))
        except Exception as e:
            logger.error(f"[EdgeTTS] Error synthesizing: {e}")
        finally:
            self._event_ch.send_nowait(tts.SynthesizeEvent(type=tts.SynthesizeEventType.FINISHED))


# ---------------------------------------------------------------------------
# Native Groq Client for official plugins
# ---------------------------------------------------------------------------
def get_groq_client():
    return AsyncOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get("GROQ_API_KEY")
    )


# ---------------------------------------------------------------------------
# Agent entrypoint
# ---------------------------------------------------------------------------

async def entrypoint(ctx: JobContext):
    logger.info(f"[Agent] Connecting to room: {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Use a default friendly female voice if none is provided via env var
    cartesia_voice = os.getenv("CARTESIA_VOICE_ID", "248be419-c632-4f23-adf1-5324ed7dbf1d")
    cartesia_dict = os.getenv("CARTESIA_DICT_ID") # Optional Pronunciation Dictionary
    
    client = get_groq_client()
    
    # Primary: Cartesia (Clone)
    # Fallback: Edge-TTS (Free & Unlimited)
    primary_tts = cartesia.TTS(voice=cartesia_voice, pronunciation_dict_id=cartesia_dict)
    fallback_tts = EdgeTTS()

    session = AgentSession(
        stt=openai.STT(model="whisper-large-v3", client=client),
        llm=openai.LLM(model="llama-3.1-8b-instant", client=client),
        tts=tts.FallbackAdapter([primary_tts, fallback_tts]),
        vad=silero.VAD.load(),
    )

    # Note: RAG can be injected via chat_ctx.messages in entrypoint or a hook
    # But for a simple job-interview twin, we build the system prompt here.
    context = get_relevant_context("Vighnarth Nile profile background research agentic workflows Sankey Solutions")
    system_prompt = build_system_prompt(context)

    agent = Agent(
        instructions=system_prompt + "\n\nCRITICAL behavioral rules:"
                                     "\n- Keep answers concise (max 3 sentences)."
                                     "\n- Do NOT correct the interviewer if they mispronounce your name (Vighnarth)."
                                     "\n- Be honest and professional as Vighnarth."
    )

    await session.start(agent, room=ctx.room)

    @ctx.room.on("data_received")
    def on_data_received(data_packet: rtc.DataPacket):
        # Log every single packet for debugging
        logger.info(f"[Agent] Packet received! Size: {len(data_packet.data)} bytes")
        
        try:
            import json
            payload = json.loads(data_packet.data)
            logger.info(f"[Agent] Payload: {payload}")
            
            if payload.get("type") == "question":
                text = payload.get("text")
                logger.info(f"[Agent] Intercepted UI question: {text}")
                # Use generate_reply to force the agent to respond
                session.generate_reply(user_input=text)
        except Exception as e:
            logger.error(f"[Agent] Error in data handler: {e}")

    await session.say(
        "Hi! I'm Vighnarth. Great to meet you — I'm looking forward to this conversation. Go ahead!",
        allow_interruptions=True,
    )

    logger.info("[Agent] Ready and listening.")
    await asyncio.sleep(3600)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(
        entrypoint_fnc=entrypoint,
        agent_name="interview-agent",  # Must match AGENT_NAME in token_server.py
    ))
