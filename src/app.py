
import os
import sys

# Add repo root to sys.path
sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import streamlit as st
from dotenv import load_dotenv
from src.vectordb_and_ingestion import VectorDBManager
from src.prompt_builder import build_prompt
from src.rag_assistant.retriever import deduplicate_and_filter
from src.logger import logger


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Abyssinia AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")


# ==========================================
# CUSTOM CSS - PREMIUM ETHIOPIAN THEME
# ==========================================

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
    background:
        radial-gradient(ellipse at 80% 0%,
        rgba(213,172,88,0.10), transparent 40%),
        #0B1020;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

#MainMenu, footer {
    visibility: hidden;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #10182A;
    border-right: 1px solid rgba(213,172,88,0.18);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--gold-light);
}

/* HERO */

.hero {
    position: relative;
    padding: 48px 38px;
    border-radius: 22px;
    border: 1px solid rgba(213,172,88,0.25);
    background: linear-gradient(
        120deg,
        rgba(213,172,88,0.13),
        rgba(21,29,48,0.96)
    );
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
    font-size: clamp(32px, 5vw, 52px);
    color: var(--gold-light);
    line-height: 1.2;
    margin: 0;
}

.hero p {
    color: #B4BED0;
    font-size: 15px;
    line-height: 1.9;
    max-width: 650px;
    margin-top: 15px;
}

.hero-icon {
    position: absolute;
    right: 35px;
    top: 30px;
    font-size: 100px;
    opacity: 0.16;
}

/* METRICS */

[data-testid="stMetric"] {
    background: #151D30;
    border: 1px solid rgba(213,172,88,0.17);
    border-radius: 14px;
    padding: 17px;
}

[data-testid="stMetricValue"] {
    color: var(--gold-light);
}

[data-testid="stMetricLabel"] {
    color: #AEB9CA;
}

/* BUTTONS */

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

/* INPUTS */

.stTextInput input {
    background: #151D30;
    color: white;
    border: 1px solid #34415B;
    border-radius: 12px;
    padding: 14px;
}

.stTextInput input:focus {
    border-color: var(--gold);
    box-shadow: 0 0 0 1px var(--gold);
}

/* CHAT */

.user-message {
    background: rgba(213,172,88,0.12);
    border: 1px solid rgba(213,172,88,0.24);
    border-radius: 15px 15px 4px 15px;
    padding: 17px;
    margin: 15px 0 15px 12%;
    line-height: 1.8;
}

.ai-message {
    background: #151D30;
    border: 1px solid #2B3851;
    border-radius: 15px 15px 15px 4px;
    padding: 22px;
    margin: 15px 5% 15px 0;
    line-height: 1.9;
}

.message-label {
    color: var(--gold-light);
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 10px;
}

/* SOURCES */

.source-item {
    background: #10182A;
    border: 1px solid #293750;
    border-left: 3px solid var(--gold);
    border-radius: 9px;
    padding: 13px;
    margin: 9px 0;
    color: #C3CDDD;
}

/* SECTION TITLES */

.section-title {
    color: var(--gold-light);
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    font-weight: 600;
}

/* DIVIDERS */

hr {
    border-color: rgba(213,172,88,0.17);
}

/* MOBILE */

