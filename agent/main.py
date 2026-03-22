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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Native Groq Client for official plugins
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
    
    client = get_groq_client()
    
    # We use official plugins pointing to Groq for maximum stability
    session = AgentSession(
        stt=openai.STT(model="whisper-large-v3", client=client),
        llm=openai.LLM(model="llama-3.3-70b-versatile", client=client),
        tts=cartesia.TTS(voice=cartesia_voice),
        vad=silero.VAD.load(),
    )

    # Note: RAG can be injected via chat_ctx.messages in entrypoint or a hook
    # But for a simple job-interview twin, we build the system prompt here.
    context = get_relevant_context("Vighnarth Nile profile background research agentic workflows Sankey Solutions")
    system_prompt = build_system_prompt(context)

    agent = Agent(
        instructions=system_prompt + "\n\nCRITICAL: Keep answers concise (3 sentences). Be honest as Vighnarth."
    )

    await session.start(agent, room=ctx.room)

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
