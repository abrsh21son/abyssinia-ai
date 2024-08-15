from code.retrieval_and_response import retrieve_relevant_chunks


def test_retrieve_none_db_returns_empty():
    assert retrieve_relevant_chunks(None, 'any query') == []