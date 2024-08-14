# Contributing to Abyssinia AI

Thank you for your interest! Here are the contribution guidelines.

## Steps
1. Fork the repository and create a feature branch.
2. Make changes with clear commit messages.
3. Run pytest tests/ to ensure all tests pass.
4. Open a Pull Request.

## Code Style
- Follow PEP 8.
- Add type hints to new functions.
- Include docstrings for public APIs.

## Adding Corpus Documents
- Place .txt files in data/.
- Delete chroma_db/ to force re-embedding.