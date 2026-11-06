from typing import List, Tuple, Any


def deduplicate_and_filter(
    results: List[Tuple[Any, float]],
    top_k: int,
    threshold: float
) -> List[Tuple[Any, float]]:
    """
    Filter results by distance threshold and remove duplicate page contents.

    Args:
        results: List of (Document, score) tuples sorted ascending by score.
        top_k: Maximum number of results to return.
        threshold: Maximum allowed score (lower = stricter match).
    """
    unique: List[Tuple[Any, float]] = []
    seen: set = set()
    for doc, score in results:
        if score is not None and score > threshold:
            continue
        content = getattr(doc, 'page_content', None)
        if content not in seen:
            seen.add(content)
            unique.append((doc, score))
        if len(unique) >= top_k:
            break
    return unique
