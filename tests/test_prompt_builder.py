import pytest
from src.prompt_builder import build_prompt


class DummyDoc:
    def __init__(self, content, filename='test.txt'):
        self.page_content = content
        self.metadata = {'filename': filename}


def test_contains_query():
    docs = [(DummyDoc('Ethiopia won.'), 0.5)]
    assert 'Who won?' in build_prompt('Who won?', docs)


def test_contains_source():
    docs = [(DummyDoc('Fact.', 'menelik_II.txt'), 0.4)]
    assert 'menelik_II.txt' in build_prompt('Test?', docs)


def test_idk_instruction():
    docs = [(DummyDoc('Unrelated.'), 0.9)]
    assert 'do not know' in build_prompt('Question?', docs)


def test_raises_on_empty_query():
    with pytest.raises(ValueError):
        build_prompt('', [(DummyDoc('Fact.'), 0.5)])


def test_raises_on_empty_docs():
    with pytest.raises(ValueError):
        build_prompt('Question?', [])
