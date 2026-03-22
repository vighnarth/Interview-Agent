"""
agent/retrieval.py
Queries the ChromaDB persona collection to retrieve relevant context
for a given user query.
"""
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer

CHROMA_DIR = Path(__file__).parent.parent / "knowledge_base" / "chroma_db"
COLLECTION_NAME = "persona"
TOP_K = 4  # number of chunks to retrieve

# Lazy singletons — loaded once per process
_client = None
_collection = None
_model = None


def _load():
    global _client, _collection, _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    if _client is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _collection = _client.get_collection(COLLECTION_NAME)


def get_relevant_context(query: str) -> str:
    """
    Embed the query and return the top-K most relevant chunks
    from the persona knowledge base, formatted as a single string.
    """
    _load()
    embedding = _model.encode([query]).tolist()
    results = _collection.query(
        query_embeddings=embedding,
        n_results=TOP_K,
        include=["documents", "metadatas"],
    )
    if not results["documents"] or not results["documents"][0]:
        return ""

    chunks = results["documents"][0]
    sources = [m.get("source", "unknown") for m in results["metadatas"][0]]

    formatted = []
    for chunk, source in zip(chunks, sources):
        formatted.append(f"[From {source}]\n{chunk}")

    return "\n\n---\n\n".join(formatted)


if __name__ == "__main__":
    # Quick test
    ctx = get_relevant_context("tell me about your projects")
    print(ctx[:2000])
