from src.retrieval_and_response import retrieve_relevant_chunks, __version__


def test_version():
    assert __version__ == '0.1.0'


def test_none_db_returns_empty():
    assert retrieve_relevant_chunks(None, 'any query') == []
