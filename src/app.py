
import os
import sys

# Add repo root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
from src.vectordb_and_ingestion import VectorDBManager
from src.prompt_builder import build_prompt
from src.rag_assistant.retriever import deduplicate_and_filter
from src.logger import logger

# PAGE CONFIG
st.set_page_config(
    page_title="Abyssinia AI",
    page_icon="🏛️",
    layout="centered"
)

# LOAD ENVIRONMENT
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")


# ==========================================
# CUSTOM COLORS AND STYLING
# ==========================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F6F5F0;
    color: #26352E;
}

/* Main content alignment */
.block-container {
    max-width: 850px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Main title */
h1 {
    color: #174B38 !important;
    text-align: center;
    font-family: Georgia, serif;
    font-size: 42px !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
}

/* Subtitle */
.stApp p {
    color: #64736A;
}

/* Center caption */
[data-testid="stCaptionContainer"] {
    text-align: center;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #EAEDE5;
    border-right: 1px solid #D8DFD3;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #174B38 !important;
}

/* Section headings */
h2, h3 {
    color: #174B38 !important;
}

/* Input fields */
.stTextInput input {
    background-color: #FFFFFF !important;
    color: #26352E !important;
    border: 1px solid #CBD5C9 !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

.stTextInput input:focus {
    border-color: #B28A3B !important;
    box-shadow: 0 0 0 1px #B28A3B !important;
}

/* Buttons */
.stButton > button {
    background-color: #174B38 !important;
    color: #FFFFFF !important;
    border: 1px solid #174B38 !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    padding: 10px 22px !important;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #24664C !important;
    border-color: #24664C !important;
    color: #FFFFFF !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] {
    color: #174B38;
}

.stSlider [role="slider"] {
    background-color: #B28A3B !important;
    border-color: #B28A3B !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #DDE3D9;
    border-radius: 10px;
    padding: 14px;
}

[data-testid="stMetricValue"] {
    color: #174B38 !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background-color: #EAEDE5 !important;
    border-radius: 8px;
    color: #174B38 !important;
}

[data-testid="stExpander"] {
    border: 1px solid #D8DFD3;
    border-radius: 9px;
    background-color: #FFFFFF;
}

/* Dividers */
hr {
    border-color: #D9DFD5 !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 9px;
}

/* Sidebar text */
section[data-testid="stSidebar"] p {
    color: #52645A;
}

/* Form labels */
label {
    color: #344B3D !important;
    font-weight: 500 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #829087;
    font-size: 12px;
    padding: 25px 0 5px;
}

/* Mobile */
@media (max-width: 700px) {
    .block-container {
        padding: 1.2rem 1rem 2rem;
    }

    h1 {
        font-size: 32px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.title("🏛️ Abyssinia AI")

st.caption("An AI Assistant for Ethiopian History")

st.markdown(
    """
    <div style="
        width: 65px;
        height: 3px;
        background: #B28A3B;
        margin: 18px auto 28px auto;
        border-radius: 5px;">
    </div>
    """,
    unsafe_allow_html=True
)

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")


# ==========================================
# DATABASE
# ==========================================

@st.cache_resource(show_spinner="Loading knowledge base...")
def get_db_manager():
    dbm = VectorDBManager()
    dbm.load_db()
    if not dbm.vector_db:
        dbm.embed_and_insert()
    return dbm


db_manager = get_db_manager()
vector_db = db_manager.get_vector_db()


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("About")

    count = db_manager.count()

    st.metric(
        "Indexed chunks",
        count if count >= 0 else "unknown"
    )

    st.caption("Embedding: all-MiniLM-L6-v2")
    st.caption("LLM: Groq openai/gpt-oss-20b")

    st.divider()

    st.markdown("**Topics:**")

    st.markdown(
        "- Axum Empire\n"
        "- Zagwe Dynasty\n"
        "- Solomonic Dynasty\n"
        "- Menelik II\n"
        "- Haile Selassie\n"
        "- Derg Regime\n"
        "- Ethiopian Civil War\n"
        "- Modern Ethiopia"
    )


# ==========================================
# QUESTION INPUT
# ==========================================

st.markdown(
    """
    <div style="
        color: #174B38;
        font-size: 20px;
        font-weight: 650;
        margin-bottom: 8px;">
        Explore Ethiopian History
    </div>
    <div style="
        color: #829087;
        font-size: 14px;
        margin-bottom: 14px;">
        Ask a question and discover the history of Ethiopia.
    </div>
    """,
    unsafe_allow_html=True
)

query = st.text_input(
    "Your question:",
    placeholder="e.g. Who won the Battle of Adwa?"
)

# Retrieval settings
st.markdown(
    '<div style="color:#174B38;font-weight:600;margin-top:15px;">Retrieval Settings</div>',
    unsafe_allow_html=True
)

top_k = st.slider(
    "Top-K chunks",
    min_value=1,
    max_value=5,
    value=2
)

threshold = st.slider(
    "Distance threshold (lower = more similar)",
    min_value=0.0,
    max_value=1.5,
    value=1.0,
    step=0.05
)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)


# ==========================================
# GET ANSWER
# ==========================================

if st.button("Get Answer", type="primary", use_container_width=True):

    if not query.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Retrieving and generating answer..."):

            results = vector_db.similarity_search_with_score(
                query,
                k=top_k * 5
            )

            results = sorted(
                results,
                key=lambda x: (x[1] is None, x[1])
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

            elif groq_key:

                try:

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

                    st.markdown("---")

                    st.subheader("🏛️ Answer")

                    st.markdown(
                        f"""
                        <div style="
                            background: #FFFFFF;
                            border: 1px solid #DDE3D9;
                            border-left: 4px solid #B28A3B;
                            border-radius: 10px;
                            padding: 22px;
                            margin: 12px 0 20px 0;
                            line-height: 1.85;
                            color: #26352E;
                        ">
                        """,
                        unsafe_allow_html=True
                    )

                    st.write(answer_text)

                    st.markdown("</div>", unsafe_allow_html=True)

                    with st.expander("📚 Sources"):

                        for doc, score in unique_contexts:

                            src = doc.metadata.get(
                                "filename",
                                "unknown"
                            )

                            chunk = doc.metadata.get(
                                "chunk_id",
                                "?"
                            )

                            st.markdown(
                                f"- **{src}** · Chunk `{chunk}` "
                                f"(Distance: `{score:.3f}`)"
                            )

                except ValueError as e:

                    st.error(f"Input error: {e}")

                except Exception as e:

                    st.error(f"Groq API error: {e}")

            else:

                st.error(
                    "GROQ_API_KEY is not set. "
                    "Add it in Streamlit Cloud secrets."
                )


# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
    <div class="footer">
        <div style="
            color:#174B38;
            font-family:Georgia,serif;
            font-size:18px;
            font-weight:600;
            margin-bottom:6px;">
            🏛️ Abyssinia AI
        </div>
        Preserving Ethiopian History · Powered by AI
    </div>
    """,
    unsafe_allow_html=True
)
