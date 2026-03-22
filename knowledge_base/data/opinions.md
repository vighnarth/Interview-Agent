# Technical Opinions

## RAG vs Fine-tuning

RAG is my default for production. Fine-tuning is often a "black box" that is expensive to update and difficult to audit. With RAG, the knowledge base remains transparent and updateable, which is critical for the source traceability I build into my systems. I only consider fine-tuning when a specific reasoning style or hyperparameter alignment is required for production-level reliability. Most teams underestimate the actual "hard parts" of RAG: chunking strategy, vector embedding quality, and managing state-aware retrieval.

## Agentic Workflows vs Linear Chains

I prioritize Agentic Workflows using multi-agent orchestration. Linear chains are too brittle for complex real-world tasks like urban monitoring or automated HR onboarding. Using frameworks like LangGraph allows for specialized agents—like a Weather Decision Engine or Traffic Agent—to coordinate autonomously, ensuring fault tolerance and superior decision-making. A system that can't reason through feedback loops isn't truly "intelligent".

## Python & FastAPI for AI Services

Python is non-negotiable for AI and ML work because the ecosystem for RAG and agentic frameworks is miles ahead of any other language. For the backend, I use FastAPI exclusively. Its native async support and type safety are essential when orchestrating real-time communication between multiple agents and external APIs like OSRM or ArcGIS.

## SQL vs Vector Databases

I believe in a hybrid approach. SQL (PostgreSQL/SQLite) is the backbone for structured state management, user data, and tracking system logs. However, for semantic similarity and high-dimensional profile analysis, Vector Databases like ChromaDB, Pinecone, or FAISS are mandatory. You can't build a modern matching engine or a policy-learning assistant without the power of vector embeddings.

## On LLMs in Production

The industry often misses that LLMs are probabilistic, not deterministic. In my work, I design for this by implementing execution correctness checks and validating agentic outputs against enterprise benchmarks. You must build systems that assume the model might hallucinate; this means integrating automated webhooks for emergency alerts and strict data governance to handle uncertainty safely.

## On Engineering Culture

I value technical rigor and high-fidelity documentation. My experience presenting research at IEEE ASIANCON taught me that the best engineering happens when you can bridge the gap between academic theory and practical, scalable code. I believe in proactive problem-solving—whether it's fixing module errors or optimizing routing algorithms—and a culture where performance is measured by reliability, not just speed.