@media(max-width: 700px) {
    .hero {
        padding: 30px 22px;
    }

    .hero-icon {
        display: none;
    }

    .user-message {
        margin-left: 3%;
    }

    .ai-message {
        margin-right: 2%;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# DATABASE - ORIGINAL LOGIC
# ==========================================

@st.cache_resource(show_spinner="Loading historical knowledge...")
def get_db_manager():
    dbm = VectorDBManager()
    dbm.load_db()

    if not dbm.vector_db:
        dbm.embed_and_insert()

    return dbm


db_manager = get_db_manager()
vector_db = db_manager.get_vector_db()
count = db_manager.count()


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "query" not in st.session_state:
    st.session_state.query = ""


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center;padding:20px 5px;">
        <div style="font-size:48px;">🏛️</div>
        <h2 style="color:#F2D99A;margin:5px 0;">
            ABYSSINIA AI
        </h2>
        <p style="color:#8F9BB0;font-size:10px;letter-spacing:2px;">
            ETHIOPIAN HISTORY INTELLIGENCE
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 📊 Knowledge Base")

    st.metric(
        "Indexed Chunks",
        count if count >= 0 else "Unknown"
    )

    st.caption("🧠 all-MiniLM-L6-v2")
    st.caption("⚡ Groq · GPT-OSS-20B")

    st.divider()

    st.markdown("### ⚙️ Retrieval Settings")

    top_k = st.slider(
        "Number of passages",
        1, 5, 2
    )

    threshold = st.slider(
        "Distance threshold",
        0.0, 1.5, 1.0, 0.05
    )

    st.caption("Lower distance = more similar.")

    st.divider()

    st.markdown("### 📚 Explore Ethiopian History")

    topics = [
        "Axum Empire",
        "Zagwe Dynasty",
        "Solomonic Dynasty",
        "Menelik II",
        "Battle of Adwa",
        "Haile Selassie",
        "Derg Regime",
        "Ethiopian Civil War",
        "Modern Ethiopia"
    ]

    for topic in topics:
        if st.button(
            f"✦ {topic}",
            key=f"topic_{topic}",
            use_container_width=True
        ):
            st.session_state.query = (
                f"Explain the history and significance of {topic}."
            )
            st.rerun()

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
    <div style="text-align:center;color:#718096;
    font-size:11px;padding:25px 5px;">
        Preserving the past.<br>
        Exploring the future.
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# HERO
# ==========================================

st.markdown("""
<div class="hero">

    <div class="hero-icon">🏛️</div>

    <div class="hero-tag">
        ✦ YOUR ETHIOPIAN HISTORY COMPANION
    </div>

    <h1>Discover the Story of Ethiopia.</h1>

    <p>
        From the ancient Kingdom of Aksum to modern Ethiopia,
        explore the emperors, civilizations, battles and events
        that shaped one of Africa's oldest histories.
        Ask questions. Discover knowledge. Explore our heritage.
    </p>

</div>
""", unsafe_allow_html=True)


# ==========================================
# DASHBOARD
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📚 Indexed Chunks", count if count >= 0 else "Unknown")

with col2:
    st.metric("💬 Questions", len(st.session_state.messages) // 2)

with col3:
    st.metric("⚡ AI Engine", "Groq OSS 20B")


st.divider()


# ==========================================
# SUGGESTED QUESTIONS
# ==========================================

st.markdown(
    '<div class="section-title">✨ Start Exploring</div>',
    unsafe_allow_html=True
)

st.write("Choose a question to begin your historical journey.")

suggestions = [
    "Who won the Battle of Adwa?",
    "What made the Axum Empire powerful?",
    "Who was Emperor Menelik II?",
    "How did the Derg regime end?"
]

cols = st.columns(2)

for i, suggestion in enumerate(suggestions):
    with cols[i % 2]:
        if st.button(
            f"✦ {suggestion}",
            key=f"suggestion_{i}",
            use_container_width=True
        ):
            st.session_state.query = suggestion
            st.rerun()


st.divider()


# ==========================================
# CHAT HISTORY
# ==========================================

st.markdown(
    '<div class="section-title">💬 Historical Research Assistant</div>',
    unsafe_allow_html=True
)

for i, message in enumerate(st.session_state.messages):

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                <div class="message-label">👤 YOU</div>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        with st.container(border=True):

            st.markdown(
                '<div class="message-label">🏛️ ABYSSINIA AI</div>',
                unsafe_allow_html=True
            )

            st.markdown(message["content"])

            if message.get("sources"):

                with st.expander(
                    f"📚 View {len(message['sources'])} historical sources"
                ):

                    for source in message["sources"]:

                        st.markdown(
                            f"""
                            <div class="source-item">
                                <b>📄 {source['filename']}</b><br>
                                Chunk: {source['chunk']}<br>
                                Distance: {source['score']:.3f}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


# ==========================================
# QUESTION INPUT
# ==========================================

st.markdown("---")

with st.form("question_form"):

    query = st.text_input(
        "Your question",
        value=st.session_state.query,
        placeholder="Ask anything about Ethiopian history...",
        label_visibility="collapsed"
    )

    submitted = st.form_submit_button(
        "🏛️ Discover History",
        type="primary",
        use_container_width=True
    )


if submitted:

    if not query.strip():

        st.warning("Please enter a question.")

    elif not groq_key:

        st.error(
            "GROQ_API_KEY is not set. Add it in Streamlit Cloud secrets."
        )

    else:

        with st.spinner("🔍 Exploring Ethiopia's historical archives..."):

            try:

                results = vector_db.similarity_search_with_score(
                    query,
                    k=top_k * 5
                )

                results = sorted(
                    results,
                    key=lambda x: (
                        x[1] is None,
                        x[1] if x[1] is not None else float("inf")
                    )
                )

                unique_contexts = deduplicate_and_filter(
                    results,
                    top_k=top_k,
                    threshold=threshold
                )

                if not unique_contexts:

                    st.warning(
                        "Sorry, I cannot answer based on the available documents."
                    )

                else:

                    prompt = build_prompt(query, unique_contexts)

                    from langchain_groq import ChatGroq

                    llm = ChatGroq(
                        api_key=groq_key,
                        model="openai/gpt-oss-20b",
                        temperature=0
                    )

                    response = llm.invoke(prompt)

                    answer_text = getattr(
                        response,
                        "content",
                        str(response)
                    )

                    logger.info(f"Query: {query}")

                    sources = []

                    for doc, score in unique_contexts:

                        sources.append({
                            "filename": doc.metadata.get(
                                "filename", "unknown"
                            ),
                            "chunk": doc.metadata.get("chunk_id", "?"),
                            "score": score
                        })

                    st.session_state.messages.append({
                        "role": "user",
                        "content": query
                    })

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer_text,
                        "sources": sources
                    })

                    st.session_state.query = ""

                    st.rerun()

            except ValueError as e:

                st.error(f"Input error: {e}")

            except Exception as e:

                logger.exception("Answer generation failed")
                st.error(f"Groq API error: {e}")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown("""
<div style="text-align:center;padding:25px 5px;color:#8490A5;">

    <div style="font-size:25px;color:#D5AC58;">
        🏛️ ABYSSINIA AI
    </div>

    <p>Preserving the past. Exploring the future.</p>

    <p style="font-size:11px;">
        Powered by Retrieval-Augmented Generation
    </p>

</div>
""", unsafe_allow_html=True)
