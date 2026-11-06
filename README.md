# 🏛️ Abyssinia AI — Ethiopian History RAG Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.37-FF4B4B?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-0.3-blueviolet" />
  <img src="https://img.shields.io/badge/ChromaDB-0.5.5-orange" />
  <img src="https://img.shields.io/badge/Groq-LLaMA_3.1-green" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
  <img src="https://github.com/abrsh21son/abyssinia-ai/actions/workflows/ci.yml/badge.svg" />
</p>

> A production-ready Retrieval-Augmented Generation (RAG) application that answers questions about Ethiopian and Abyssinian history using a curated local text corpus, a persistent ChromaDB vector store, and the Groq-hosted LLaMA 3.1 LLM.

---

## 📸 Screenshots

| Answer Found | Out-of-Scope Query |
|---|---|
| <img width="500" alt="Answer found" src="https://github.com/user-attachments/assets/392a5dbd-ae5e-4934-8edb-6e8e3b79a805" /> | <img width="500" alt="No answer" src="https://github.com/user-attachments/assets/baa4041e-a550-4e3a-b891-e3f3b60bb599" /> |

---

## ✨ Features

- 📚 **Curated Corpus** — Eight hand-crafted `.txt` documents covering Axum, Zagwe, Solomonic Dynasty, Menelik II, Haile Selassie, the Derg Regime, the Ethiopian Civil War, and Modern Ethiopia.
- 🔍 **Semantic Search** — Embeds documents with `sentence-transformers/all-MiniLM-L6-v2` and stores them in ChromaDB for fast similarity search.
- 🧠 **Grounded Answers** — Strict prompt policy: answers come *only* from retrieved context; the model replies "I do not know" when nothing relevant is found.
- ⚡ **Groq LLM** — Uses `llama-3.1-8b-instant` via `langchain_groq` for sub-second inference.
- 🖥️ **Streamlit UI** — Interactive sliders for Top-K chunks and similarity threshold, a sidebar with corpus info, and a collapsible sources panel.
- 💻 **CLI Interface** — Script-friendly entry point with `--version` and `--threshold` flags.
- 🐳 **Docker Support** — Single-command containerised deployment.
- 🌐 **Wikipedia Ingestion** — `wiki_fetcher.py` lets you expand the corpus with any Wikipedia article.
- ✅ **Unit Tests** — Pytest suite covering retrieval, prompt building, generator, data loader, and CLI pipeline.
- ⚙️ **CI/CD** — GitHub Actions workflow runs tests against Python 3.11 and 3.12.

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────┐
│               Streamlit UI / CLI                    │
│         (app.py / retrieval_and_response.py)        │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
           ┌────────────────────────────┐
           │      VectorDBManager       │
           │  vectordb_and_ingestion.py │
           │  • Chunk (Recursive CS)    │
           │  • Embed (MiniLM-L6-v2)    │
           │  • Persist (ChromaDB)      │
           └────────────┬───────────────┘
                        │ top-k chunks
                        ▼
           ┌────────────────────────────┐
           │    rag_assistant package   │
           │    retriever.py            │
           │  • filter by threshold     │
           │  • deduplicate content     │
           └────────────┬───────────────┘
                        │ filtered docs
                        ▼
           ┌────────────────────────────┐
           │     prompt_builder.py      │
           │  • numbered source context │
           │  • strict grounding policy │
           └────────────┬───────────────┘
                        │ prompt
                        ▼
           ┌────────────────────────────┐
           │   Groq LLM (LLaMA 3.1)    │
           │    via langchain_groq      │
           └────────────┬───────────────┘
                        │
                        ▼
                    Answer ✅
```

---

## 📂 Project Structure

```
abyssinia-ai/
├── code/
│   ├── app.py                    # Streamlit UI entry point
│   ├── retrieval_and_response.py # CLI pipeline
│   ├── vectordb_and_ingestion.py # VectorDBManager (chunk/embed/persist)
│   ├── prompt_builder.py         # Prompt assembly with grounding policy
│   ├── logger.py                 # Shared console logger
│   └── rag_assistant/
│       ├── __init__.py
│       ├── data_loader.py        # List .txt corpus files
│       ├── retriever.py          # Filter & deduplicate results
│       └── generator.py          # Wrap LLM invocation
├── data/
│   ├── axum_empire.txt
│   ├── zagwe_dynasty.txt
│   ├── solomonic_dynasty.txt
│   ├── menelik_II.txt
│   ├── haile_selassie.txt
│   ├── derg_regime.txt
│   ├── ethiopian_civil_war.txt
│   └── modern_ethiopia.txt
├── tests/
│   ├── test_retriever.py
│   ├── test_prompt_builder.py
│   ├── test_generator.py
│   ├── test_data_loader.py
│   ├── test_retrieval_pipeline.py
│   ├── test_vectordb_manager.py
│   └── conftest.py
├── models/
│   └── README.md
├── assets/
│   └── screenshots/
├── .github/
│   └── workflows/
│       └── ci.yml
├── wiki_fetcher.py               # Wikipedia corpus expansion utility
├── Dockerfile
├── .dockerignore
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
└── README.md
```

---

## 🚀 Quickstart

### 1. Clone and set up

```bash
git clone https://github.com/abrsh21son/abyssinia-ai.git
cd abyssinia-ai

python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com).

### 4. Run the app

```bash
streamlit run code/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 💻 CLI Usage

```bash
python -m code.retrieval_and_response "Who was Menelik II?" --top_k 2 --threshold 1.0
```

| Argument | Default | Description |
|---|---|---|
| `query` | *(required)* | Question about Ethiopian history |
| `--top_k` | `2` | Number of top chunks to retrieve |
| `--threshold` | `1.0` | Max cosine distance (lower = stricter) |
| `--version` | — | Print version and exit |

---

## 🌐 Expanding the Corpus

```bash
python -c "from wiki_fetcher import fetch_and_save_page; fetch_and_save_page('Battle of Adwa')"
```

Then delete `chroma_db/` and restart the app to re-embed the new document.

---

## 🐳 Docker

```bash
docker build -t abyssinia-ai .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key abyssinia-ai
```

---

## 🧪 Tests

```bash
pytest tests/ -v
```

---

## 🗂️ Data Corpus

| File | Topic |
|---|---|
| `axum_empire.txt` | The Aksumite Empire (1st–10th century CE) |
| `zagwe_dynasty.txt` | Zagwe Dynasty and Lalibela churches |
| `solomonic_dynasty.txt` | Solomonic restoration and imperial lineage |
| `menelik_II.txt` | Emperor Menelik II and the Battle of Adwa |
| `haile_selassie.txt` | Haile Selassie and the OAU |
| `derg_regime.txt` | Derg military junta and Red Terror (1974–1991) |
| `ethiopian_civil_war.txt` | Ethiopian Civil War and TPLF/EPLF |
| `modern_ethiopia.txt` | EPRDF era through Abiy Ahmed and the Tigray War |

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | API key for Groq LLM inference |

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| `GROQ_API_KEY missing` | Create `.env` from `.env.example` and add your key |
| Slow first startup | Normal — embedding the corpus takes ~30 s on first run |
| Weak/irrelevant answers | Increase Top-K or lower the similarity threshold |
| `ModuleNotFoundError` | Activate venv and run `pip install -r requirements.txt` |
| Empty results | Check `.txt` files exist in `data/` |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) — RAG orchestration
- [ChromaDB](https://github.com/chroma-core/chroma) — vector store
- [Groq](https://groq.com) — ultra-fast LLM inference
- [Hugging Face](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) — embedding model
