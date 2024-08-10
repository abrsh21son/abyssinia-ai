from code.rag_assistant.retriever import deduplicate_and_filter


class DummyDoc:
    def __init__(self, content):
        self.page_content = content


def test_basic():
    results = [
        (DummyDoc('A'), 0.9), (DummyDoc('A'), 0.95),
        (DummyDoc('B'), 0.8), (DummyDoc('C'), 0.6),
    ]
    filtered = deduplicate_and_filter(results, top_k=2, threshold=0.7)
    assert len(filtered) == 2


def test_threshold_excludes_all():
    results = [(DummyDoc('X'), 1.5), (DummyDoc('Y'), 1.2)]
    assert deduplicate_and_filter(results, top_k=5, threshold=1.0) == []


def test_empty_input():
    assert deduplicate_and_filter([], top_k=3, threshold=1.0) == []


def test_top_k_limit():
    results = [(DummyDoc(str(i)), 0.5) for i in range(10)]
    filtered = deduplicate_and_filter(results, top_k=3, threshold=1.0)
    assert len(filtered) == 3