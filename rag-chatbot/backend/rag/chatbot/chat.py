import asyncio
from uuid import UUID

from app.db.vectors import search_chat, search_docs
from config import models
from rag.chatbot.chains import (
    answer_synthesis_chain,
    chat_query_variation_chain,
    contextual_query_enhancement_chain,
    document_query_variation_chain,
)
from rag.file_processing.embeddings import get_text_embedding
from sqlalchemy.ext.asyncio import AsyncSession

embedding_model = models.EMBEDDING


async def remove_duplicate_vectors(vectors):

    seen_ids = set()
    unique_vectors = []
    for vector in vectors:
        if vector.id not in seen_ids:
            seen_ids.add(vector.id)
            unique_vectors.append(vector)
    return unique_vectors


async def add_chat_context_to_query(query: str, chat_id: UUID, db: AsyncSession):
    query_variations_json = await chat_query_variation_chain.ainvoke({'query': query})
    query_variations = [query]
    if query_variations_json['variation1']:
        query_variations.append(query_variations_json['variation1'])
    if query_variations_json['variation2']:
        query_variations.append(query_variations_json['variation2'])
    relevant_chat_messages = []
    for variation in query_variations:
        query_embedding = await get_text_embedding(embedding_model=embedding_model, text=variation)
        relevant_chat_vector = await search_chat(chat_id=chat_id, query_embedding=query_embedding, db=db)
        relevant_chat_messages.extend(relevant_chat_vector)
    chat_vectors = await remove_duplicate_vectors(relevant_chat_messages)

    chat_results = ""
    for vector in chat_vectors:
        if vector.is_message:
            chat_results += f"User: {vector.content}\n"
        else:
            chat_results += f"Bot Assistant: {vector.content}\n"

    enhanced_query = await contextual_query_enhancement_chain.ainvoke(
        {"original_query": query, "relevant_chat_messages": chat_results})

    return enhanced_query


async def get_relevant_chuncks(user_id: UUID, enhanced_query: str, db: AsyncSession):
    query_variations_json = await document_query_variation_chain.ainvoke({'query': enhanced_query})
    query_variations = [enhanced_query]
    if query_variations_json['variation1']:
        query_variations.append(query_variations_json['variation1'])
    if query_variations_json['variation2']:
        query_variations.append(query_variations_json['variation2'])

    relevant_documents = []
    for variation in query_variations:
        if type(variation) is str:
            query_embedding = await get_text_embedding(embedding_model=embedding_model, text=variation)
            relevant_doc_vectors = await search_docs(user_id=user_id, query_embedding=query_embedding, db=db)
            relevant_documents.extend(relevant_doc_vectors)
    doc_vectors = await remove_duplicate_vectors(relevant_documents)

    doc_results = ""
    sources = []
    i = 1
    for vector in doc_vectors:
        doc_results += f'{i}. "{vector.content}"\n'
        sources.append((vector.doc_id, vector.doc_index))
        i = i+1

    return doc_results, sources


async def ask(query: str, user_id: UUID, chat_id: UUID, db: AsyncSession) -> str:
    enhanced_query = await add_chat_context_to_query(query=query, chat_id=chat_id, db=db)
    relevant_context, sources = await get_relevant_chuncks(user_id=user_id, enhanced_query=enhanced_query, db=db)
    answer = await answer_synthesis_chain.ainvoke(
        {"enhanced_query": enhanced_query, "document_chunks": relevant_context})

    return answer, sources

if __name__ == "__main__":
    asyncio.run(main())
