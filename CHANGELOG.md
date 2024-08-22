# Changelog

All notable changes to Abyssinia AI are documented here.

## [Unreleased]
- Streaming response in Streamlit UI
- Multi-language support

## [0.1.0] - 2024-08-21

### Added
- Eight Ethiopian history corpus documents (Axum to Modern Ethiopia)
- VectorDBManager with ChromaDB, persistence, configurable embedding model, count()
- build_prompt with numbered sources, system persona, and ValueError validation
- deduplicate_and_filter with full type annotations
- Streamlit UI (sliders, sidebar, sources expander, primary button)
- CLI with --version flag and argparse
- wiki_fetcher.py for Wikipedia corpus expansion
- Dockerfile and .dockerignore
- GitHub Actions CI (Python 3.11 + 3.12 matrix)
- Pytest suite: retriever, prompt, generator, data_loader, pipeline, VectorDBManager
- MIT License, .env.example, CONTRIBUTING.md, CHANGELOG.md, pyproject.toml

### Fixed
- wiki_fetcher corrected to use code.logger import
- Empty query guard in Streamlit button handler
- Input validation (ValueError) in build_prompt