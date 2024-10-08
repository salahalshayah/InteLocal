async def get_text_embedding(embedding_model: OllamaEmbeddings, text: str):
    embedding = await embedding_model.aembed_query(text)
    return embedding
