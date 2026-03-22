# Behavioral Stories (STAR Format)

## Story 1: Handling Technical Roadblocks in Agentic Systems

**Situation**: During the development of the Smart City Dashboard, I encountered significant latency issues when orchestrating real-time communication between multiple specialized agents.

**Task**: Optimize the multi-agent framework to ensure sub-second response times for incident reporting and emergency alerts.

**Action**:
1. Analyzed the communication overhead and identified that the initial linear chain was a bottleneck.
2. Shifted the architecture to a state-aware multi-agent system using LangGraph.
3. Replaced slow components with the Groq API for faster LLM inference and optimized routing calls through the OSRM API.
4. Implemented error handling for module and server connection errors to ensure backend stability.

**Result**: Reduced incident logging latency significantly. The system now autonomously handles traffic and weather triggers with a robust, fault-tolerant backbone.

**What I learned**: When building complex AI systems, the orchestration framework is just as important as the model itself.

---

## Story 2: Defending Technical Choices with Data

**Situation**: During my Sankey Solutions internship, there was a discussion about using traditional OCR versus a more streamlined RAG-based approach for document verification.

**Task**: Prove that a RAG-based multi-agent orchestration would be more reliable and faster for enterprise HR benchmarks.

**Action**: I developed a proof-of-concept using ChromaDB and SQLite to manage user states and policy retrieval. I ran evaluations by fine-tuning hyperparameters and validating agentic outputs against real HR datasets to demonstrate production-level reliability.

**Result**: The RAG-driven approach was adopted, reducing manual processing latency and ensuring higher execution correctness.

**What I learned**: In AI engineering, validation against real-world benchmarks is the only way to prove a system's value.

---

## Story 3: Leading Technical Execution under Pressure

**Situation**: I was the lead author for a research paper on AI-based skill gap analysis while simultaneously developing the SkillBridgeAI platform.

**Task**: Complete the development of the matching engine and prepare the research findings for the IEEE ASIANCON 2025 conference.

**Action**: I balanced the engineering of the FAISS-based semantic similarity engine with the rigorous academic writing required for the publication. I ensured the platform’s results were grounded in data that could withstand peer review at a major conference.

**Result**: The paper was successfully presented at IEEE ASIANCON 2025, and the platform successfully implemented real-time job market insights.

**What I learned**: Technical leadership requires bridging the gap between innovative research and functional, scalable code.

---

## Story 4: Learning and Applying New Infrastructures Rapidly

**Situation**: For the Smart City project, I needed to integrate advanced geospatial routing and weather decision engines, which were new areas for me.

**Task**: Master the OSRM API and ArcGIS routing algorithms within the project timeline.

**Action**: I spent a week diving into the OSRM documentation and ArcGIS API keys. I built a prototype for traffic agent optimization and integrated it into the FastAPI backend. I documented the routing logic to ensure system interoperability.

**Result**: Successfully implemented a Weather Decision Engine that triggers emergency alerts via webhooks, now a core feature of the dashboard.

**What I learned**: High-speed learning is a prerequisite for AI engineers. The ability to pivot to new APIs and frameworks is what allows for true system innovation.