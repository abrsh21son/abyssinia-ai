# Abyssinia AI - Ethiopian History RAG Assistant

A production-ready Retrieval-Augmented Generation (RAG) application that answers questions
about Ethiopian and Abyssinian history using a curated local text corpus, a persistent
ChromaDB vector store, and the Groq-hosted LLaMA 3.1 LLM.

## Features

- Curated Corpus: Eight .txt documents covering Axum through Modern Ethiopia
- Semantic Search: sentence-transformers/all-MiniLM-L6-v2 + ChromaDB
- Grounded Answers: Answers only from retrieved context; replies 'I do not know' otherwise
- Groq LLM: llama-3.1-8b-instant for sub-second inference
- Streamlit UI: Sliders for Top-K and similarity threshold
- CLI Interface: Script-friendly entry point
- Docker Support: Single-command containerised deployment
- Wikipedia Ingestion: Expand corpus from any Wikipedia article
- Unit Tests: Pytest suite covering retrieval and prompt logic

## Architecture

User Query -> Streamlit UI / CLI -> VectorDBManager (ChromaDB)
-> deduplicate_and_filter -> build_prompt -> Groq LLaMA 3.1 -> Answer

## Quickstart

git clone https://github.com/abrsh21son/abyssinia-ai.git
cd abyssinia-ai
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
cp .env.example .env      # add GROQ_API_KEY
streamlit run code/app.py

## CLI Usage

python -m code.retrieval_and_response "Who was Menelik II?" --top_k 2 --threshold 1.0

## Docker

docker build -t abyssinia-ai .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key abyssinia-ai

## Tests

pytest tests/ -v

## Data Corpus

axum_empire.txt, zagwe_dynasty.txt, solomonic_dynasty.txt, menelik_II.txt,
haile_selassie.txt, derg_regime.txt, ethiopian_civil_war.txt, modern_ethiopia.txt

## Environment Variables

GROQ_API_KEY - Your Groq API key (https://console.groq.com)

## License

MIT License - see LICENSE for details.