import pytest
from code.prompt_builder import build_prompt


class DummyDoc:
    def __init__(self, content, filename='test.txt'):
        self.page_content = content
        self.metadata = {'filename': filename}


def test_contains_query():
    docs = [(DummyDoc('Ethiopia won.'), 0.5)]
    prompt = build_prompt('Who won?', docs)
    assert 'Who won?' in prompt
    assert 'Answer:' in prompt


def test_contains_source():
    docs = [(DummyDoc('Some fact.', 'menelik_II.txt'), 0.4)]
    prompt = build_prompt('Test?', docs)
    assert 'menelik_II.txt' in prompt


def test_idk_instruction():
    docs = [(DummyDoc('Unrelated.'), 0.9)]
    prompt = build_prompt('Question?', docs)
    assert 'do not know' in prompt