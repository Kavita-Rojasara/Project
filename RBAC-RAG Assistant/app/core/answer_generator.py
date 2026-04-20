def generate_answer(query: str, chunks: list):
    if not chunks:
        return "I couldn’t find a clear answer in the available documents."

    best_chunk = chunks[0]["text"].strip()

    if len(best_chunk) > 500:
        best_chunk = best_chunk[:500] + "..."

    return best_chunk