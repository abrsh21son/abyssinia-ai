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
                        st.markdown(f'- **{src}** chunk {chunk} (distance: {score:.3f})')
            except Exception as e:
                st.error(f'Groq API error: {e}')