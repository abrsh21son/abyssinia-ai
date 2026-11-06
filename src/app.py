import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
from src.vectordb_and_ingestion import VectorDBManager
from src.prompt_builder import build_prompt
from src.rag_assistant.retriever import deduplicate_and_filter
from src.logger import logger

st.set_page_config(
    page_title="Abyssinia AI",
    page_icon="🏛️",
    layout="centered",
)

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.stApp { background-color:#F7F5F0; color:#26352E; font-family:'Inter',sans-serif; }
.block-container { max-width:820px; padding-top:2rem; padding-bottom:3rem; }
header[data-testid="stHeader"] { background:transparent; }
#MainMenu, footer { visibility:hidden; }

/* sidebar */
section[data-testid="stSidebar"] { background:#ECEEE8; border-right:1px solid #D5DBD0; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color:#1A4D35!important; }
section[data-testid="stSidebar"] p { color:#52645A; }
section[data-testid="stSidebar"] .stButton>button {
    background:transparent!important; color:#1A4D35!important;
    border:1px solid #BDC9B7!important; border-radius:8px!important;
    font-size:13px!important; text-align:left!important;
    padding:9px 14px!important; transition:all 0.18s!important;
}
section[data-testid="stSidebar"] .stButton>button:hover {
    background:#1A4D35!important; color:#fff!important;
    border-color:#1A4D35!important; transform:translateX(3px)!important;
}

/* headings */
h1 { color:#1A4D35!important; font-family:'Playfair Display',serif!important;
     text-align:center; font-size:40px!important; letter-spacing:-0.5px; }
h2, h3 { color:#1A4D35!important; }

/* input */
.stTextInput>div>div>input {
    background:#fff!important; color:#26352E!important;
    border:1.5px solid #CBD5C9!important; border-radius:12px!important;
    padding:14px 16px!important; font-size:15px!important;
    transition:border 0.2s!important;
}
.stTextInput>div>div>input:focus {
    border-color:#B28A3B!important;
    box-shadow:0 0 0 2px rgba(178,138,59,0.18)!important;
}
.stTextInput>div>div>input::placeholder { color:#A0ABA5!important; }

/* GOLD discovery button */
div[data-testid="stForm"] .stButton>button,
.gold-btn .stButton>button {
    background:linear-gradient(135deg,#C9A84C,#8F6420)!important;
    color:#fff!important; border:none!important;
    border-radius:12px!important; font-weight:700!important;
    font-size:15px!important; padding:14px!important;
    letter-spacing:0.3px!important; transition:all 0.2s!important;
}
div[data-testid="stForm"] .stButton>button:hover,
.gold-btn .stButton>button:hover {
    background:linear-gradient(135deg,#DEB95A,#C9A84C)!important;
    transform:translateY(-2px)!important;
    box-shadow:0 6px 20px rgba(178,138,59,0.30)!important;
}

/* slider gold thumb */
.stSlider [role="slider"] {
    background:#B28A3B!important; border-color:#B28A3B!important;
}

/* metrics */
[data-testid="stMetric"] {
    background:#fff; border:1px solid #DDE3D9; border-radius:10px; padding:14px;
}
[data-testid="stMetricValue"] { color:#1A4D35!important; }

/* expander */
[data-testid="stExpander"] {
    border:1px solid #DDE3D9!important; border-radius:10px!important;
    background:#fff!important;
}
.streamlit-expanderHeader { color:#1A4D35!important; font-weight:600!important; }

/* divider */
hr { border-color:#D9DFD5!important; }

/* chat bubbles */
.user-bubble {
    background:#fff;
    border:1px solid #D5DBD0;
    border-left:4px solid #B28A3B;
    border-radius:0 14px 14px 14px;
    padding:16px 20px; margin:14px 0 4px 0;
    font-size:15px; line-height:1.7; color:#26352E;
}
.ai-bubble {
    background:#F0F4ED;
    border:1px solid #CDD8C9;
    border-left:4px solid #1A4D35;
    border-radius:0 14px 14px 14px;
    padding:18px 22px; margin:4px 0 16px 0;
    font-size:15px; line-height:1.85; color:#1C2E24;
}
.label-you  { color:#B28A3B; font-size:12px; font-weight:700; margin-bottom:7px; }
.label-ai   { color:#1A4D35; font-size:12px; font-weight:700; margin-bottom:7px; }
.source-row {
    background:#fff; border:1px solid #DDE3D9;
    border-left:3px solid #B28A3B; border-radius:8px;
    padding:11px 14px; margin:6px 0; font-size:13px; color:#52645A;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "messages"      not in st.session_state: st.session_state.messages      = []
if "pending_query" not in st.session_state: st.session_state.pending_query = ""

# ── DB ─────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading knowledge base...")
def get_db_manager():
    dbm = VectorDBManager()
    dbm.load_db()
    if not dbm.vector_db:
        dbm.embed_and_insert()
    return dbm

db_manager = get_db_manager()
vector_db  = db_manager.get_vector_db()
count      = db_manager.count()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏛️ Abyssinia AI")
    st.caption("Ethiopian History Intelligence")
    st.divider()

    st.metric("Indexed chunks", count if count >= 0 else "–")
    st.caption("🧠 all-MiniLM-L6-v2")
    st.caption("⚡ Groq · GPT-OSS-20B")
    st.divider()

    # ── Retrieval settings live here — actionable next to topics ──
    st.markdown("### ⚙️ Retrieval Settings")
    st.caption("How many passages to retrieve and how closely they must match your question.")

    top_k = st.slider(
        "📄 Passages to retrieve",
        min_value=1, max_value=5, value=2,
        help="More passages = broader context. Start at 2."
    )
    threshold = st.slider(
        "🎯 Similarity threshold",
        min_value=0.0, max_value=1.5, value=1.0, step=0.05,
        help="Lower = only very close matches. 1.0 is a good default."
    )

    st.divider()
    st.markdown("### 📚 Explore Topics")
    st.caption("Click a topic to ask about it instantly.")

    topics = [
        ("🏰", "Axum Empire"),
        ("⛪", "Zagwe Dynasty"),
        ("👑", "Solomonic Dynasty"),
        ("⚔️", "Battle of Adwa"),
        ("🦁", "Menelik II"),
        ("🕊️", "Haile Selassie"),
        ("🔴", "Derg Regime"),
        ("🌍", "Ethiopian Civil War"),
        ("🇪🇹", "Modern Ethiopia"),
    ]
    for icon, topic in topics:
        if st.button(f"{icon}  {topic}", key=f"t_{topic}", use_container_width=True):
            st.session_state.pending_query = f"Tell me about {topic} in Ethiopian history."

    st.divider()
    if st.button("🗑️  Clear conversation", use_container_width=True, key="clear"):
        st.session_state.messages      = []
        st.session_state.pending_query = ""

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏛️ Abyssinia AI")
st.caption("An AI assistant for Ethiopian history")
st.markdown('<div style="width:60px;height:3px;background:#B28A3B;margin:10px auto 24px;border-radius:4px;"></div>', unsafe_allow_html=True)

# ── Suggested questions (only when chat is empty) ─────────────────────────────
if not st.session_state.messages:
    st.markdown('<p style="color:#52645A;font-size:13px;text-align:center;margin-bottom:12px;">✦ Start with a suggested question</p>', unsafe_allow_html=True)
    suggestions = [
        ("⚔️", "Who won the Battle of Adwa?"),
        ("🏰", "What made the Axum Empire powerful?"),
        ("🦁", "Who was Emperor Menelik II?"),
        ("⛪", "Tell me about the Zagwe Dynasty churches"),
        ("🕊️", "What was Haile Selassie's legacy?"),
        ("🔴", "How did the Derg regime fall?"),
    ]
    c1, c2 = st.columns(2)
    for i, (icon, q) in enumerate(suggestions):
        col = c1 if i % 2 == 0 else c2
        if col.button(f"{icon}  {q}", key=f"sug_{i}", use_container_width=True):
            st.session_state.pending_query = q
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-bubble">
            <div class="label-you">👤 YOU</div>
            {msg["content"]}
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="ai-bubble">
            <div class="label-ai">🏛️ ABYSSINIA AI</div>
            {msg["content"]}
        </div>""", unsafe_allow_html=True)
        if msg.get("sources"):
            with st.expander(f"📚 {len(msg['sources'])} source(s) used"):
                for src in msg["sources"]:
                    st.markdown(f"""
                    <div class="source-row">
                        📄 <b>{src['filename']}</b>
                        &nbsp;·&nbsp; chunk {src['chunk']}
                        &nbsp;·&nbsp; distance {src['score']:.3f}
                    </div>""", unsafe_allow_html=True)

# ── Input — question + button side by side in one form ────────────────────────
st.markdown("---")
default_q = st.session_state.pop("pending_query", "") or ""

with st.form("ask_form", clear_on_submit=True):
    q_col, btn_col = st.columns([5, 1])
    with q_col:
        query = st.text_input(
            "q",
            value=default_q,
            placeholder="Ask anything about Ethiopian history...",
            label_visibility="collapsed",
        )
    with btn_col:
        submitted = st.form_submit_button("✦ Discoveries", use_container_width=True)

# ── Answer logic ──────────────────────────────────────────────────────────────
if submitted:
    if not query.strip():
        st.markdown("""
        <div style="background:#FFF8EC;border:1px solid #E5C96A;border-radius:10px;
                    padding:13px 16px;color:#7A5C1E;font-size:14px;margin-top:8px;">
            ✦ Please type a question and click <b>Discoveries</b>.
        </div>""", unsafe_allow_html=True)
    elif not groq_key:
        st.error("GROQ_API_KEY is not set. Add it in Streamlit Cloud → Secrets.")
    else:
        with st.spinner("🔍 Searching the historical archives..."):
            try:
                results = vector_db.similarity_search_with_score(query, k=top_k * 5)
                results = sorted(
                    results,
                    key=lambda x: (x[1] is None, x[1] if x[1] is not None else float("inf"))
                )
                unique_contexts = deduplicate_and_filter(results, top_k=top_k, threshold=threshold)

                if not unique_contexts:
                    st.markdown("""
                    <div style="background:#F5F3EE;border:1px solid #CDD8C9;border-radius:10px;
                                padding:16px 20px;color:#52645A;font-size:14px;">
                        🏛️ No relevant passages found. Try rephrasing or lower the similarity threshold in the sidebar.
                    </div>""", unsafe_allow_html=True)
                else:
                    prompt = build_prompt(query, unique_contexts)
                    from langchain_groq import ChatGroq
                    llm        = ChatGroq(api_key=groq_key, model="openai/gpt-oss-20b", temperature=0)
                    response   = llm.invoke(prompt)
                    answer_txt = getattr(response, "content", str(response))
                    logger.info(f"Query: {query}")

                    sources = [
                        {"filename": doc.metadata.get("filename", "unknown"),
                         "chunk":    doc.metadata.get("chunk_id", "?"),
                         "score":    score}
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

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:28px 0 8px;color:#A0ABA5;font-size:12px;">
    <span style="color:#B28A3B;font-size:16px;">🏛️</span>
    &nbsp; Abyssinia AI · Preserving Ethiopian History · Powered by RAG + Groq
</div>""", unsafe_allow_html=True)
