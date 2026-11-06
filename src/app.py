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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --gold:      #C9A84C;
    --gold-lite: #E8C97A;
    --gold-dim:  rgba(201,168,76,0.15);
    --bg:        #080E1A;
    --bg2:       #0F1826;
    --bg3:       #162030;
    --border:    rgba(201,168,76,0.20);
    --text:      #EAE6DC;
    --muted:     #7A8899;
}

/* ── base ── */
html, body, .stApp {
    background: var(--bg) !important;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}
.block-container {
    padding: 1.5rem 2.5rem 3rem !important;
    max-width: 900px !important;
}
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden !important; }

/* ── sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── buttons (sidebar topics) ── */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    text-align: left !important;
    padding: 9px 14px !important;
    margin-bottom: 4px !important;
    transition: all 0.18s ease !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--gold-dim) !important;
    border-color: var(--gold) !important;
    color: var(--gold-lite) !important;
    transform: translateX(4px) !important;
}

/* ── clear button ── */
.clear-btn > button {
    background: rgba(255,80,80,0.08) !important;
    border: 1px solid rgba(255,80,80,0.25) !important;
    color: #ff8080 !important;
    border-radius: 8px !important;
}
.clear-btn > button:hover {
    background: rgba(255,80,80,0.18) !important;
}

/* ── main input ── */
.stTextInput > div > div > input {
    background: var(--bg3) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 16px 18px !important;
    font-size: 15px !important;
    transition: border 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.18) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }

