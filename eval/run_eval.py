"""
eval/run_eval.py
Batch evaluator — runs 20 interview questions through the agent pipeline
(bypasses voice, tests LLM+RAG directly) and prints a fidelity report.

Run with:
  python -m eval.run_eval
"""
import asyncio
import json
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.pipeline import generate_response

QUESTIONS = [
    # Intro
    "Tell me about yourself.",
    "What's your background in machine learning?",
    "Why did you choose to specialize in AI/ML?",

    # Projects
    "Tell me about a challenging project you've worked on.",
    "What is your most technically complex project?",
    "Tell me about a project that failed and what you learned from it.",

    # Technical
    "When would you use RAG vs fine-tuning an LLM?",
    "What's your opinion on Python vs Go for backend services?",
    "How do you think about monolith vs microservices?",
    "Explain how you'd build a semantic search system from scratch.",
    "How would you deal with a heavily imbalanced dataset?",
    "What's your approach to debugging a production ML model that's underperforming?",

    # Behavioral
    "Tell me about a time you disagreed with a technical decision.",
    "Describe a time you had to learn a new technology quickly.",
    "Tell me about a time you mentored or helped a junior engineer.",
    "Tell me about a production incident you handled.",

    # Opinions
    "What do you think makes a good engineering team?",
    "What do you look for in a role?",
    "What are your weaknesses or blind spots?",
    "Where do you see AI/ML going in the next 3 years?",
]

RESULTS_FILE = Path(__file__).parent / "results.json"


async def run_eval():
    print("🧪 Running evaluation over 20 interview questions...")
    print("=" * 60)

    results = []
    total_time = 0

    for i, question in enumerate(QUESTIONS, 1):
        print(f"\n[{i:02d}/{len(QUESTIONS)}] Q: {question}")
        t0 = time.time()
        try:
            answer = await generate_response(question)
            elapsed = round(time.time() - t0, 2)
            total_time += elapsed
            status = "✅"
        except Exception as e:
            answer = f"ERROR: {e}"
            elapsed = round(time.time() - t0, 2)
            status = "❌"

        print(f"       A: {answer[:200]}{'...' if len(answer) > 200 else ''}")
        print(f"       {status} {elapsed}s")

        results.append({
            "question": question,
            "answer": answer,
            "latency_s": elapsed,
            "ok": not answer.startswith("ERROR"),
        })

    # Save results
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Report
    ok_count = sum(1 for r in results if r["ok"])
    avg_latency = round(total_time / len(results), 2)
    print("\n" + "=" * 60)
    print(f"📊 EVALUATION REPORT")
    print(f"   Questions answered:  {ok_count}/{len(QUESTIONS)}")
    print(f"   Average latency:     {avg_latency}s")
    print(f"   Total time:          {round(total_time, 1)}s")
    print(f"   Results saved to:    {RESULTS_FILE}")

    failed = [r for r in results if not r["ok"]]
    if failed:
        print(f"\n❌ Failed questions:")
        for r in failed:
            print(f"   - {r['question']}: {r['answer']}")


if __name__ == "__main__":
    asyncio.run(run_eval())
