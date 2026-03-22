# Projects

## Project 1: Smart City Dashboard — Agentic Urban Management (2026)

**Context**: Urban monitoring systems are often fragmented, leading to delayed incident reporting. I am leading the development of a multi-agent system to orchestrate autonomous city monitoring and emergency response.

**What I built**:
- A Multi-Agent System using LangGraph to orchestrate specialized agents (Traffic, Weather, Incident Logging) for real-time autonomous monitoring.
- Integrated a Traffic Agent with OSRM API for route optimization and a Weather Decision Engine to trigger emergency alerts via automated webhooks.
- Built backend services using FastAPI to manage state-aware retrieval, ensuring data governance and fault tolerance across the ecosystem.

**Tech**: Python, LangGraph, FastAPI, OSRM API, ArcGIS, PostgreSQL.

**Outcome**: Currently in development as lead developer, focusing on high-fidelity monitoring and reducing manual latency in incident reporting.

**What was hard**: Ensuring state-aware retrieval across multiple agents while maintaining low-latency communication. Managing real-time data from disparate APIs (Weather and Traffic) required a robust orchestration layer to prevent race conditions.

**What I'd do differently**: I would invest more time in building a custom GeoJSON-based visualization layer earlier instead of relying strictly on external API overlays to improve dashboard performance.

---

## Project 2: AI/ML HR Onboarding Assistant (2025–2026)

**Context**: Manual employee onboarding at Sankey Solutions involved high latency in document verification and policy explanation.

**What I built**:
- A full-stack RAG-based onboarding assistant to automate document collection, verification, and policy support.
- Implemented a multi-agent orchestration framework using ChromaDB and SQLite for context-aware retrieval and automated email generation.
- Designed interactive frontend components in Streamlit to guide users through verification stages and policy quizzes.

**Tech**: Python, LangChain, Streamlit, ChromaDB, SQLite.

**Outcome**: Successfully architected HR workflows that reduced manual processing latency and ensured execution correctness through enterprise benchmarks.

**What was hard**: Fine-tuning hyperparameters to ensure agentic outputs met production-level reliability for sensitive HR documents. Validating the RAG pipeline's accuracy was critical to ensure users received the correct policy information.

**What I'd do differently**: I initially used OCR, but later realized the project would be more efficient by streamlining the document intake process and moving toward vector-based retrieval earlier.

---

## Project 3: SkillBridgeAI — AI Employment Platform (2025 — current)
A full-stack R&D platform that matches job seekers with opportunities using semantic similarity and vector embeddings (FAISS). I developed the AI-powered matching engine and skill-gap detection system, comparing candidate competencies with real-time job market requirements. This work led to my lead-authored research paper, "Real-time AI based skill gap analysis and adaptive career guidance," published and presented at the IEEE 5th ASIANCON 2025.

---

## Project 4: Edusphere — School Communication Portal (2023 — current)
Built a commercial website for Gayatri Vidyalaya to enhance school-student communication. Developed a responsive front-end with React and Tailwind CSS, featuring real-time data dashboards for 500+ students and faculty members supported by Firebase.