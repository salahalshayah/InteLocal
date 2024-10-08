
from typing import List
from uuid import UUID

from app.db.models import DocVector
from langchain_experimental.text_splitter import SemanticChunker
from rag.file_processing.embeddings import get_text_embedding
from tqdm.asyncio import tqdm  # Make sure to install tqdm with asyncio support


async def process_content(content: str, text_splitter: SemanticChunker, file_path: str, embeddings: OllamaEmbeddings, user_id: UUID, doc_id: UUID) -> List[DocVector]:
    content = content
    chunks = text_splitter.create_documents([content])

    # Use tqdm to create a progress bar for the asynchronous loop
    tasks = [
        get_text_embedding(model=embeddings, text=chunk.page_content)
        for chunk in chunks
    ]

    # Use tqdm to wrap the tasks for progress indication
    embeddings_results = await tqdm.gather(*tasks, total=len(tasks))

    return [
        DocVector(
            doc_id=doc_id,
            doc_index=doc_index,
            user_id=user_id,
            content=chunk.page_content,
            vector=vector
        )
        for doc_index, (chunk, vector) in enumerate(zip(chunks, embeddings_results))
    ]
