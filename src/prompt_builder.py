# Abyssinia AI - Prompt construction
from typing import List, Tuple, Any


def build_prompt(query: str, docs: List[Tuple[Any, float]]) -> str:
    """
    Build a strict, context-grounded prompt for the LLM.

    Raises:
        ValueError: if query or docs is empty.
    """
    if not query or not query.strip():
        raise ValueError('Query must not be empty.')
    if not docs:
        raise ValueError('Docs list must not be empty.')
    context_lines = []
    for i, (doc, _) in enumerate(docs, 1):
        src = doc.metadata.get('filename', 'unknown')
        snippet = doc.page_content.strip()[:400].replace('\n', ' ')
        context_lines.append(f'[{i}] (Source: {src}) {snippet}')
    context = '\n'.join(context_lines)
    return (
        f'You are a factual assistant specialising in Ethiopian history.\n'
        f'Answer ONLY using the numbered context passages below.\n'
        f'- If found, cite the source number.\n'
        f'- If not found, reply: I do not know\n\n'
        f'Context:\n{context}\n\n'
        f'Question: {query}\n'
        f'Answer:'
    )

