# Abyssinia AI - CLI entry point
import os
import sys
from dotenv import load_dotenv
from .vectordb_and_ingestion import VectorDBManager
from .prompt_builder import build_prompt
from .rag_assistant.retriever import deduplicate_and_filter
from .logger import logger

__version__ = '0.1.0'


def retrieve_relevant_chunks(vector_db, query, top_k=2, similarity_threshold=1.0):
    if not vector_db:
        logger.error('Vector DB not initialized.')
        return []
    results = vector_db.similarity_search_with_score(query, k=top_k * 5)
    results = sorted(results, key=lambda x: (x[1] is None, x[1]))
    return deduplicate_and_filter(results, top_k=top_k, threshold=similarity_threshold)


def respond_to_query(query, top_k=2, similarity_threshold=1.0):
    load_dotenv()
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        return 'Error: GROQ_API_KEY missing.'
    try:
        from langchain_groq import ChatGroq
    except ImportError:
        return 'Error: langchain_groq not installed.'
    vm = VectorDBManager()
    vm.load_db()
    if not vm.vector_db:
        vm.embed_and_insert()
    if not vm.vector_db:
        return 'Error: Failed to initialise vector database.'
    docs = retrieve_relevant_chunks(vm.vector_db, query, top_k, similarity_threshold)
    if not docs:
        return 'No relevant information found.'
    try:
        prompt = build_prompt(query, docs)
    except ValueError as e:
        return f'Prompt error: {e}'
    try:
        llm = ChatGroq(api_key=groq_key, model='llama3-8b-8192', temperature=0)
        answer = llm.invoke(prompt)
        return getattr(answer, 'content', str(answer))
    except Exception as e:
        return f'Error: {e}'


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Abyssinia AI CLI')
    parser.add_argument('query', nargs='?')
    parser.add_argument('--top_k', type=int, default=2)
    parser.add_argument('--threshold', type=float, default=1.0)
    parser.add_argument('--version', action='version', version=f'abyssinia-ai {__version__}')
    args = parser.parse_args()
    if not args.query:
        parser.print_help()
        sys.exit(1)
    print('\nAnswer:\n', respond_to_query(args.query, args.top_k, args.threshold))

