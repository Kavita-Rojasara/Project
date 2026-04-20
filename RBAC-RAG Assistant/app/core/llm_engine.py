from transformers import pipeline
import torch

# Load model
generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device_map="auto",
    torch_dtype=torch.float32
)


def generate_llm_answer(query: str, context_chunks: list):
    """
    Generic LLM answer generator (NO domain-specific hacks)
    """

    if not context_chunks:
        return (
            "I couldn’t find a clear answer in the available documents. "
            "Try rephrasing your question."
        )

    # Extract text 
    texts = [chunk["text"] for chunk in context_chunks]
    context = "\n\n".join(texts)

    # Prompt
    prompt = f"""
You are an internal company assistant.

Answer the question using ONLY the provided documents.
Be concise and clear.
Do NOT repeat the question.
Do NOT invent information.

Documents:
{context}

Question:
{query}

Answer:
"""

    result = generator(
        prompt,
        max_new_tokens=120,
        temperature=0.2,
        do_sample=True
    )

    output = result[0]["generated_text"]

    # Output
    answer = output.replace(prompt, "").strip()

    # Safety fallback (LLM sometimes returns garbage)
    if not answer:
        return texts[0][:300]

    return answer