/* ── submit button ── */
div[data-testid="stForm"] .stButton > button {
    background: linear-gradient(135deg, var(--gold), #9B6E20) !important;
    color: #0a0e17 !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 14px !important;
    letter-spacing: 0.4px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stForm"] .stButton > button:hover {
    background: linear-gradient(135deg, var(--gold-lite), var(--gold)) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(201,168,76,0.25) !important;
}

/* ── expander ── */
details { background: var(--bg3) !important; border-radius: 10px !important; border: 1px solid var(--border) !important; }
summary { color: var(--gold-lite) !important; font-size: 13px !important; }

/* ── scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* ── divider ── */
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }
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
    st.markdown("""
    <div style="text-align:center;padding:24px 8px 16px;">
        <div style="font-size:46px;line-height:1;">🏛️</div>
        <div style="font-family:'Playfair Display',serif;font-size:20px;
                    color:#E8C97A;font-weight:700;margin:10px 0 4px;">
            Abyssinia AI
        </div>
        <div style="color:#556070;font-size:11px;letter-spacing:2.5px;">
            HISTORY INTELLIGENCE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(f"""
    <div style="display:flex;gap:10px;margin-bottom:16px;">
        <div style="flex:1;background:#0F1826;border:1px solid rgba(201,168,76,0.2);
                    border-radius:10px;padding:12px;text-align:center;">
            <div style="color:#E8C97A;font-size:22px;font-weight:700;">{count if count >= 0 else '—'}</div>
            <div style="color:#556070;font-size:11px;margin-top:2px;">Chunks</div>
        </div>
        <div style="flex:1;background:#0F1826;border:1px solid rgba(201,168,76,0.2);
                    border-radius:10px;padding:12px;text-align:center;">
            <div style="color:#E8C97A;font-size:22px;font-weight:700;">{len(st.session_state.messages)//2}</div>
            <div style="color:#556070;font-size:11px;margin-top:2px;">Asked</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#556070;font-size:11px;margin-bottom:16px;">
        🧠 MiniLM-L6-v2 &nbsp;·&nbsp; ⚡ Groq GPT-OSS-20B
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="color:#E8C97A;font-size:13px;font-weight:600;
                letter-spacing:1px;margin-bottom:10px;">
        📚 EXPLORE TOPICS
    </div>
    """, unsafe_allow_html=True)

    topics = [
        ("🏰", "Axum Empire"),
        ("⛪", "Zagwe Dynasty"),
        ("👑", "Solomonic Dynasty"),
        ("⚔️",  "Battle of Adwa"),
        ("🦁", "Menelik II"),
        ("🕊️",  "Haile Selassie"),
        ("🔴", "Derg Regime"),
        ("🌍", "Ethiopian Civil War"),
        ("🇪🇹", "Modern Ethiopia"),
    ]

    top_k     = st.slider("Passages", 1, 5, 2, label_visibility="collapsed")
    threshold = st.slider("Threshold", 0.0, 1.5, 1.0, 0.05, label_visibility="collapsed")

    st.markdown("""
    <div style="color:#556070;font-size:11px;margin:-8px 0 12px;">
        ⚙️ passages &amp; similarity threshold
    </div>
    """, unsafe_allow_html=True)

    for icon, topic in topics:
        if st.button(f"{icon}  {topic}", key=f"t_{topic}", use_container_width=True):
            st.session_state.pending_query = f"Explain the history and significance of {topic}."

    st.divider()

    col_clear = st.container()
    with col_clear:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("🗑️  Clear conversation", use_container_width=True, key="clear"):
            st.session_state.messages      = []
            st.session_state.pending_query = ""
        st.markdown("</div>", unsafe_allow_html=True)

# ── Main header ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:32px 20px 24px;">
    <div style="font-size:52px;line-height:1;margin-bottom:12px;">🏛️</div>
    <div style="font-family:'Playfair Display',serif;font-size:36px;font-weight:700;
                color:#E8C97A;line-height:1.2;margin-bottom:10px;">
        Abyssinia AI
    </div>
    <div style="color:#7A8899;font-size:15px;max-width:520px;margin:0 auto;line-height:1.7;">
        Your intelligent guide to Ethiopian history — from the ancient Kingdom
        of Aksum to the modern era. Ask anything.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Suggested questions (only when no chat yet) ───────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="color:#7A8899;font-size:12px;text-align:center;
                letter-spacing:1.5px;margin-bottom:14px;">
        ✦ SUGGESTED QUESTIONS
    </div>
    """, unsafe_allow_html=True)

    suggestions = [
        ("⚔️",  "Who won the Battle of Adwa?"),
        ("🏰", "What made the Axum Empire powerful?"),
        ("🦁", "Who was Emperor Menelik II?"),
        ("⛪", "Tell me about the Zagwe Dynasty rock churches"),
        ("🕊️",  "What was Haile Selassie's legacy?"),
        ("🔴", "How did the Derg regime fall?"),
    ]

    c1, c2 = st.columns(2)
    for i, (icon, q) in enumerate(suggestions):
        col = c1 if i % 2 == 0 else c2
        with col:
            st.markdown(f"""
            <div style="background:#0F1826;border:1px solid rgba(201,168,76,0.18);
                        border-radius:11px;padding:0;margin-bottom:0;">
            """, unsafe_allow_html=True)
            if st.button(
                f"{icon}  {q}",
                key=f"sug_{i}",
                use_container_width=True,
            ):
                st.session_state.pending_query = q
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Chat history ───────────────────────────────────────────────────────────────
if st.session_state.messages:
    st.markdown("""
    <div style="color:#E8C97A;font-family:'Playfair Display',serif;
                font-size:18px;font-weight:600;margin-bottom:16px;">
        💬 Historical Research Assistant
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style="background:rgba(201,168,76,0.10);
                    border:1px solid rgba(201,168,76,0.22);
                    border-radius:16px 16px 4px 16px;
                    padding:16px 20px;margin:10px 0 10px 15%;
                    font-size:15px;line-height:1.7;">
            <span style="color:#E8C97A;font-size:12px;
                         font-weight:600;display:block;margin-bottom:6px;">
                👤 YOU
            </span>
            {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:#0F1826;
                    border:1px solid #1E2D42;
                    border-radius:16px 16px 16px 4px;
                    border-left:3px solid var(--gold,#C9A84C);
                    padding:20px 22px;margin:10px 15% 10px 0;
                    font-size:15px;line-height:1.8;">
            <span style="color:#E8C97A;font-size:12px;
                         font-weight:600;display:block;margin-bottom:10px;">
                🏛️ ABYSSINIA AI
            </span>
            {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

        if msg.get("sources"):
            with st.expander(f"📚 {len(msg['sources'])} source(s) used"):
                for src in msg["sources"]:
                    st.markdown(f"""
                    <div style="background:#080E1A;border:1px solid #1E2D42;
                                border-left:3px solid #C9A84C;border-radius:8px;
                                padding:12px 14px;margin:7px 0;font-size:13px;color:#A0AEBF;">
                        📄 <b style="color:#E8C97A;">{src['filename']}</b>
                        &nbsp;·&nbsp; chunk {src['chunk']}
                        &nbsp;·&nbsp; distance {src['score']:.3f}
                    </div>
                    """, unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

default_q = st.session_state.pop("pending_query", "") or ""

with st.form("ask_form", clear_on_submit=True):
    query = st.text_input(
        "q",
        value=default_q,
        placeholder="Ask anything about Ethiopian history...",
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button(
        "🏛️  Discover History",
        type="primary",
        use_container_width=True,
    )

# ── Answer ─────────────────────────────────────────────────────────────────────
if submitted:
    if not query.strip():
        st.markdown("""
        <div style="background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.25);
                    border-radius:10px;padding:14px 18px;color:#E8C97A;font-size:14px;margin-top:8px;">
            ✦ Please type a question above and click <b>Discover History</b>.
        </div>
        """, unsafe_allow_html=True)
    elif not groq_key:
        st.error("GROQ_API_KEY is not set. Add it in Streamlit Cloud → Settings → Secrets.")
    else:
        with st.spinner("🔍 Searching Ethiopia's historical archives..."):
            try:
                results = vector_db.similarity_search_with_score(query, k=top_k * 5)
                results = sorted(
                    results,
                    key=lambda x: (x[1] is None, x[1] if x[1] is not None else float("inf"))
                )
                unique_contexts = deduplicate_and_filter(results, top_k=top_k, threshold=threshold)

                if not unique_contexts:
                    st.markdown("""
                    <div style="background:#0F1826;border:1px solid #1E2D42;
                                border-radius:12px;padding:18px 22px;color:#7A8899;font-size:14px;">
                        🏛️ I don't have enough context in my knowledge base to answer that.
                        Try rephrasing or choose a topic from the sidebar.
                    </div>
                    """, unsafe_allow_html=True)
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

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:30px 5px 10px;color:#3A4858;">
    <span style="font-size:18px;color:#5A6878;">🏛️</span>
    <span style="font-size:12px;margin-left:8px;">
        Abyssinia AI · Powered by RAG · Groq · ChromaDB
    </span>
</div>
""", unsafe_allow_html=True)
