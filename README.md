# Interview Agent — Divya Sharma

A real-time voice agent that represents you as a candidate in interviews. The interviewer speaks, the agent hears, retrieves relevant knowledge about you from a RAG knowledge base, and speaks back in a natural voice.

## Tech Stack
- **Transport**: LiveKit (WebRTC)
- **VAD**: Silero (built into LiveKit)
- **STT**: Groq `whisper-large-v3-turbo`
- **LLM**: Groq `llama-3.3-70b-versatile`
- **RAG**: ChromaDB + `all-MiniLM-L6-v2` embeddings
- **TTS**: Kokoro TTS (Apache 2.0, free, runs on CPU)

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY, LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET
```

### 3. Ingest your knowledge base
```bash
python knowledge_base/ingest.py
```

### 4. Test the pipeline (no voice)
```bash
python -m eval.run_eval
```

### 5. Start the agent (two terminals)

**Terminal 1 — Token Server:**
```bash
python token_server.py
```

**Terminal 2 — LiveKit Worker:**
```bash
python -m agent.main start
```

**Browser:** Open http://localhost:8000 → Click "Start Interview"

## Customizing Your Persona
Edit the files in `knowledge_base/data/` with your real information, then re-run ingestion:
```bash
python knowledge_base/ingest.py
```

| File | Contents |
|---|---|
| `bio.md` | Your background, education, career timeline |
| `projects.md` | Project deep-dives with outcomes |
| `opinions.md` | Technical opinions and philosophy |
| `stories.md` | STAR-format behavioral stories |
| `skills.md` | Tech stack and proficiencies |

## Adding Your Voice (Optional)
See `voice_sample/README.md` for instructions on recording a voice clip and enabling Chatterbox TTS voice cloning.
