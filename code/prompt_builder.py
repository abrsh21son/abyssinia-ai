def build_prompt(query: str, docs: list) -> str:
    """Build a concise, factual prompt for the LLM using only provided context."""
    context = '\n'.join([
        f'- {doc.page_content.strip()[:300]} (Source: {doc.metadata.get(""filename"","")})'
        for doc, _ in docs
    ])
    return (
        f'Answer ONLY using the context below.\n'
        f'- If the context contains the answer, state it concisely.\n'
        f'- If not, reply exactly: I do not know\n\n'
        f'Context:\n{context}\n\n'
        f'Question: {query}\n'
        f'Answer:'
    )