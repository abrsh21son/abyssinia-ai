from src.rag_assistant.retriever import deduplicate_and_filter


class DummyDoc:
    def __init__(self, content):
        self.page_content = content


def test_basic_dedup():
    results = [
        (DummyDoc('A'), 0.9), (DummyDoc('A'), 0.95),
        (DummyDoc('B'), 0.8), (DummyDoc('C'), 0.6),
    ]
    filtered = deduplicate_and_filter(results, top_k=2, threshold=0.7)
    assert len(filtered) == 2
    assert filtered[0][0].page_content == 'A'


def test_all_above_threshold():
    results = [(DummyDoc('X'), 1.5), (DummyDoc('Y'), 1.2)]
    assert deduplicate_and_filter(results, top_k=5, threshold=1.0) == []


def test_empty():
    assert deduplicate_and_filter([], top_k=3, threshold=1.0) == []


def test_top_k_enforced():
    results = [(DummyDoc(str(i)), 0.5) for i in range(10)]
    assert len(deduplicate_and_filter(results, top_k=3, threshold=1.0)) == 3


def test_none_score_included():
    results = [(DummyDoc('A'), None), (DummyDoc('B'), 0.5)]
    filtered = deduplicate_and_filter(results, top_k=5, threshold=1.0)
    assert any(d.page_content == 'A' for d, _ in filtered)
