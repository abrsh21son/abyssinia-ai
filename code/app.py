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