"""
knowledge_base/ingest.py
Reads all .md files from data/, chunks them, embeds with sentence-transformers,
and upserts into a local ChromaDB collection named 'persona'.
"""
import os
import uuid
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer

DATA_DIR = Path(__file__).parent / "data"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "persona"
CHUNK_SIZE = 300       # words per chunk
CHUNK_OVERLAP = 50     # overlap words between chunks


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split a string of text into overlapping word-based chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start += chunk_size - overlap
    return chunks


def ingest():
    print("🔄 Starting ingestion...")

    # Load embedding model
    print("📦 Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Set up ChromaDB (persistent, local)
    CHROMA_DIR.mkdir(exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Delete existing collection if present (clean rebuild)
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"🗑️  Cleared existing '{COLLECTION_NAME}' collection.")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    total_chunks = 0
    md_files = sorted(DATA_DIR.glob("*.md"))

    if not md_files:
        print(f"❌ No .md files found in {DATA_DIR}")
        return

    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        ids = [str(uuid.uuid4()) for _ in chunks]
        embeddings = model.encode(chunks, show_progress_bar=False).tolist()
        metadatas = [{"source": md_file.name} for _ in chunks]

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )
        print(f"  ✅ {md_file.name}: {len(chunks)} chunks ingested")
        total_chunks += len(chunks)

    print(f"\n🎉 Done! Ingested {total_chunks} total chunks from {len(md_files)} files.")
    print(f"📁 ChromaDB stored at: {CHROMA_DIR.resolve()}")


if __name__ == "__main__":
    ingest()
