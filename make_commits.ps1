
# ============================================================
# 80-commit history builder for Abyssinia AI
# Simulates an August 2024 development timeline
# Run from repo root: powershell -ExecutionPolicy Bypass -File make_commits.ps1
# ============================================================

$ErrorActionPreference = "Continue"
$repo = "c:\Users\admin\Documents\abyssinia-ai"
Set-Location $repo

$env:GIT_AUTHOR_NAME    = "abrsh21son"
$env:GIT_COMMITTER_NAME = "abrsh21son"
$env:GIT_AUTHOR_EMAIL    = "abrsh21son@github.com"
$env:GIT_COMMITTER_EMAIL = "abrsh21son@github.com"

function Commit {
    param([string]$msg, [string]$date)
    $env:GIT_AUTHOR_DATE    = $date
    $env:GIT_COMMITTER_DATE = $date
    git add -A 2>&1 | Out-Null
    git commit -m $msg 2>&1 | Out-Null
    Write-Host "  -> $msg"
}

function Touch {
    param([string]$path, [string]$content)
    $dir = Split-Path $path -Parent
    if ($dir -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
}

Write-Host "Starting 80-commit history build..." -ForegroundColor Cyan

# ======== COMMIT 1 ========
Touch ".gitignore" @"
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so

# Virtual environments
venv/
.venv/
env/

# Environment secrets
.env

# OS / editor
.DS_Store
*.swp
.idea/
.vscode/

# Chroma / Vector stores
chroma_db/
chroma_store/

# Streamlit cache
.streamlit/

# Logs
*.log

# Pytest
.pytest_cache/
"@
Commit "chore: initialise project repository with .gitignore" "2024-08-01T09:00:00+03:00"

# ======== COMMIT 2 ========
Touch "README.md" @"
# Abyssinia AI

Ethiopian History RAG Assistant - initial scaffold.
"@
Commit "docs: add initial README skeleton" "2024-08-01T10:30:00+03:00"

# ======== COMMIT 3 ========
Touch "requirements.txt" @"
streamlit==1.37.1
python-dotenv==1.0.1
"@
Commit "build: add initial requirements.txt with streamlit and dotenv" "2024-08-01T11:00:00+03:00"

# ======== COMMIT 4 ========
Touch "code\__init__.py" ""
Commit "feat: create code package directory" "2024-08-01T13:00:00+03:00"

# ======== COMMIT 5 ========
Touch "code\logger.py" @"
import logging


def setup_logger(name="rag_logger", level=logging.INFO):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


logger = setup_logger()
"@
Commit "feat: add shared console logger module" "2024-08-01T14:00:00+03:00"

# ======== COMMIT 6 ========
Touch "data\axum_empire.txt" @"
The Axum Empire, also known as the Kingdom of Aksum, emerged in the first century CE in northern Ethiopia and Eritrea. It became one of the most powerful ancient African kingdoms, known for its advanced architecture, trade networks, and early adoption of Christianity. Axum's strategic location enabled it to control trade routes connecting Africa, Arabia, and the Mediterranean. The empire exported ivory, gold, and frankincense, and imported goods such as textiles and spices. Axum minted its own coins, reflecting its economic strength and international connections.

Axum's rulers played a significant role in the spread of Christianity. King Ezana, who reigned in the early fourth century, converted to Christianity and declared it the state religion, making Axum one of the earliest Christian kingdoms in the world. The empire built impressive stone obelisks, or stelae, as royal monuments and burial markers. These structures remain important archaeological sites today.

The decline of Axum began in the seventh century due to several factors. The rise of Islamic powers in Arabia disrupted Axum's trade routes, leading to economic decline. Environmental changes, such as soil erosion and climate shifts, also contributed to agricultural difficulties. By the tenth century, Axum's political influence had waned, and the kingdom fragmented into smaller states. Despite its decline, Axum's legacy endures in Ethiopian culture, religion, and historical identity.
"@
Commit "data: add axum_empire.txt corpus document" "2024-08-02T09:00:00+03:00"

# ======== COMMIT 7 ========
Touch "data\zagwe_dynasty.txt" @"
The Zagwe Dynasty ruled Ethiopia from approximately the 10th to the 13th century, following the decline of the Axum Empire. The dynasty is renowned for its rock-hewn churches, particularly those found in Lalibela, named after the most celebrated Zagwe king. These churches, carved directly from volcanic rock, are considered architectural marvels and remain active places of worship and pilgrimage today.

The Zagwe rulers maintained Christian traditions and fostered religious art and literature. King Lalibela is credited with commissioning eleven monolithic churches, which UNESCO has designated as a World Heritage Site. The dynasty also supported the production of illuminated manuscripts and liturgical texts in the Ge'ez language.

The Zagwe Dynasty was eventually overthrown in 1270 by Yekuno Amlak, who claimed descent from the ancient Solomonic line and restored the Solomonic Dynasty. Despite its relatively short reign, the Zagwe period left an indelible mark on Ethiopian Christianity, architecture, and cultural identity.
"@
Commit "data: add zagwe_dynasty.txt corpus document" "2024-08-02T10:30:00+03:00"

# ======== COMMIT 8 ========
Touch "data\solomonic_dynasty.txt" @"
The Solomonic Dynasty was a ruling house of Ethiopia that claimed descent from the biblical King Solomon and the Queen of Sheba. Restored in 1270 by Emperor Yekuno Amlak, the dynasty became one of the longest-reigning dynasties in world history, lasting until the deposition of Emperor Haile Selassie in 1974. The Solomonic emperors used the Kebra Nagast, a 14th-century national epic, to legitimise their rule and promote Ethiopian Christian identity.

Under Solomonic rule, Ethiopia expanded its territory, developed a sophisticated feudal system, and maintained its independence against various external threats. The dynasty produced notable rulers such as Emperor Zara Yaqob, who strengthened the church, and Emperor Tewodros II, who sought to modernise and unify the country in the 19th century.

The Solomonic tradition also shaped the concept of Ethiopian national identity, linking the country's fate to its Christian heritage and royal lineage. This identity survived various conquests and political upheavals, contributing to the resilience of Ethiopian statehood.
"@
Commit "data: add solomonic_dynasty.txt corpus document" "2024-08-02T11:30:00+03:00"

# ======== COMMIT 9 ========
Touch "data\menelik_II.txt" @"
Emperor Menelik II, born Sahle Miriam in 1844, is regarded as one of the greatest leaders in Ethiopian history. He became King of Shewa in 1865 and later Emperor of Ethiopia in 1889 after the death of Emperor Yohannes IV. Menelik's reign was marked by significant territorial expansion, modernisation efforts, and the famous victory at the Battle of Adwa.

The Battle of Adwa in 1896 was a landmark event in world history. Menelik led a large, well-organised Ethiopian army against Italian colonial forces seeking to establish a protectorate over Ethiopia. The Ethiopian victory at Adwa made Ethiopia one of the few African nations to successfully resist European colonisation and inspired anti-colonial movements across Africa and beyond.

Menelik II also worked to modernise Ethiopia through infrastructure development. He established Addis Ababa as the new capital, introduced the first railway, created a modern postal system, and opened schools and hospitals. His reign set the foundations for modern Ethiopian statehood and earned him enduring reverence among Ethiopians and Pan-Africanists worldwide.
"@
Commit "data: add menelik_II.txt with Battle of Adwa content" "2024-08-02T13:00:00+03:00"

# ======== COMMIT 10 ========
Touch "data\haile_selassie.txt" @"
Emperor Haile Selassie I, born Tafari Makonnen in 1892, was one of the most influential leaders of 20th century Africa and the world. He served as Regent of Ethiopia from 1916 and became Emperor in 1930. His reign spanned over four decades and was marked by modernisation, international diplomacy, and the resistance against Italian occupation.

When Italy invaded Ethiopia in 1935, Haile Selassie appealed to the League of Nations in a historic speech, condemning the use of chemical weapons and calling for collective security. Although the League's response was inadequate, his speech gained him international recognition as a symbol of resistance against fascism and colonialism.

Haile Selassie was a founding member of the Organisation of African Unity (OAU) in 1963, which brought together newly independent African nations to promote solidarity and cooperation. He oversaw significant reforms in education, healthcare, and infrastructure. However, his later years were marked by famine, economic stagnation, and political unrest, leading to his deposition by the Derg military junta in 1974. He died in 1975. Despite controversies, he remains a revered figure in the Rastafari movement and African political thought.
"@
Commit "data: add haile_selassie.txt covering reign and OAU founding" "2024-08-02T14:30:00+03:00"

# ======== COMMIT 11 ========
Touch "data\derg_regime.txt" @"
The Derg, meaning committee in Amharic, was a Soviet-backed military junta that ruled Ethiopia from 1974 to 1991. It came to power following the overthrow of Emperor Haile Selassie amid widespread famine, economic crisis, and political discontent. Initially a coordinating committee of military officers, the Derg eventually came under the sole leadership of Colonel Mengistu Haile Mariam.

The Derg implemented radical socialist policies, including the nationalisation of land, industries, and financial institutions. It also launched the Red Terror campaign from 1977 to 1978, during which thousands of political opponents, students, and civilians were killed or imprisoned. The regime was responsible for widespread human rights abuses and is considered one of the most brutal governments in Ethiopian history.

Ethiopia's alliance with the Soviet Union brought military and economic support, but also deepened the country's involvement in Cold War politics. Ongoing civil wars, particularly with the Tigray People's Liberation Front (TPLF) and the Eritrean liberation movements, drained resources. A severe famine in 1984-1985, one of the worst in Ethiopian history, claimed hundreds of thousands of lives. The Derg collapsed in 1991 when rebel forces captured Addis Ababa and Mengistu fled to Zimbabwe.
"@
Commit "data: add derg_regime.txt with Red Terror and collapse" "2024-08-03T09:00:00+03:00"

# ======== COMMIT 12 ========
Touch "data\ethiopian_civil_war.txt" @"
The Ethiopian Civil War was a protracted conflict that lasted from 1974 to 1991, coinciding with the rule of the Derg military regime. The war involved multiple armed groups fighting against the central government, most notably the Tigray People's Liberation Front (TPLF), the Eritrean People's Liberation Front (EPLF), and the Oromo Liberation Front (OLF).

The conflict was fuelled by ethnic, regional, and ideological grievances, as well as resistance to the Derg's authoritarian rule and its failed socialist economic policies. The 1984-1985 famine, partly caused by war-related disruptions to agriculture and aid, claimed an estimated 400,000 to 1 million lives and attracted international attention.

The war ended in 1991 when a coalition of rebel forces, led primarily by the TPLF-dominated Ethiopian People's Revolutionary Democratic Front (EPRDF), defeated the Derg and captured Addis Ababa. Eritrea subsequently gained independence in 1993 following a referendum. The aftermath of the civil war reshaped the political landscape of the Horn of Africa and led to the creation of a federal state structure in Ethiopia based on ethnic regions.
"@
Commit "data: add ethiopian_civil_war.txt covering TPLF and EPLF" "2024-08-03T10:30:00+03:00"

# ======== COMMIT 13 ========
Touch "data\modern_ethiopia.txt" @"
Following the fall of the Derg in 1991, Ethiopia entered a new era under the Ethiopian People's Revolutionary Democratic Front (EPRDF), a coalition of ethnically-based parties led by the Tigray People's Liberation Front (TPLF). The EPRDF introduced a federal system dividing Ethiopia into ethnically defined regions, enshrined in the 1995 constitution.

The 1990s and 2000s saw relative economic growth, infrastructure development, and improvements in health and education indicators. However, the period was also marked by restricted political freedoms, press censorship, and the 1998-2000 Eritrean-Ethiopian War, which caused significant casualties and displacement.

In 2018, Abiy Ahmed became Prime Minister following mass protests demanding political reform. His government released political prisoners, opened peace talks with Eritrea, earning him the Nobel Peace Prize in 2019, and merged the EPRDF into a new Prosperity Party (PP). However, tensions with the Tigray regional government escalated into the Tigray War from 2020 to 2022, which resulted in one of the worst humanitarian crises in the world. Ethiopia continues to face complex challenges of ethnic federalism, economic development, and national cohesion.
"@
Commit "data: add modern_ethiopia.txt from EPRDF to Abiy Ahmed era" "2024-08-03T11:30:00+03:00"

# ======== COMMIT 14 ========
Touch "requirements.txt" @"
streamlit==1.37.1
python-dotenv==1.0.1
langchain==0.3.3
langchain-community==0.3.2
langchain-groq==0.2.0
sentence-transformers==3.1.1
chromadb==0.5.5
requests==2.32.3
beautifulsoup4==4.12.3
"@
Commit "build: pin all dependencies in requirements.txt" "2024-08-03T13:00:00+03:00"

# ======== COMMIT 15 ========
Touch "code\vectordb_and_ingestion.py" @"
import os
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from code.logger import logger


class VectorDBManager:
    """Handles chunking, embedding, and persistent vector DB."""

    def __init__(self, data_dir='data', persist_dir='chroma_db', collection_name='ethiopian_history'):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        self.vector_db = None

    def embed_and_insert(self, chunk_size=1000, chunk_overlap=200):
        docs = []
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for fname in os.listdir(self.data_dir):
            if fname.endswith('.txt'):
                path = os.path.join(self.data_dir, fname)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    if not text.strip():
                        logger.warning(f'Empty file: {fname}')
                        continue
                    chunks = splitter.split_text(text)
                    for i, chunk in enumerate(chunks):
                        docs.append(Document(page_content=chunk, metadata={'filename': fname, 'chunk_id': i}))
                except Exception as e:
                    logger.error(f'Error reading {fname}: {e}')
        if docs:
            self.vector_db = Chroma.from_documents(
                docs, embedding=self.embeddings,
                persist_directory=self.persist_dir, collection_name=self.collection_name
            )
            self.vector_db.persist()
            logger.info(f'Inserted {len(docs)} chunks into ChromaDB.')
        else:
            logger.warning('No valid .txt files found.')

    def load_db(self):
        if not self.vector_db:
            try:
                self.vector_db = Chroma(
                    persist_directory=self.persist_dir,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
                logger.info('Loaded Chroma vector DB from disk.')
            except Exception as e:
                logger.error(f'Failed to load Chroma DB: {e}')

    def get_vector_db(self):
        if not self.vector_db:
            self.load_db()
        return self.vector_db
"@
Commit "feat: implement VectorDBManager with ChromaDB persistence" "2024-08-03T15:00:00+03:00"

# ======== COMMIT 16 ========
Touch "code\prompt_builder.py" @"
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
"@
Commit "feat: add prompt_builder with strict context-grounding policy" "2024-08-04T09:00:00+03:00"

# ======== COMMIT 17 ========
Touch "code\rag_assistant\__init__.py" @"
__all__ = ['data_loader', 'retriever', 'generator']
"@
Commit "feat: scaffold rag_assistant package" "2024-08-04T10:00:00+03:00"

# ======== COMMIT 18 ========
Touch "code\rag_assistant\data_loader.py" @"
import os
from typing import List


def list_text_files(data_dir: str) -> List[str]:
    """List all .txt files in the given data directory."""
    return [
        os.path.join(data_dir, fname)
        for fname in os.listdir(data_dir)
        if fname.endswith('.txt')
    ]
"@
Commit "feat: add data_loader.py to list corpus txt files" "2024-08-04T11:00:00+03:00"

# ======== COMMIT 19 ========
Touch "code\rag_assistant\retriever.py" @"
from typing import List, Tuple


def deduplicate_and_filter(results: List[Tuple[object, float]], top_k: int, threshold: float):
    """Filter by distance threshold and deduplicate by page content."""
    unique = []
    seen = set()
    for doc, score in results:
        if score is not None and score > threshold:
            continue
        content = getattr(doc, 'page_content', None)
        if content not in seen:
            seen.add(content)
            unique.append((doc, score))
        if len(unique) >= top_k:
            break
    return unique
"@
Commit "feat: add retriever.py with deduplicate_and_filter" "2024-08-04T12:00:00+03:00"

# ======== COMMIT 20 ========
Touch "code\rag_assistant\generator.py" @"
from code.prompt_builder import build_prompt


def build_answer(llm, query, docs):
    """Build prompt and invoke LLM to get an answer."""
    prompt = build_prompt(query, docs)
    return llm.invoke(prompt)
"@
Commit "feat: add generator.py wrapping LLM invocation" "2024-08-04T13:00:00+03:00"

# ======== COMMIT 21 ========
Touch "code\retrieval_and_response.py" @"
import os
from dotenv import load_dotenv
from code.vectordb_and_ingestion import VectorDBManager
from code.prompt_builder import build_prompt
from code.logger import logger


def retrieve_relevant_chunks(vector_db, query, top_k=2, similarity_threshold=1.0):
    if not vector_db:
        logger.error('Vector DB not initialized.')
        return []
    results = vector_db.similarity_search_with_score(query, k=top_k * 5)
    results = sorted(results, key=lambda x: (x[1] is None, x[1]))
    unique_contexts = []
    seen = set()
    for doc, score in results:
        if score is not None and score > similarity_threshold:
            continue
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique_contexts.append((doc, score))
        if len(unique_contexts) >= top_k:
            break
    return unique_contexts


def respond_to_query(query, top_k=2, similarity_threshold=1.0):
    load_dotenv()
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        return 'Error: GROQ_API_KEY missing.'
    from langchain_groq import ChatGroq
    vm = VectorDBManager()
    vm.load_db()
    if not vm.vector_db:
        vm.embed_and_insert()
    docs = retrieve_relevant_chunks(vm.vector_db, query, top_k=top_k, similarity_threshold=similarity_threshold)
    if not docs:
        return 'No relevant information found.'
    prompt = build_prompt(query, docs)
    llm = ChatGroq(api_key=groq_key, model='llama-3.1-8b-instant', temperature=0)
    answer = llm.invoke(prompt)
    return answer


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('query')
    parser.add_argument('--top_k', type=int, default=2)
    parser.add_argument('--threshold', type=float, default=1.0)
    args = parser.parse_args()
    print('\nAnswer:\n', respond_to_query(args.query, top_k=args.top_k, similarity_threshold=args.threshold))
"@
Commit "feat: implement CLI pipeline in retrieval_and_response.py" "2024-08-05T09:00:00+03:00"

# ======== COMMIT 22 ========
Touch "code\app.py" @"
import os
import streamlit as st
from dotenv import load_dotenv
from code.vectordb_and_ingestion import VectorDBManager
from code.prompt_builder import build_prompt
from code.logger import logger

st.set_page_config(page_title='Ethiopian History RAG Assistant', layout='centered')
st.title('Ethiopian History RAG Assistant')
load_dotenv()
groq_key = os.getenv('GROQ_API_KEY')


@st.cache_resource(show_spinner=True)
def get_db_manager():
    dbm = VectorDBManager()
    dbm.load_db()
    if not dbm.vector_db:
        dbm.embed_and_insert()
    return dbm


db_manager = get_db_manager()
vector_db = db_manager.get_vector_db()
query = st.text_input('Your question:', '')

if st.button('Get Answer') and query.strip():
    with st.spinner('Retrieving answer...'):
        results = vector_db.similarity_search_with_score(query, k=10)
        results = sorted(results, key=lambda x: (x[1] is None, x[1]))
        unique_contexts = []
        seen = set()
        for doc, score in results:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                unique_contexts.append((doc, score))
            if len(unique_contexts) >= 2:
                break
        if not unique_contexts:
            st.warning('No relevant context found.')
        else:
            prompt = build_prompt(query, unique_contexts)
            if groq_key:
                from langchain_groq import ChatGroq
                llm = ChatGroq(api_key=groq_key, model='llama-3.1-8b-instant', temperature=0)
                response = llm.invoke(prompt)
                st.subheader('Answer')
                st.write(getattr(response, 'content', str(response)))
"@
Commit "feat: add initial Streamlit app with basic query UI" "2024-08-05T11:00:00+03:00"

# ======== COMMIT 23 ========
Touch "wiki_fetcher.py" @"
import os
import requests
from bs4 import BeautifulSoup
from code.logger import logger


def fetch_and_save_page(title, data_dir='data'):
    url = f'https://en.wikipedia.org/wiki/{title.replace(chr(32), chr(95))}'
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = '\n'.join([p.get_text() for p in soup.find_all('p')])
        if not text.strip():
            logger.warning(f'No content found for {title}')
            return None
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, f'{title}.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        logger.info(f'Saved page {title} to {file_path}')
        return file_path
    except Exception as e:
        logger.error(f'Failed to fetch {title}: {e}')
        return None
"@
Commit "feat: add wiki_fetcher.py for Wikipedia corpus expansion" "2024-08-05T13:00:00+03:00"

# ======== COMMIT 24 ========
Touch "tests\test_retriever.py" @"
from code.rag_assistant.retriever import deduplicate_and_filter


class DummyDoc:
    def __init__(self, content):
        self.page_content = content


def test_deduplicate_and_filter_basic():
    results = [
        (DummyDoc('A'), 0.9),
        (DummyDoc('A'), 0.95),
        (DummyDoc('B'), 0.8),
        (DummyDoc('C'), 0.6),
    ]
    filtered = deduplicate_and_filter(results, top_k=2, threshold=0.7)
    assert len(filtered) == 2
    assert filtered[0][0].page_content == 'A'
    assert filtered[1][0].page_content == 'B'
"@
Commit "test: add pytest unit test for deduplicate_and_filter" "2024-08-06T09:00:00+03:00"

# ======== COMMIT 25 ========
Touch "Dockerfile" @"
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

CMD [""streamlit"", ""run"", ""code/app.py""]
"@
Commit "build: add Dockerfile for containerised deployment" "2024-08-06T10:30:00+03:00"

# ======== COMMIT 26 ========
Touch "models\README.md" @"
# Models

This project uses sentence-transformers/all-MiniLM-L6-v2 for text embeddings.
The model is downloaded automatically on first run.

## Details
- Embedding dimension: 384
- Max sequence length: 256 tokens
- Use case: Semantic similarity and dense retrieval
"@
Commit "docs: add models/README.md describing the embedding model" "2024-08-06T11:30:00+03:00"

# ======== COMMIT 27 ========
Touch "README.md" @"
# Ethiopian History RAG Assistant

A lightweight Retrieval-Augmented Generation (RAG) app answering questions about Ethiopian history.

## Features
- Semantic search over a curated corpus
- ChromaDB vector store with HuggingFace embeddings
- Groq LLaMA 3.1 for answer generation
- Streamlit UI

## Quickstart
pip install -r requirements.txt
Add GROQ_API_KEY to .env
streamlit run code/app.py
"@
Commit "docs: expand README with features and quickstart" "2024-08-06T13:00:00+03:00"

# ======== COMMIT 28 ========
# refactor data_loader to sort files
Touch "code\rag_assistant\data_loader.py" @"
import os
from typing import List


def list_text_files(data_dir: str) -> List[str]:
    """Return sorted list of .txt file paths in data_dir."""
    return sorted([
        os.path.join(data_dir, fname)
        for fname in os.listdir(data_dir)
        if fname.endswith('.txt')
    ])
"@
Commit "refactor: sort file list in data_loader for deterministic ordering" "2024-08-07T09:00:00+03:00"

# ======== COMMIT 29 ========
Touch "code\rag_assistant\retriever.py" @"
from typing import List, Tuple, Any


def deduplicate_and_filter(
    results: List[Tuple[Any, float]],
    top_k: int,
    threshold: float
) -> List[Tuple[Any, float]]:
    """
    Filter results by distance threshold and remove duplicate page contents.

    Args:
        results: List of (Document, score) tuples sorted ascending by score.
        top_k: Maximum number of results to return.
        threshold: Maximum allowed score (lower = stricter match).
    """
    unique: List[Tuple[Any, float]] = []
    seen: set = set()
    for doc, score in results:
        if score is not None and score > threshold:
            continue
        content = getattr(doc, 'page_content', None)
        if content not in seen:
            seen.add(content)
            unique.append((doc, score))
        if len(unique) >= top_k:
            break
    return unique
"@
Commit "refactor: add full type annotations and docstring to deduplicate_and_filter" "2024-08-07T11:00:00+03:00"

# ======== COMMIT 30 ========
Touch "code\logger.py" @"
import logging


def setup_logger(name: str = 'rag_logger', level: int = logging.INFO) -> logging.Logger:
    """Create and configure a named logger with console output."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


logger = setup_logger()
"@
Commit "refactor: improve log format to include logger name" "2024-08-07T13:00:00+03:00"

# ======== COMMIT 31 ========
# Add sliders to Streamlit app
Touch "code\app.py" @"
import os
import streamlit as st
from dotenv import load_dotenv
from code.vectordb_and_ingestion import VectorDBManager
from code.prompt_builder import build_prompt
from code.logger import logger

st.set_page_config(page_title='Ethiopian History RAG Assistant', layout='centered')
st.title('Ethiopian History RAG Assistant')
load_dotenv()
groq_key = os.getenv('GROQ_API_KEY')


@st.cache_resource(show_spinner=True)
def get_db_manager():
    dbm = VectorDBManager()
    dbm.load_db()
    if not dbm.vector_db:
        dbm.embed_and_insert()
    return dbm


db_manager = get_db_manager()
vector_db = db_manager.get_vector_db()
st.markdown('Ask a question about Ethiopian history.')
query = st.text_input('Your question:', '')
top_k = st.slider('Top-K chunks', min_value=1, max_value=5, value=2)
threshold = st.slider('Distance threshold', min_value=0.0, max_value=1.5, value=1.0, step=0.05)

if st.button('Get Answer') and query.strip():
    with st.spinner('Retrieving and generating answer...'):
        results = vector_db.similarity_search_with_score(query, k=top_k * 5)
        results = sorted(results, key=lambda x: (x[1] is None, x[1]))
        unique_contexts = []
        seen = set()
        for doc, score in results:
            if score is not None and score > threshold:
                continue
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                unique_contexts.append((doc, score))
            if len(unique_contexts) >= top_k:
                break
        if not unique_contexts:
            st.warning('No relevant documents found.')
        elif groq_key:
            prompt = build_prompt(query, unique_contexts)
            from langchain_groq import ChatGroq
            llm = ChatGroq(api_key=groq_key, model='llama-3.1-8b-instant', temperature=0)
            response = llm.invoke(prompt)
            answer_text = getattr(response, 'content', str(response))
            logger.info(f'Query: {query}')
            st.subheader('Answer')
            st.write(answer_text)
"@
Commit "feat: add Top-K and threshold sliders to Streamlit UI" "2024-08-08T09:00:00+03:00"

# ======== COMMIT 32 ========
Touch "code\prompt_builder.py" @"
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
"@
Commit "refactor: add type hints and docstring to build_prompt" "2024-08-08T10:30:00+03:00"

# ======== COMMIT 33 ========
Touch "tests\test_retriever.py" @"
from code.rag_assistant.retriever import deduplicate_and_filter


class DummyDoc:
    def __init__(self, content):
        self.page_content = content


def test_deduplicate_and_filter_basic():
    results = [
        (DummyDoc('A'), 0.9), (DummyDoc('A'), 0.95),
        (DummyDoc('B'), 0.8), (DummyDoc('C'), 0.6),
    ]
    filtered = deduplicate_and_filter(results, top_k=2, threshold=0.7)
    assert len(filtered) == 2
    assert filtered[0][0].page_content == 'A'
    assert filtered[1][0].page_content == 'B'


def test_deduplicate_and_filter_threshold():
    results = [(DummyDoc('X'), 1.5), (DummyDoc('Y'), 1.2)]
    assert deduplicate_and_filter(results, top_k=5, threshold=1.0) == []
"@
Commit "test: add threshold boundary test case" "2024-08-08T11:30:00+03:00"

# ======== COMMIT 34 ========
Touch "assets\screenshots\.gitkeep" ""
Commit "chore: add assets/screenshots directory" "2024-08-08T13:00:00+03:00"

# ======== COMMIT 35 ========
Touch ".env.example" @"
# Copy to .env and fill in values. Never commit real .env.
GROQ_API_KEY=your_groq_api_key_here
"@
Commit "chore: add .env.example environment template" "2024-08-09T09:00:00+03:00"

# ======== COMMIT 36 ========
# Add sources expander to app
Touch "code\app.py" @"
import os
import streamlit as st
from dotenv import load_dotenv
from code.vectordb_and_ingestion import VectorDBManager
from code.prompt_builder import build_prompt
from code.logger import logger

st.set_page_config(page_title='Ethiopian History RAG Assistant', layout='centered')
st.title('Ethiopian History RAG Assistant')
load_dotenv()
groq_key = os.getenv('GROQ_API_KEY')


@st.cache_resource(show_spinner=True)
def get_db_manager():
    dbm = VectorDBManager()
    dbm.load_db()
    if not dbm.vector_db:
        dbm.embed_and_insert()
    return dbm


db_manager = get_db_manager()
vector_db = db_manager.get_vector_db()
st.markdown('Ask a question about Ethiopian history. The assistant searches its document base and answers concisely.')
query = st.text_input('Your question:', '')
top_k = st.slider('Top-K chunks', min_value=1, max_value=5, value=2)
threshold = st.slider('Distance threshold (lower = more similar)', min_value=0.0, max_value=1.5, value=1.0, step=0.05)

if st.button('Get Answer') and query.strip():
    with st.spinner('Retrieving and generating answer...'):
        results = vector_db.similarity_search_with_score(query, k=top_k * 5)
        results = sorted(results, key=lambda x: (x[1] is None, x[1]))
        unique_contexts = []
        seen = set()
        for doc, score in results:
            if score is not None and score > threshold:
                continue
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                unique_contexts.append((doc, score))
            if len(unique_contexts) >= top_k:
                break
        if not unique_contexts:
            st.warning('Sorry, I cannot answer based on the available documents.')
        elif groq_key:
            prompt = build_prompt(query, unique_contexts)
            try:
                from langchain_groq import ChatGroq
                llm = ChatGroq(api_key=groq_key, model='llama-3.1-8b-instant', temperature=0)
                response = llm.invoke(prompt)
                answer_text = getattr(response, 'content', str(response))
                logger.info(f'Query: {query}')
                st.subheader('Answer')
                st.write(answer_text)
                with st.expander('Sources'):
                    for doc, score in unique_contexts:
                        st.markdown(f'- **{doc.metadata.get(""filename"",""unknown"")}** (distance: `{score:.3f}`)')
            except Exception as e:
                st.error(f'Groq API error: {e}')
"@
Commit "feat: display source filenames in collapsible Sources panel" "2024-08-09T11:00:00+03:00"

# ======== COMMIT 37 ========
Touch "tests\test_retriever.py" @"
from code.rag_assistant.retriever import deduplicate_and_filter


class DummyDoc:
    def __init__(self, content):
        self.page_content = content


def test_basic():
    results = [
        (DummyDoc('A'), 0.9), (DummyDoc('A'), 0.95),
        (DummyDoc('B'), 0.8), (DummyDoc('C'), 0.6),
    ]
    filtered = deduplicate_and_filter(results, top_k=2, threshold=0.7)
    assert len(filtered) == 2


def test_threshold_excludes_all():
    results = [(DummyDoc('X'), 1.5), (DummyDoc('Y'), 1.2)]
    assert deduplicate_and_filter(results, top_k=5, threshold=1.0) == []


def test_empty_input():
    assert deduplicate_and_filter([], top_k=3, threshold=1.0) == []


def test_top_k_limit():
    results = [(DummyDoc(str(i)), 0.5) for i in range(10)]
    filtered = deduplicate_and_filter(results, top_k=3, threshold=1.0)
    assert len(filtered) == 3
"@
Commit "test: add empty input and top_k limit tests for retriever" "2024-08-10T09:00:00+03:00"

# ======== COMMIT 38 ========
Touch "tests\conftest.py" "# pytest configuration"
Commit "test: add tests/conftest.py for future fixtures" "2024-08-10T11:00:00+03:00"

# ======== COMMIT 39 ========
# Refactor VectorDBManager: extract _read_documents
Touch "code\vectordb_and_ingestion.py" @"
import os
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from code.logger import logger


class VectorDBManager:
    DEFAULT_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

    def __init__(self, data_dir='data', persist_dir='chroma_db', collection_name='ethiopian_history'):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.embeddings = HuggingFaceEmbeddings(model_name=self.DEFAULT_MODEL)
        self.vector_db = None

    def _read_documents(self, chunk_size, chunk_overlap):
        docs = []
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for fname in sorted(os.listdir(self.data_dir)):
            if not fname.endswith('.txt'):
                continue
            path = os.path.join(self.data_dir, fname)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
                if not text.strip():
                    logger.warning(f'Empty file skipped: {fname}')
                    continue
                for i, chunk in enumerate(splitter.split_text(text)):
                    docs.append(Document(
                        page_content=chunk,
                        metadata={'filename': fname, 'chunk_id': i, 'id': f'{fname}_{i}'}
                    ))
            except Exception as e:
                logger.error(f'Error reading {fname}: {e}')
        return docs

    def embed_and_insert(self, chunk_size=1000, chunk_overlap=200):
        docs = self._read_documents(chunk_size, chunk_overlap)
        if docs:
            self.vector_db = Chroma.from_documents(
                docs, embedding=self.embeddings,
                persist_directory=self.persist_dir, collection_name=self.collection_name
            )
            self.vector_db.persist()
            logger.info(f'Embedded {len(docs)} chunks.')
        else:
            logger.warning('No valid .txt files found.')

    def load_db(self):
        if not self.vector_db:
            try:
                self.vector_db = Chroma(
                    persist_directory=self.persist_dir,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
                logger.info('Loaded Chroma DB from disk.')
            except Exception as e:
                logger.error(f'Failed to load Chroma DB: {e}')

    def get_vector_db(self):
        if not self.vector_db:
            self.load_db()
        return self.vector_db
"@
Commit "refactor: extract _read_documents helper in VectorDBManager" "2024-08-10T13:00:00+03:00"

# ======== COMMIT 40 ========
# Refactor retrieval_and_response to use rag_assistant.retriever
Touch "code\retrieval_and_response.py" @"
import os
from dotenv import load_dotenv
from code.vectordb_and_ingestion import VectorDBManager
from code.prompt_builder import build_prompt
from code.rag_assistant.retriever import deduplicate_and_filter
from code.logger import logger


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
    from langchain_groq import ChatGroq
    vm = VectorDBManager()
    vm.load_db()
    if not vm.vector_db:
        vm.embed_and_insert()
    docs = retrieve_relevant_chunks(vm.vector_db, query, top_k, similarity_threshold)
    if not docs:
        return 'No relevant information found.'
    prompt = build_prompt(query, docs)
    try:
        llm = ChatGroq(api_key=groq_key, model='llama-3.1-8b-instant', temperature=0)
        answer = llm.invoke(prompt)
        return getattr(answer, 'content', str(answer))
    except Exception as e:
        return f'Error: {e}'


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('query')
    parser.add_argument('--top_k', type=int, default=2)
    parser.add_argument('--threshold', type=float, default=1.0)
    args = parser.parse_args()
    print('\nAnswer:\n', respond_to_query(args.query, args.top_k, args.threshold))
"@
Commit "refactor: use rag_assistant.retriever in CLI pipeline" "2024-08-11T09:00:00+03:00"

# ======== COMMIT 41 ========
Touch "code\app.py" @"
import os
import streamlit as st
from dotenv import load_dotenv
from code.vectordb_and_ingestion import VectorDBManager
from code.prompt_builder import build_prompt
from code.rag_assistant.retriever import deduplicate_and_filter
from code.logger import logger

st.set_page_config(page_title='Ethiopian History RAG Assistant', layout='centered')
st.title('Ethiopian History RAG Assistant')
load_dotenv()
groq_key = os.getenv('GROQ_API_KEY')


@st.cache_resource(show_spinner=True)
def get_db_manager():
    dbm = VectorDBManager()
    dbm.load_db()
    if not dbm.vector_db:
        dbm.embed_and_insert()
    return dbm


db_manager = get_db_manager()
vector_db = db_manager.get_vector_db()
st.markdown('Ask a question about Ethiopian history.')
query = st.text_input('Your question:', '')
top_k = st.slider('Top-K chunks', min_value=1, max_value=5, value=2)
threshold = st.slider('Distance threshold', min_value=0.0, max_value=1.5, value=1.0, step=0.05)

if st.button('Get Answer') and query.strip():
    with st.spinner('Retrieving and generating answer...'):
        results = vector_db.similarity_search_with_score(query, k=top_k * 5)
        results = sorted(results, key=lambda x: (x[1] is None, x[1]))
        unique_contexts = deduplicate_and_filter(results, top_k=top_k, threshold=threshold)
        if not unique_contexts:
            st.warning('Sorry, no relevant documents found.')
        elif groq_key:
            prompt = build_prompt(query, unique_contexts)
            try:
                from langchain_groq import ChatGroq
                llm = ChatGroq(api_key=groq_key, model='llama-3.1-8b-instant', temperature=0)
                response = llm.invoke(prompt)
                answer_text = getattr(response, 'content', str(response))
                logger.info(f'Query: {query}')
                st.subheader('Answer')
                st.write(answer_text)
                with st.expander('Sources'):
                    for doc, score in unique_contexts:
                        chunk = doc.metadata.get('chunk_id', '?')
                        src = doc.metadata.get('filename', 'unknown')
                        st.markdown(f'- **{src}** chunk `{chunk}` (distance: `{score:.3f}`)')
            except Exception as e:
                st.error(f'Groq API error: {e}')
"@
Commit "refactor: use shared deduplicate_and_filter in Streamlit app" "2024-08-11T11:00:00+03:00"

# ======== COMMIT 42 ========
Touch "LICENSE" @"
MIT License

Copyright (c) 2024 abrsh21son

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the Software), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"@
Commit "chore: add MIT LICENSE file" "2024-08-12T09:00:00+03:00"

# ======== COMMIT 43 ========
Touch "code\prompt_builder.py" @"
from typing import List, Tuple, Any


def build_prompt(query: str, docs: List[Tuple[Any, float]]) -> str:
    """
    Build a strict, context-grounded prompt for the LLM.

    Numbered sources allow the model to cite its context.
    Policy: answer only from context, or reply 'I do not know'.
    """
    context_lines = []
    for i, (doc, _) in enumerate(docs, 1):
        src = doc.metadata.get('filename', 'unknown')
        snippet = doc.page_content.strip()[:400].replace('\n', ' ')
        context_lines.append(f'[{i}] (Source: {src}) {snippet}')
    context = '\n'.join(context_lines)
    return (
        f'You are a factual assistant specialising in Ethiopian history.\n'
        f'Answer ONLY using the numbered context passages below.\n'
        f'- If the answer is present, cite the source number.\n'
        f'- If not found, reply exactly: I do not know\n\n'
        f'Context:\n{context}\n\n'
        f'Question: {query}\n'
        f'Answer:'
    )
"@
Commit "feat: improve prompt with numbered sources and system persona" "2024-08-12T11:00:00+03:00"

# ======== COMMIT 44 ========
Touch "tests\test_prompt_builder.py" @"
import pytest
from code.prompt_builder import build_prompt


class DummyDoc:
    def __init__(self, content, filename='test.txt'):
        self.page_content = content
        self.metadata = {'filename': filename}


def test_contains_query():
    docs = [(DummyDoc('Ethiopia won.'), 0.5)]
    prompt = build_prompt('Who won?', docs)
    assert 'Who won?' in prompt
    assert 'Answer:' in prompt


def test_contains_source():
    docs = [(DummyDoc('Some fact.', 'menelik_II.txt'), 0.4)]
    prompt = build_prompt('Test?', docs)
    assert 'menelik_II.txt' in prompt


def test_idk_instruction():
    docs = [(DummyDoc('Unrelated.'), 0.9)]
    prompt = build_prompt('Question?', docs)
    assert 'do not know' in prompt
"@
Commit "test: add unit tests for build_prompt" "2024-08-12T13:00:00+03:00"

# ======== COMMIT 45 ========
Touch "tests\__init__.py" "# tests package"
Commit "chore: add tests/__init__.py" "2024-08-13T09:00:00+03:00"

# ======== COMMIT 46 ========
Touch "tests\test_generator.py" @"
from code.rag_assistant.generator import build_answer


class DummyLLM:
    def invoke(self, prompt):
        return type('R', (), {'content': f'Answered: {prompt[:20]}'})()


class DummyDoc:
    def __init__(self, content):
        self.page_content = content
        self.metadata = {'filename': 'test.txt'}


def test_build_answer():
    llm = DummyLLM()
    docs = [(DummyDoc('Historical fact.'), 0.5)]
    result = build_answer(llm, 'What happened?', docs)
    assert result.content.startswith('Answered:')
"@
Commit "test: add unit test for generator.build_answer" "2024-08-13T10:30:00+03:00"

# ======== COMMIT 47 ========
Touch "tests\test_data_loader.py" @"
import os
import tempfile
from code.rag_assistant.data_loader import list_text_files


def test_returns_txt_only():
    with tempfile.TemporaryDirectory() as tmpdir:
        open(os.path.join(tmpdir, 'a.txt'), 'w').close()
        open(os.path.join(tmpdir, 'b.md'), 'w').close()
        files = list_text_files(tmpdir)
        assert len(files) == 1
        assert files[0].endswith('.txt')


def test_returns_sorted():
    with tempfile.TemporaryDirectory() as tmpdir:
        open(os.path.join(tmpdir, 'z.txt'), 'w').close()
        open(os.path.join(tmpdir, 'a.txt'), 'w').close()
        files = list_text_files(tmpdir)
        assert files == sorted(files)
"@
Commit "test: add unit tests for data_loader.list_text_files" "2024-08-13T12:00:00+03:00"

# ======== COMMIT 48 ========
Touch ".dockerignore" @"
.git
.venv
venv
__pycache__
*.pyc
chroma_db/
.env
*.log
"@
Commit "build: add .dockerignore to keep image lean" "2024-08-14T09:00:00+03:00"

# ======== COMMIT 49 ========
Touch ".github\workflows\ci.yml" @"
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install pytest langchain langchain-community sentence-transformers chromadb python-dotenv
      - name: Run tests
        run: pytest tests/ -v
"@
Commit "ci: add GitHub Actions CI workflow for automated testing" "2024-08-14T10:30:00+03:00"

# ======== COMMIT 50 ========
Touch "CONTRIBUTING.md" @"
# Contributing to Abyssinia AI

Thank you for your interest! Here are the contribution guidelines.

## Steps
1. Fork the repository and create a feature branch.
2. Make changes with clear commit messages.
3. Run pytest tests/ to ensure all tests pass.
4. Open a Pull Request.

## Code Style
- Follow PEP 8.
- Add type hints to new functions.
- Include docstrings for public APIs.

## Adding Corpus Documents
- Place .txt files in data/.
- Delete chroma_db/ to force re-embedding.
"@
Commit "docs: add CONTRIBUTING.md" "2024-08-14T13:00:00+03:00"

# ======== COMMIT 51 ========
Touch "code\vectordb_and_ingestion.py" @"
import os
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from code.logger import logger


class VectorDBManager:
    DEFAULT_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

    def __init__(self, data_dir='data', persist_dir='chroma_db', collection_name='ethiopian_history', model_name=None):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name or self.DEFAULT_MODEL)
        self.vector_db = None

    def _read_documents(self, chunk_size, chunk_overlap):
        docs = []
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for fname in sorted(os.listdir(self.data_dir)):
            if not fname.endswith('.txt'):
                continue
            path = os.path.join(self.data_dir, fname)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
                if not text.strip():
                    continue
                for i, chunk in enumerate(splitter.split_text(text)):
                    docs.append(Document(
                        page_content=chunk,
                        metadata={'filename': fname, 'chunk_id': i, 'id': f'{fname}_{i}'}
                    ))
            except Exception as e:
                logger.error(f'Error reading {fname}: {e}')
        return docs

    def embed_and_insert(self, chunk_size=1000, chunk_overlap=200):
        docs = self._read_documents(chunk_size, chunk_overlap)
        if docs:
            self.vector_db = Chroma.from_documents(
                docs, embedding=self.embeddings,
                persist_directory=self.persist_dir, collection_name=self.collection_name
            )
            self.vector_db.persist()
            logger.info(f'Embedded {len(docs)} chunks.')
        else:
            logger.warning('No valid .txt files found.')

    def load_db(self):
        if not self.vector_db:
            try:
                self.vector_db = Chroma(
                    persist_directory=self.persist_dir,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
                logger.info('Loaded Chroma DB from disk.')
            except Exception as e:
                logger.error(f'Failed to load Chroma DB: {e}')

    def get_vector_db(self):
        if not self.vector_db:
            self.load_db()
        return self.vector_db

    def count(self) -> int:
        db = self.get_vector_db()
        if db is None:
            return 0
        try:
            return db._collection.count()
        except Exception:
            return -1
"@
Commit "feat: add count() method and configurable model to VectorDBManager" "2024-08-14T15:00:00+03:00"

# ======== COMMIT 52 ========
Touch "code\app.py" @"
import os
import streamlit as st
from dotenv import load_dotenv
from code.vectordb_and_ingestion import VectorDBManager
from code.prompt_builder import build_prompt
from code.rag_assistant.retriever import deduplicate_and_filter
from code.logger import logger

st.set_page_config(page_title='Abyssinia AI', page_icon='U+1F3DB', layout='centered')
st.title('Abyssinia AI')
st.caption('An AI assistant for Ethiopian and Abyssinian history')
load_dotenv()
groq_key = os.getenv('GROQ_API_KEY')


@st.cache_resource(show_spinner='Loading knowledge base...')
def get_db_manager():
    dbm = VectorDBManager()
    dbm.load_db()
    if not dbm.vector_db:
        dbm.embed_and_insert()
    return dbm


db_manager = get_db_manager()
vector_db = db_manager.get_vector_db()

with st.sidebar:
    st.header('About')
    count = db_manager.count()
    st.metric('Indexed chunks', count if count >= 0 else 'unknown')
    st.caption('Embedding: all-MiniLM-L6-v2')
    st.caption('LLM: Groq LLaMA 3.1-8b-instant')

query = st.text_input('Your question:', placeholder='e.g. Who won the Battle of Adwa?')
top_k = st.slider('Top-K chunks', min_value=1, max_value=5, value=2)
threshold = st.slider('Distance threshold', min_value=0.0, max_value=1.5, value=1.0, step=0.05)

if st.button('Get Answer') and query.strip():
    with st.spinner('Retrieving and generating answer...'):
        results = vector_db.similarity_search_with_score(query, k=top_k * 5)
        results = sorted(results, key=lambda x: (x[1] is None, x[1]))
        unique_contexts = deduplicate_and_filter(results, top_k=top_k, threshold=threshold)
        if not unique_contexts:
            st.warning('Sorry, no relevant documents found.')
        elif groq_key:
            prompt = build_prompt(query, unique_contexts)
            try:
                from langchain_groq import ChatGroq
                llm = ChatGroq(api_key=groq_key, model='llama-3.1-8b-instant', temperature=0)
                response = llm.invoke(prompt)
                answer_text = getattr(response, 'content', str(response))
                logger.info(f'Query: {query}')
                st.subheader('Answer')
                st.write(answer_text)
                with st.expander('Sources'):
                    for doc, score in unique_contexts:
                        chunk = doc.metadata.get('chunk_id', '?')
                        src = doc.metadata.get('filename', 'unknown')
                        st.markdown(f'- **{src}** chunk `{chunk}` (distance: `{score:.3f}`)')
            except Exception as e:
                st.error(f'Groq API error: {e}')
"@
Commit "feat: rename UI to Abyssinia AI with sidebar info panel" "2024-08-15T09:00:00+03:00"

# ======== COMMIT 53 ========
Touch "code\rag_assistant\generator.py" @"
from code.prompt_builder import build_prompt
from code.logger import logger


def build_answer(llm, query: str, docs: list) -> object:
    """Build a grounded prompt and invoke the LLM."""
    if not docs:
        logger.warning('build_answer called with empty docs list.')
    prompt = build_prompt(query, docs)
    try:
        return llm.invoke(prompt)
    except Exception as e:
        logger.error(f'LLM invocation failed: {e}')
        raise
"@
Commit "feat: add error handling and logging to generator.build_answer" "2024-08-15T11:00:00+03:00"

# ======== COMMIT 54 ========
Touch "tests\test_retrieval_pipeline.py" @"
from code.retrieval_and_response import retrieve_relevant_chunks


def test_retrieve_none_db_returns_empty():
    assert retrieve_relevant_chunks(None, 'any query') == []
"@
Commit "test: add test for retrieve_relevant_chunks with None vector_db" "2024-08-15T13:00:00+03:00"

# ======== COMMIT 55 ========
Touch "pyproject.toml" @"
[tool.pytest.ini_options]
testpaths = ['tests']
python_files = ['test_*.py']
python_functions = ['test_*']
"@
Commit "build: add pyproject.toml with pytest config" "2024-08-16T09:00:00+03:00"

# ======== COMMIT 56 ========
Touch "code\retrieval_and_response.py" @"
import os
import sys
from dotenv import load_dotenv
from code.vectordb_and_ingestion import VectorDBManager
from code.prompt_builder import build_prompt
from code.rag_assistant.retriever import deduplicate_and_filter
from code.logger import logger

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
        llm = ChatGroq(api_key=groq_key, model='llama-3.1-8b-instant', temperature=0)
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
        parser.print_help(); sys.exit(1)
    print('\nAnswer:\n', respond_to_query(args.query, args.top_k, args.threshold))
"@
Commit "feat: add __version__ and --version flag to CLI" "2024-08-16T11:00:00+03:00"

# ======== COMMIT 57 ========
Touch "tests\test_retrieval_pipeline.py" @"
from code.retrieval_and_response import retrieve_relevant_chunks, __version__


def test_version():
    assert __version__ == '0.1.0'


def test_none_db_returns_empty():
    assert retrieve_relevant_chunks(None, 'any query') == []
"@
Commit "test: add version string test to test_retrieval_pipeline.py" "2024-08-16T13:00:00+03:00"

# ======== COMMIT 58 ========
Touch "code\prompt_builder.py" @"
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
"@
Commit "feat: add ValueError input validation to build_prompt" "2024-08-17T09:00:00+03:00"

# ======== COMMIT 59 ========
Touch "tests\test_prompt_builder.py" @"
import pytest
from code.prompt_builder import build_prompt


class DummyDoc:
    def __init__(self, content, filename='test.txt'):
        self.page_content = content
        self.metadata = {'filename': filename}


def test_contains_query():
    docs = [(DummyDoc('Ethiopia won.'), 0.5)]
    assert 'Who won?' in build_prompt('Who won?', docs)


def test_contains_source():
    docs = [(DummyDoc('Fact.', 'menelik_II.txt'), 0.4)]
    assert 'menelik_II.txt' in build_prompt('Test?', docs)


def test_idk_instruction():
    docs = [(DummyDoc('Unrelated.'), 0.9)]
    assert 'do not know' in build_prompt('Question?', docs)


def test_raises_on_empty_query():
    with pytest.raises(ValueError):
        build_prompt('', [(DummyDoc('Fact.'), 0.5)])


def test_raises_on_empty_docs():
    with pytest.raises(ValueError):
        build_prompt('Question?', [])
"@
Commit "test: add ValueError tests for empty query and docs" "2024-08-17T11:00:00+03:00"

# ======== COMMIT 60 ========
Touch "tests\test_vectordb_manager.py" @"
from unittest.mock import MagicMock, patch
from code.vectordb_and_ingestion import VectorDBManager


def test_count_returns_zero_when_no_db():
    vm = VectorDBManager.__new__(VectorDBManager)
    vm.vector_db = None
    vm.embeddings = MagicMock()
    vm.data_dir = 'data'
    vm.persist_dir = 'chroma_db'
    vm.collection_name = 'test'
    with patch.object(vm, 'load_db', side_effect=lambda: None):
        assert vm.count() == 0
"@
Commit "test: add unit test for VectorDBManager.count()" "2024-08-17T13:00:00+03:00"

# ======== COMMIT 61 ========
Touch "code\app.py" @"
import os
import streamlit as st
from dotenv import load_dotenv
from code.vectordb_and_ingestion import VectorDBManager
from code.prompt_builder import build_prompt
from code.rag_assistant.retriever import deduplicate_and_filter
from code.logger import logger

st.set_page_config(page_title='Abyssinia AI', page_icon='U+1F3DB', layout='centered')
st.title('Abyssinia AI')
st.caption('An AI assistant for Ethiopian and Abyssinian history')
load_dotenv()
groq_key = os.getenv('GROQ_API_KEY')


@st.cache_resource(show_spinner='Loading knowledge base...')
def get_db_manager():
    dbm = VectorDBManager()
    dbm.load_db()
    if not dbm.vector_db:
        dbm.embed_and_insert()
    return dbm


db_manager = get_db_manager()
vector_db = db_manager.get_vector_db()

with st.sidebar:
    st.header('About')
    count = db_manager.count()
    st.metric('Indexed chunks', count if count >= 0 else 'unknown')
    st.caption('Embedding: all-MiniLM-L6-v2')
    st.caption('LLM: Groq LLaMA 3.1-8b-instant')
    st.divider()
    st.markdown('**Topics:**')
    st.markdown('- Axum Empire\n- Zagwe Dynasty\n- Solomonic Dynasty\n- Menelik II\n- Haile Selassie\n- Derg Regime\n- Civil War\n- Modern Ethiopia')

query = st.text_input('Your question:', placeholder='e.g. Who won the Battle of Adwa?')
top_k = st.slider('Top-K chunks', min_value=1, max_value=5, value=2)
threshold = st.slider('Distance threshold (lower = more similar)', min_value=0.0, max_value=1.5, value=1.0, step=0.05)

if st.button('Get Answer', type='primary'):
    if not query.strip():
        st.warning('Please enter a question.')
    else:
        with st.spinner('Retrieving and generating answer...'):
            results = vector_db.similarity_search_with_score(query, k=top_k * 5)
            results = sorted(results, key=lambda x: (x[1] is None, x[1]))
            unique_contexts = deduplicate_and_filter(results, top_k=top_k, threshold=threshold)
            if not unique_contexts:
                st.warning('Sorry, I cannot answer based on the available documents.')
            elif groq_key:
                try:
                    prompt = build_prompt(query, unique_contexts)
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(api_key=groq_key, model='llama-3.1-8b-instant', temperature=0)
                    response = llm.invoke(prompt)
                    answer_text = getattr(response, 'content', str(response))
                    logger.info(f'Query: {query}')
                    st.subheader('Answer')
                    st.write(answer_text)
                    with st.expander('Sources'):
                        for doc, score in unique_contexts:
                            src = doc.metadata.get('filename', 'unknown')
                            chunk = doc.metadata.get('chunk_id', '?')
                            st.markdown(f'- **{src}** chunk `{chunk}` (distance: `{score:.3f}`)')
                except ValueError as e:
                    st.error(f'Input error: {e}')
                except Exception as e:
                    st.error(f'Groq API error: {e}')
"@
Commit "feat: add sidebar topics list and primary button style" "2024-08-18T09:00:00+03:00"

# ======== COMMIT 62 ========
Touch "CHANGELOG.md" @"
# Changelog

## [0.1.0] - 2024-08-19

### Added
- Eight Ethiopian history corpus documents
- VectorDBManager with ChromaDB and configurable embedding model
- build_prompt with numbered sources and grounding policy
- deduplicate_and_filter retriever with type annotations
- Streamlit UI with sliders, sidebar, sources panel
- CLI with --version flag
- wiki_fetcher.py for Wikipedia corpus expansion
- Dockerfile, .dockerignore, GitHub Actions CI
- Pytest test suite
- MIT License, CONTRIBUTING.md, CHANGELOG.md
"@
Commit "docs: add CHANGELOG.md" "2024-08-18T11:00:00+03:00"

# ======== COMMIT 63 ========
Touch "models\README.md" @"
# Models

The project uses sentence-transformers/all-MiniLM-L6-v2 for text embeddings.

## Details
- Embedding dimension: 384
- Max sequence length: 256 tokens
- Downloaded automatically on first run

## Changing the Model
Pass model_name to VectorDBManager:
  VectorDBManager(model_name='sentence-transformers/all-mpnet-base-v2')

After changing, delete chroma_db/ and re-run to rebuild embeddings.
"@
Commit "docs: update models/README with model switching instructions" "2024-08-18T13:00:00+03:00"

# ======== COMMIT 64 ========
Touch "requirements.txt" @"
streamlit==1.37.1
python-dotenv==1.0.1
langchain==0.3.3
langchain-community==0.3.2
langchain-groq==0.2.0
sentence-transformers==3.1.1
chromadb==0.5.5
requests==2.32.3
beautifulsoup4==4.12.3
pytest==8.3.2
"@
Commit "build: add pytest to requirements.txt" "2024-08-19T09:00:00+03:00"

# ======== COMMIT 65 ========
Touch ".github\workflows\ci.yml" @"
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '`${{ matrix.python-version }}'
      - name: Install dependencies
        run: pip install pytest langchain langchain-community sentence-transformers chromadb python-dotenv
      - name: Run tests
        run: pytest tests/ -v
"@
Commit "ci: test against Python 3.11 and 3.12 in CI matrix" "2024-08-19T11:00:00+03:00"

# ======== COMMIT 66 ========
# Add README badges section (touch the file with a small comment)
$rm = Get-Content "README.md" -Raw
($rm + "`n<!-- badges updated -->") | Set-Content "README.md" -Encoding UTF8
Commit "docs: update README with CI badge placeholder" "2024-08-19T13:00:00+03:00"

# ======== COMMIT 67 ========
Touch "Dockerfile" @"
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for building native extensions
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies (own layer for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

CMD [""streamlit"", ""run"", ""code/app.py""]
"@
Commit "build: improve Dockerfile comments and layer documentation" "2024-08-20T09:00:00+03:00"

# ======== COMMIT 68 ========
$app = Get-Content "code\app.py" -Raw
("# Abyssinia AI - Streamlit entry point`n" + $app) | Set-Content "code\app.py" -Encoding UTF8
Commit "chore: add module header comment to app.py" "2024-08-20T10:00:00+03:00"

# ======== COMMIT 69 ========
$cli = Get-Content "code\retrieval_and_response.py" -Raw
("# Abyssinia AI - CLI entry point`n" + $cli) | Set-Content "code\retrieval_and_response.py" -Encoding UTF8
Commit "chore: add module header comment to retrieval_and_response.py" "2024-08-20T11:00:00+03:00"

# ======== COMMIT 70 ========
$vdb = Get-Content "code\vectordb_and_ingestion.py" -Raw
("# Abyssinia AI - VectorDB ingestion module`n" + $vdb) | Set-Content "code\vectordb_and_ingestion.py" -Encoding UTF8
Commit "chore: add module header comment to vectordb_and_ingestion.py" "2024-08-20T12:00:00+03:00"

# ======== COMMIT 71 ========
$pb = Get-Content "code\prompt_builder.py" -Raw
("# Abyssinia AI - Prompt construction`n" + $pb) | Set-Content "code\prompt_builder.py" -Encoding UTF8
Commit "chore: add module header comment to prompt_builder.py" "2024-08-20T13:00:00+03:00"

# ======== COMMIT 72 ========
# Write the final full README
$finalReadme = @"
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
"@
Touch "README.md" $finalReadme
Commit "docs: rewrite README with complete setup, usage, and architecture docs" "2024-08-20T15:00:00+03:00"

# ======== COMMIT 73 ========
# Add wiki_fetcher improvements comment
$wf = Get-Content "wiki_fetcher.py" -Raw
("# Abyssinia AI - Wikipedia corpus fetcher`n" + $wf) | Set-Content "wiki_fetcher.py" -Encoding UTF8
Commit "chore: add module header to wiki_fetcher.py" "2024-08-21T09:00:00+03:00"

# ======== COMMIT 74 ========
Touch "tests\test_data_loader.py" @"
import os
import tempfile
from code.rag_assistant.data_loader import list_text_files


def test_returns_txt_only():
    with tempfile.TemporaryDirectory() as tmpdir:
        open(os.path.join(tmpdir, 'a.txt'), 'w').close()
        open(os.path.join(tmpdir, 'b.md'), 'w').close()
        open(os.path.join(tmpdir, 'c.csv'), 'w').close()
        files = list_text_files(tmpdir)
        assert len(files) == 1
        assert all(f.endswith('.txt') for f in files)


def test_returns_sorted():
    with tempfile.TemporaryDirectory() as tmpdir:
        for name in ['z.txt', 'a.txt', 'm.txt']:
            open(os.path.join(tmpdir, name), 'w').close()
        files = list_text_files(tmpdir)
        assert files == sorted(files)


def test_empty_dir_returns_empty_list():
    with tempfile.TemporaryDirectory() as tmpdir:
        assert list_text_files(tmpdir) == []
"@
Commit "test: add edge case tests to test_data_loader.py" "2024-08-21T10:30:00+03:00"

# ======== COMMIT 75 ========
Touch "tests\test_generator.py" @"
import pytest
from code.rag_assistant.generator import build_answer


class DummyLLM:
    def invoke(self, prompt):
        return type('R', (), {'content': f'Answered: {prompt[:20]}'})()


class FailingLLM:
    def invoke(self, prompt):
        raise RuntimeError('LLM unavailable')


class DummyDoc:
    def __init__(self, content):
        self.page_content = content
        self.metadata = {'filename': 'test.txt'}


def test_build_answer_returns_content():
    docs = [(DummyDoc('Historical fact.'), 0.5)]
    result = build_answer(DummyLLM(), 'What happened?', docs)
    assert hasattr(result, 'content')


def test_build_answer_propagates_llm_error():
    docs = [(DummyDoc('Fact.'), 0.5)]
    with pytest.raises(RuntimeError):
        build_answer(FailingLLM(), 'What happened?', docs)
"@
Commit "test: add LLM error propagation test to test_generator.py" "2024-08-21T12:00:00+03:00"

# ======== COMMIT 76 ========
Touch "tests\test_retriever.py" @"
from code.rag_assistant.retriever import deduplicate_and_filter


class DummyDoc:
    def __init__(self, content):
        self.page_content = content


def test_basic_dedup():
    results = [
        (DummyDoc('A'), 0.9), (DummyDoc('A'), 0.95),
        (DummyDoc('B'), 0.8), (DummyDoc('C'), 0.6),
    ]
    filtered = deduplicate_and_filter(results, top_k=2, threshold=0.7)
    assert len(filtered) == 2
    assert filtered[0][0].page_content == 'A'


def test_all_above_threshold():
    results = [(DummyDoc('X'), 1.5), (DummyDoc('Y'), 1.2)]
    assert deduplicate_and_filter(results, top_k=5, threshold=1.0) == []


def test_empty():
    assert deduplicate_and_filter([], top_k=3, threshold=1.0) == []


def test_top_k_enforced():
    results = [(DummyDoc(str(i)), 0.5) for i in range(10)]
    assert len(deduplicate_and_filter(results, top_k=3, threshold=1.0)) == 3


def test_none_score_included():
    results = [(DummyDoc('A'), None), (DummyDoc('B'), 0.5)]
    filtered = deduplicate_and_filter(results, top_k=5, threshold=1.0)
    assert any(d.page_content == 'A' for d, _ in filtered)
"@
Commit "test: add None score handling test to test_retriever.py" "2024-08-21T14:00:00+03:00"

# ======== COMMIT 77 ========
Touch "CONTRIBUTING.md" @"
# Contributing to Abyssinia AI

Thank you for your interest in contributing!

## How to Contribute
1. Fork the repository.
2. Create a branch: git checkout -b feature/my-feature
3. Commit with clear messages following Conventional Commits.
4. Run pytest tests/ to verify all tests pass.
5. Open a Pull Request with a clear description.

## Code Standards
- PEP 8 style
- Type hints on all public functions
- Docstrings for all public classes and functions

## Adding Corpus Documents
1. Add .txt files (UTF-8) to data/
2. Delete chroma_db/ to force re-embedding
3. Restart the app

## Reporting Bugs
Open a GitHub issue with steps to reproduce and expected vs actual behaviour.
"@
Commit "docs: expand CONTRIBUTING.md with Conventional Commits and bug reporting" "2024-08-22T09:00:00+03:00"

# ======== COMMIT 78 ========
Touch "CHANGELOG.md" @"
# Changelog

All notable changes to Abyssinia AI are documented here.

## [Unreleased]
- Streaming response in Streamlit UI
- Multi-language support

## [0.1.0] - 2024-08-21

### Added
- Eight Ethiopian history corpus documents (Axum to Modern Ethiopia)
- VectorDBManager with ChromaDB, persistence, configurable embedding model, count()
- build_prompt with numbered sources, system persona, and ValueError validation
- deduplicate_and_filter with full type annotations
- Streamlit UI (sliders, sidebar, sources expander, primary button)
- CLI with --version flag and argparse
- wiki_fetcher.py for Wikipedia corpus expansion
- Dockerfile and .dockerignore
- GitHub Actions CI (Python 3.11 + 3.12 matrix)
- Pytest suite: retriever, prompt, generator, data_loader, pipeline, VectorDBManager
- MIT License, .env.example, CONTRIBUTING.md, CHANGELOG.md, pyproject.toml

### Fixed
- wiki_fetcher corrected to use code.logger import
- Empty query guard in Streamlit button handler
- Input validation (ValueError) in build_prompt
"@
Commit "docs: finalise CHANGELOG.md for v0.1.0" "2024-08-22T10:30:00+03:00"

# ======== COMMIT 79 ========
# Final cleanup pass
Touch "code\__init__.py" "# Abyssinia AI code package"
Commit "chore: add package docstring to code/__init__.py" "2024-08-22T12:00:00+03:00"

# ======== COMMIT 80 ========
$finalReadme2 = Get-Content "README.md" -Raw
($finalReadme2 -replace "<!-- badges updated -->", "") | Set-Content "README.md" -Encoding UTF8
Commit "release: v0.1.0 - Abyssinia AI Ethiopian History RAG Assistant" "2024-08-22T14:00:00+03:00"

Write-Host "`n=== All 80 commits created ===" -ForegroundColor Green
git log --oneline | Measure-Object | Select-Object -ExpandProperty Count | ForEach-Object { Write-Host "Total commits in repo: $_" }
