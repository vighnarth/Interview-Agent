"""
agent/pipeline.py
Orchestrates the LLM response pipeline:
  1. Retrieve relevant context from ChromaDB via RAG
  2. Build system prompt from persona.py
  3. Stream response from Groq (llama-3.3-70b-versatile)
"""
import os
from groq import AsyncGroq
from dotenv import load_dotenv
from agent.retrieval import get_relevant_context
from agent.persona import build_system_prompt

load_dotenv()

MODEL = "llama-3.3-70b-versatile"  # Best Groq model for instruction following + speed


async def generate_response(user_message: str) -> str:
    """
    Full pipeline: RAG → prompt → LLM.
    Returns the complete response string (non-streaming, for eval/testing).
    """
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

    context = get_relevant_context(user_message)
    system_prompt = build_system_prompt(context)

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
        max_tokens=400,
    )
    return response.choices[0].message.content


async def stream_response(user_message: str, chat_history: list[dict] | None = None):
    """
    Streaming pipeline for LiveKit voice agent.
    Yields text chunks as they arrive from Groq.
    chat_history: list of {"role": "user"/"assistant", "content": "..."} dicts
    """
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

    context = get_relevant_context(user_message)
    system_prompt = build_system_prompt(context)

    messages = [{"role": "system", "content": system_prompt}]
    if chat_history:
        messages.extend(chat_history)
    messages.append({"role": "user", "content": user_message})

    stream = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=400,
        stream=True
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


if __name__ == "__main__":
    import asyncio

    async def _test():
        print("Testing pipeline...\n")
        resp = await generate_response("Tell me about yourself and your background.")
        print(resp)

    asyncio.run(_test())
