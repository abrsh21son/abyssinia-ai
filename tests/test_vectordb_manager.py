from unittest.mock import MagicMock, patch
from src.vectordb_and_ingestion import VectorDBManager


def test_count_returns_zero_when_no_db():
    vm = VectorDBManager.__new__(VectorDBManager)
    vm.vector_db = None
    vm.embeddings = MagicMock()
    vm.data_dir = 'data'
    vm.persist_dir = 'chroma_db'
    vm.collection_name = 'test'
    with patch.object(vm, 'load_db', side_effect=lambda: None):
        assert vm.count() == 0
