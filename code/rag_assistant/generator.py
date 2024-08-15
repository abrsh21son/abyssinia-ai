from code.prompt_builder import build_prompt
from code.logger import logger


def build_answer(llm, query: str, docs: list) -> object:
    """Build a grounded prompt and invoke the LLM."""
    if not docs:
        logger.warning('build_answer called with empty docs list.')
    prompt = build_prompt(query, docs)
    try:
        return llm.invoke(prompt)
    except Exception as e:
        logger.error(f'LLM invocation failed: {e}')
        raise