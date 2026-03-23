"""
token_server.py
FastAPI server that:
  - Generates LiveKit JWT tokens manually via PyJWT
  - Dispatches the agent to the room via LiveKit API (required in v1.5.0)
  - Serves the frontend index.html (GET /)

Run with:
  python token_server.py
"""
import os
import time
import asyncio
from pathlib import Path
from dotenv import load_dotenv

import jwt  # PyJWT
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import subprocess
import sys
import signal

load_dotenv()

FRONTEND_DIR = Path(__file__).parent / "frontend"
AGENT_NAME = "interview-agent"  # Must match WorkerOptions(agent_name=...) in main.py

app = FastAPI(title="Interview Agent Token Server")


def _make_livekit_token(
    api_key: str,
    api_secret: str,
    room: str,
    identity: str,
    name: str = "Interviewer",
    ttl_seconds: int = 3600,
) -> str:
    """Generate a LiveKit-compatible JWT using PyJWT."""
    now = int(time.time())
    payload = {
        "iss": api_key,
        "sub": identity,
        "iat": now,
        "nbf": now,
        "exp": now + ttl_seconds,
        "name": name,
        "video": {
            "room": room,
            "roomJoin": True,
            "canPublish": True,
            "canSubscribe": True,
            "canPublishData": True,
        },
    }
    return jwt.encode(payload, api_secret, algorithm="HS256")


async def _dispatch_agent(room: str) -> bool:
    """
    Use LiveKit API to explicitly dispatch the agent to the room.
    Required in livekit-agents v1.5.0 — agents no longer auto-join.
    """
    import livekit.api as lkapi

    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    livekit_url = os.getenv("LIVEKIT_URL", "")

    # Convert wss:// to https:// for REST API
    http_url = livekit_url.replace("wss://", "https://").replace("ws://", "http://")

    try:
        async with lkapi.LiveKitAPI(url=http_url, api_key=api_key, api_secret=api_secret) as lk:
            dispatch = await lk.agent_dispatch.create_dispatch(
                lkapi.CreateAgentDispatchRequest(
                    agent_name=AGENT_NAME,
                    room=room,
                )
            )
        print(f"[Dispatch] Agent dispatched to room '{room}': {dispatch.agent_name}")
        return True
    except Exception as e:
        print(f"[Dispatch] Warning — could not dispatch agent: {e}")
        return False


@app.get("/token")
async def get_token(room: str = "interview-room", identity: str = "interviewer"):
    """Generate a LiveKit access token."""
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    livekit_url = os.getenv("LIVEKIT_URL", "")

    if not api_key or not api_secret:
        return JSONResponse(
            {"error": "LIVEKIT_API_KEY or LIVEKIT_API_SECRET not set in .env"},
            status_code=500,
        )

    try:
        token = _make_livekit_token(api_key=api_key, api_secret=api_secret,
                                     room=room, identity=identity)
        return JSONResponse({"token": token, "url": livekit_url, "room": room})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/dispatch")
async def dispatch(room: str = "interview-room"):
    """Explicitly dispatch the agent to the room after the frontend connects."""
    success = await _dispatch_agent(room)
    if success:
        return JSONResponse({"status": "dispatched"})
    return JSONResponse({"error": "Failed to dispatch agent"}, status_code=500)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_file = FRONTEND_DIR / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Frontend not found</h1>", status_code=404)


if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


if __name__ == "__main__":
    print("🚀 Starting Interview Suite...")
    
    # 1. Start the Agent Worker in the background
    # We use subprocess to keep it simple and separate from the FastAPI event loop
    # Write logs to a file for debugging
    log_file = open("agent.log", "w", encoding="utf-8")
    print("🤖 Starting Agent Worker (logging to agent.log)")
    agent_process = subprocess.Popen(
        [sys.executable, "-m", "agent.main", "start"],
        stdout=log_file,
        stderr=subprocess.STDOUT
    )

    def cleanup(signum, frame):
        print("\n🛑 Shutting down Interview Suite...")
        agent_process.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    print("🌐 Frontend:  http://localhost:8000/")
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")
    finally:
        agent_process.terminate()
