def build_prompt(query, docs):
    context = '\n'.join([
        f'- {doc.page_content.strip()[:300]} (Source: {doc.metadata.get(""filename"","")})'
        for doc, _ in docs
    ])
    prompt = (
        f'Answer ONLY using the context below.\n'
        f'- If the context clearly contains the answer, state it concisely.\n'
        f'- If the context does not contain the answer, reply exactly: I don\u2019t know\n\n'
        f'Context:\n{context}\n\n'
        f'Question: {query}\n'
        f'Answer:'
    )
    return prompt