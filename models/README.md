# Models

The project uses sentence-transformers/all-MiniLM-L6-v2 for text embeddings.

## Details
- Embedding dimension: 384
- Max sequence length: 256 tokens
- Downloaded automatically on first run

## Changing the Model
Pass model_name to VectorDBManager:
  VectorDBManager(model_name='sentence-transformers/all-mpnet-base-v2')

After changing, delete chroma_db/ and re-run to rebuild embeddings.