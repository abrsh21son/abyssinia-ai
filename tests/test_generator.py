import pytest
from src.rag_assistant.generator import build_answer


class DummyLLM:
    def invoke(self, prompt):
        return type('R', (), {'content': f'Answered: {prompt[:20]}'})()


class FailingLLM:
    def invoke(self, prompt):
        raise RuntimeError('LLM unavailable')


class DummyDoc:
    def __init__(self, content):
        self.page_content = content
        self.metadata = {'filename': 'test.txt'}


def test_build_answer_returns_content():
    docs = [(DummyDoc('Historical fact.'), 0.5)]
    result = build_answer(DummyLLM(), 'What happened?', docs)
    assert hasattr(result, 'content')


def test_build_answer_propagates_llm_error():
    docs = [(DummyDoc('Fact.'), 0.5)]
    with pytest.raises(RuntimeError):
        build_answer(FailingLLM(), 'What happened?', docs)
