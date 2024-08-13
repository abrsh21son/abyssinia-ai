from code.rag_assistant.generator import build_answer


class DummyLLM:
    def invoke(self, prompt):
        return type('R', (), {'content': f'Answered: {prompt[:20]}'})()


class DummyDoc:
    def __init__(self, content):
        self.page_content = content
        self.metadata = {'filename': 'test.txt'}


def test_build_answer():
    llm = DummyLLM()
    docs = [(DummyDoc('Historical fact.'), 0.5)]
    result = build_answer(llm, 'What happened?', docs)
    assert result.content.startswith('Answered:')