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