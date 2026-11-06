import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
from src.vectordb_and_ingestion import VectorDBManager
from src.prompt_builder import build_prompt
from src.rag_assistant.retriever import deduplicate_and_filter
from src.logger import logger

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Abyssinia AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --gold: #D5AC58;
    --gold-light: #F2D99A;
    --navy: #0B1020;
    --surface: #151D30;
    --text: #F4F0E8;
    --muted: #9BA8BD;
}
.stApp {
    background: radial-gradient(ellipse at 80% 0%, rgba(213,172,88,0.10), transparent 40%), #0B1020;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1100px; padding-top: 2rem; padding-bottom: 3rem; }
#MainMenu, footer { visibility: hidden; }

section[data-testid="stSidebar"] {
    background: #10182A;
    border-right: 1px solid rgba(213,172,88,0.18);
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: var(--gold-light); }

.hero {
    position: relative;
    padding: 48px 38px;
    border-radius: 22px;
    border: 1px solid rgba(213,172,88,0.25);
    background: linear-gradient(120deg, rgba(213,172,88,0.13), rgba(21,29,48,0.96));
    margin-bottom: 30px;
    overflow: hidden;
}
.hero-tag {
    display: inline-block;
    color: var(--gold-light);
    background: rgba(213,172,88,0.12);
    border: 1px solid rgba(213,172,88,0.3);
    border-radius: 30px;
    padding: 7px 14px;
    font-size: 11px;
    letter-spacing: 2px;
    margin-bottom: 18px;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(28px, 4vw, 48px);
    color: var(--gold-light);
    line-height: 1.2;
    margin: 0;
}
.hero p { color: #B4BED0; font-size: 15px; line-height: 1.9; max-width: 650px; margin-top: 15px; }
.hero-icon { position: absolute; right: 35px; top: 30px; font-size: 100px; opacity: 0.16; }

[data-testid="stMetric"] {
    background: #151D30;
    border: 1px solid rgba(213,172,88,0.17);
    border-radius: 14px;
    padding: 17px;
}
[data-testid="stMetricValue"] { color: var(--gold-light); }
[data-testid="stMetricLabel"] { color: #AEB9CA; }

.stButton > button {
    background: linear-gradient(135deg, #D9B66C, #AD813A);
    color: #111827;
    border: none;
    border-radius: 11px;
    font-weight: 700;
    transition: 0.2s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #F2D99A, #D5AC58);
    color: #111827;
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(213,172,88,0.18);
}

.stTextInput input {
    background: #151D30 !important;
    color: white !important;
    border: 1px solid #34415B !important;
    border-radius: 12px !important;
    padding: 14px !important;
}
.stTextInput input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 1px var(--gold) !important;
}

.user-bubble {
    background: rgba(213,172,88,0.12);
    border: 1px solid rgba(213,172,88,0.24);
    border-radius: 15px 15px 4px 15px;
    padding: 17px 20px;
    margin: 15px 0 15px 12%;
    line-height: 1.8;
}
.ai-bubble {
    background: #151D30;
    border: 1px solid #2B3851;
    border-radius: 15px 15px 15px 4px;
    padding: 22px;
    margin: 15px 5% 15px 0;
    line-height: 1.9;
}
.msg-label { color: var(--gold-light); font-size: 13px; font-weight: 700; margin-bottom: 10px; }

.source-card {
    background: #10182A;
    border: 1px solid #293750;
    border-left: 3px solid var(--gold);
    border-radius: 9px;
    padding: 13px;
    margin: 9px 0;
    color: #C3CDDD;
    font-size: 13px;
}

.section-title {
    color: var(--gold-light);
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 12px;
}
hr { border-color: rgba(213,172,88,0.17); }

@media(max-width:700px) {
    .hero { padding: 30px 22px; }
    .hero-icon { display: none; }
    .user-bubble { margin-left: 3%; }
    .ai-bubble { margin-right: 2%; }
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = ""

# ── DB ─────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading historical knowledge base...")
def get_db_manager():
    dbm = VectorDBManager()
    dbm.load_db()
    if not dbm.vector_db:
        dbm.embed_and_insert()
    return dbm

db_manager = get_db_manager()
vector_db   = db_manager.get_vector_db()
count       = db_manager.count()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 5px 10px;">
        <div style="font-size:44px;">🏛️</div>
        <h2 style="color:#F2D99A;margin:5px 0;font-size:18px;">ABYSSINIA AI</h2>
        <p style="color:#8F9BB0;font-size:10px;letter-spacing:2px;">ETHIOPIAN HISTORY INTELLIGENCE</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📊 Knowledge Base")
    st.metric("Indexed Chunks", count if count >= 0 else "Unknown")
    st.caption("🧠 all-MiniLM-L6-v2")
    st.caption("⚡ Groq · GPT-OSS-20B")

    st.divider()
    st.markdown("### ⚙️ Retrieval Settings")
    top_k     = st.slider("Number of passages", 1, 5, 2)
    threshold = st.slider("Distance threshold", 0.0, 1.5, 1.0, 0.05)
    st.caption("Lower distance = more similar.")

    st.divider()
    st.markdown("### 📚 Explore Ethiopian History")

    topics = [
        "Axum Empire", "Zagwe Dynasty", "Solomonic Dynasty",
        "Menelik II", "Battle of Adwa", "Haile Selassie",
        "Derg Regime", "Ethiopian Civil War", "Modern Ethiopia",
    ]
    for topic in topics:
        if st.button(f"✦ {topic}", key=f"topic_{topic}", use_container_width=True):
            st.session_state.pending_query = f"Explain the history and significance of {topic}."

    st.divider()
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_query = ""

    st.markdown("""
    <div style="text-align:center;color:#718096;font-size:11px;padding:20px 5px;">
        Preserving the past.<br>Exploring the future.
    </div>
    """, unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-icon">🏛️</div>
    <div class="hero-tag">✦ YOUR ETHIOPIAN HISTORY COMPANION</div>
    <h1>Discover the Story of Ethiopia.</h1>
    <p>
        From the ancient Kingdom of Aksum to modern Ethiopia,
        explore the emperors, civilisations, battles and events that shaped
        one of Africa's oldest histories. Ask questions. Discover knowledge.
    </p>
</div>
""", unsafe_allow_html=True)



# ── Suggested questions ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">✨ Start Exploring</div>', unsafe_allow_html=True)
st.caption("Choose a question to begin your historical journey.")

suggestions = [
    "Who won the Battle of Adwa?",
    "What made the Axum Empire powerful?",
    "Who was Emperor Menelik II?",
    "How did the Derg regime end?",
]
s_cols = st.columns(2)
for i, s in enumerate(suggestions):
    if s_cols[i % 2].button(f"✦ {s}", key=f"sug_{i}", use_container_width=True):
        st.session_state.pending_query = s

st.divider()

# ── Chat history ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">💬 Historical Research Assistant</div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-bubble"><div class="msg-label">👤 YOU</div>{msg["content"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="ai-bubble"><div class="msg-label">🏛️ ABYSSINIA AI</div>{msg["content"]}</div>',
            unsafe_allow_html=True,
        )
        if msg.get("sources"):
            with st.expander(f"📚 View {len(msg['sources'])} historical source(s)"):
                for src in msg["sources"]:
                    st.markdown(
                        f'<div class="source-card"><b>📄 {src["filename"]}</b><br>'
                        f'Chunk: {src["chunk"]} &nbsp;|&nbsp; Distance: {src["score"]:.3f}</div>',
                        unsafe_allow_html=True,
                    )

# ── Input form ─────────────────────────────────────────────────────────────────
st.markdown("---")

# Pre-fill the text box from pending_query (set by buttons) without rerun
default_query = st.session_state.pop("pending_query", "") or ""

with st.form("ask_form", clear_on_submit=True):
    query = st.text_input(
        "question",
        value=default_query,
        placeholder="Ask anything about Ethiopian history...",
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button(
        "🏛️ Discover History",
        type="primary",
        use_container_width=True,
    )

# ── Answer logic ───────────────────────────────────────────────────────────────
if submitted and query.strip():
    if not groq_key:
        st.error("GROQ_API_KEY is not set. Add it in Streamlit Cloud secrets.")
    else:
        with st.spinner("🔍 Searching Ethiopia's historical archives..."):
            try:
                results = vector_db.similarity_search_with_score(query, k=top_k * 5)
                results = sorted(results, key=lambda x: (x[1] is None, x[1] if x[1] is not None else float("inf")))
                unique_contexts = deduplicate_and_filter(results, top_k=top_k, threshold=threshold)

                if not unique_contexts:
                    st.warning("No relevant documents found for that question.")
                else:
                    prompt = build_prompt(query, unique_contexts)
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(api_key=groq_key, model="openai/gpt-oss-20b", temperature=0)
                    response   = llm.invoke(prompt)
                    answer_txt = getattr(response, "content", str(response))
                    logger.info(f"Query: {query}")

                    sources = [
                        {
                            "filename": doc.metadata.get("filename", "unknown"),
                            "chunk":    doc.metadata.get("chunk_id", "?"),
                            "score":    score,
                        }
                        for doc, score in unique_contexts
                    ]

                    st.session_state.messages.append({"role": "user",      "content": query})
                    st.session_state.messages.append({"role": "assistant", "content": answer_txt, "sources": sources})
                    st.rerun()

            except ValueError as e:
                st.error(f"Input error: {e}")
            except Exception as e:
                logger.exception("Answer generation failed")
                st.error(f"Groq API error: {e}")

elif submitted:
    st.warning("Please enter a question.")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;padding:20px 5px;color:#8490A5;">
    <div style="font-size:22px;color:#D5AC58;">🏛️ ABYSSINIA AI</div>
    <p style="margin:6px 0;font-size:13px;">Preserving the past. Exploring the future.</p>
    <p style="font-size:11px;margin:0;">Powered by Retrieval-Augmented Generation</p>
</div>
""", unsafe_allow_html=True)
