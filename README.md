# 🏛️ Abyssinia AI — Ethiopian History RAG Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.37-FF4B4B?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-0.3-blueviolet?logo=chainlink&logoColor=white" />
  <img src="https://img.shields.io/badge/ChromaDB-0.5.5-orange" />
  <img src="https://img.shields.io/badge/Groq-LLaMA_3.1-green" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

> A production-ready Retrieval-Augmented Generation (RAG) application that answers questions about Ethiopian and Abyssinian history using a curated local text corpus, a persistent ChromaDB vector store, and the Groq-hosted LLaMA 3.1 LLM.

---

## 📸 Screenshots

| Answer Found | Out-of-Scope Query |
|---|---|
| <img width="500" alt="Answer found" src="https://github.com/user-attachments/assets/392a5dbd-ae5e-4934-8edb-6e8e3b79a805" /> | <img width="500" alt="No answer" src="https://github.com/user-attachments/assets/baa4041e-a550-4e3a-b891-e3f3b60bb599" /> |

---

## ✨ Features

- 📚 **Curated Corpus** — Eight hand-crafted `.txt` documents covering Axum, the Zagwe Dynasty, Solomonic Dynasty, Menelik II, Haile Selassie, the Derg Regime, the Ethiopian Civil War, and Modern Ethiopia.
- 🔍 **Semantic Search** — Embeds documents with `sentence-transformers/all-MiniLM-L6-v2` and stores them in ChromaDB for fast similarity search.
- 🧠 **Grounded Answers** — Strict prompt policy: answers come *only* from retrieved context; the model replies "I don't know" when no relevant chunk is found.
- ⚡ **Groq LLM** — Uses `llama-3.1-8b-instant` via `langchain_groq` for sub-second inference.
- 🖥️ **Streamlit UI** — Interactive sliders for Top-K chunks and similarity threshold; no coding required to query.
- 💻 **CLI Interface** — Script-friendly `retrieval_and_response.py` for shell pipelines and automation.
- 🐳 **Docker Support** — Single-command containerised deployment.
- 🌐 **Wikipedia Ingestion** — `wiki_fetcher.py` lets you expand the corpus with any Wikipedia article.
- ✅ **Unit Tests** — Pytest suite covering retrieval deduplication logic.

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────┐
│                   Streamlit UI / CLI                │
│               (app.py / retrieval_and_response.py)  │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
           ┌────────────────────────┐
           │   VectorDBManager      │
           │  vectordb_and_ingestion│
           │  • Chunk (RecursiveCS) │
           │  • Embed (MiniLM-L6)   │
           │  • Persist (ChromaDB)  │
           └────────────┬───────────┘
                        │ top-k chunks
                        ▼
           ┌────────────────────────┐
           │   rag_assistant pkg    │
           │  retriever.py          │
           │  • filter by threshold │
           │  • deduplicate         │
           └────────────┬───────────┘
                        │ filtered docs
                        ▼
           ┌────────────────────────┐
           │   prompt_builder.py    │
           │  • build context string│
           │  • strict grounding    │
           └────────────┬───────────┘
                        │ prompt
                        ▼
           ┌────────────────────────┐
           │   Groq LLM (LLaMA 3.1) │
           │   via langchain_groq   │
           └────────────┬───────────┘
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
│   ├── derg_regime.txt
│   ├── ethiopian_civil_war.txt
│   ├── haile_selassie.txt
│   ├── menelik_II.txt
│   ├── modern_ethiopia.txt
│   ├── solomonic_dynasty.txt
│   └── zagwe_dynasty.txt
├── tests/
│   └── test_retriever.py         # Pytest unit tests
├── models/
│   └── README.md                 # Notes on embedding model
├── assets/
│   └── screenshots/              # UI screenshots
├── wiki_fetcher.py               # Wikipedia corpus expansion utility
├── Dockerfile                    # Container build definition
├── requirements.txt              # Pinned Python dependencies
├── .env.example                  # Environment variable template
├── .gitignore
└── README.md
```

---

## 🚀 Quickstart

### 1. Clone & set up environment

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

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env and paste your Groq API key
```

`.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com).

### 4. Run the Streamlit app

```bash
streamlit run code/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### 5. (Optional) Expand the corpus with Wikipedia

```bash
python -c "from wiki_fetcher import fetch_and_save_page; fetch_and_save_page('Battle of Adwa')"
```

Then re-run the app — it will automatically re-embed the new document on first query.

---

## 💻 CLI Usage

```bash
python -m code.retrieval_and_response "Who was Menelik II?" --top_k 2 --threshold 1.0
```

Arguments:

| Argument | Default | Description |
|---|---|---|
| `query` | *(required)* | Your question about Ethiopian history |
| `--top_k` | `2` | Number of top chunks to retrieve |
| `--threshold` | `1.0` | Max cosine distance (lower = stricter match) |

---

## 🐳 Docker

```bash
# Build the image
docker build -t abyssinia-ai .

# Run (pass your API key at runtime)
docker run -p 8501:8501 -e GROQ_API_KEY=your_key abyssinia-ai
```

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## 🗂️ Data Corpus

| File | Topic |
|---|---|
| `axum_empire.txt` | The Aksumite Empire (1st–10th century CE) |
| `zagwe_dynasty.txt` | The Zagwe Dynasty and rock-hewn churches |
| `solomonic_dynasty.txt` | The Solomonic restoration and imperial lineage |
| `menelik_II.txt` | Emperor Menelik II and the Battle of Adwa |
| `haile_selassie.txt` | Emperor Haile Selassie and the League of Nations |
| `derg_regime.txt` | The Derg military junta (1974–1991) |
| `ethiopian_civil_war.txt` | The Ethiopian Civil War |
| `modern_ethiopia.txt` | Contemporary Ethiopia and the EPRDF/PP era |

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | API key for Groq LLM inference |

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| `GROQ_API_KEY missing` | Create `.env` and add `GROQ_API_KEY=your_key` |
| Slow first startup | Normal — embedding all documents takes ~30 s |
| Weak/irrelevant answers | Increase `Top-K` or lower the similarity threshold |
| `ModuleNotFoundError` | Ensure venv is active and `pip install -r requirements.txt` was run |
| Empty results | Check `.txt` files exist in `data/` and contain text |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push and open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) for the RAG orchestration framework
- [ChromaDB](https://github.com/chroma-core/chroma) for the vector store
- [Groq](https://groq.com) for ultra-fast LLM inference
- [Hugging Face](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) for the embedding model
- Ethiopian history scholars and Wikipedia contributors for reference material
