import os
from uuid import UUID

import pymupdf4llm
from config import models
from langchain_experimental.text_splitter import SemanticChunker
from rag.file_processing.chunk import process_content

embeddings = models.EMBEDDING


async def pdf_loader(file_path: str) -> str:
    """Converts PDF to markdown text."""
    md_text = pymupdf4llm.to_markdown(file_path)
    return md_text


async def file_to_string(file_path: str) -> str:
    """Loads text or markdown file content as string."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


async def load_file(file_path: str) -> str:
    """Determines the file type and uses the appropriate loader."""
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)

    # Decide which loader to use based on the file extension
    if file_extension.lower() == '.pdf':
        return await pdf_loader(file_path)
    elif file_extension.lower() in ['.txt', '.md']:
        return await file_to_string(file_path)
    else:
        raise ValueError(
            "Unsupported file format. Only .pdf, .txt, and .md are supported.")
text_splitter = SemanticChunker(embeddings,
                                breakpoint_threshold_type="standard_deviation",
                                breakpoint_threshold_amount=0.6,
                                )


async def process_file(file_path: str, user_id: UUID, doc_id: UUID):
    content = await load_file(file_path)
    doc_vectors = await process_content(content=content, text_splitter=text_splitter, file_path=file_path, embeddings=embeddings, user_id=user_id, doc_id=doc_id)
    return doc_vectors
