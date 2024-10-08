import os
import uuid
from uuid import UUID

from app.db.models import Chat, Document, DocVector, Message, Response, User
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session, sessionmaker

# Auth Related CRUD


async def get_user_by_email(email: str, db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user_by_id(user_id: UUID, db: AsyncSession):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def add_user(user: User, db: AsyncSession):
    db.add(user)
    await db.commit()


# Document Related CRUD

async def get_user_docs(user_id: UUID, db: AsyncSession):
    result = await db.execute(select(Document).filter(Document.user_id == user_id))
    return result.scalars().all()


async def add_doc(document: Document, db: AsyncSession):
    db.add(document)
    await db.commit()


# Placeholder document ID for deleted documents
DELETED_DOC_ID = uuid.UUID('00000000-0000-0000-0000-000000000000')

# 1. Get all DocVector entries for a document


async def get_doc_vectors(doc_id: uuid.UUID, db: AsyncSession):
    result = await db.execute(select(DocVector).where(DocVector.doc_id == doc_id))
    return result.scalars().all()

# 2. Reassign DocVector entries to the placeholder document ID


async def reassign_doc_vectors_to_placeholder(doc_vectors, db: AsyncSession):
    for doc_vector in doc_vectors:
        doc_vector.doc_id = DELETED_DOC_ID
    await db.commit()

# 3. Delete the document row and remove its file from the filesystem


async def delete_document(doc_id: uuid.UUID, db: AsyncSession):
    doc = await db.get(Document, doc_id)
    if doc:
        file_path = doc.file_path
        await db.delete(doc)
        await db.commit()
        return file_path
    return None

# 4. Clean up unused DocVector entries linked to the placeholder document


async def get_unused_doc_vectors(db: AsyncSession):
    return await db.execute(
        select(DocVector)
        .where(DocVector.doc_id == DELETED_DOC_ID)
        .where(~exists().where(Response.sources.contains(DocVector.id)))
    )


async def delete_doc_vectors(doc_vectors, db: AsyncSession):
    for vector in doc_vectors:
        await db.delete(vector)
    await db.commit()


async def cleanup_unused_doc_vectors(db: AsyncSession):
    unused_vectors_result = await get_unused_doc_vectors(db)
    unused_vectors = unused_vectors_result.scalars().all()
    # await delete_doc_vectors(unused_vectors, db)

# 5. Check if the document belongs to the user


async def check_document_ownership(doc_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession):
    result = await db.execute(
        select(Document).where(Document.id ==
                               doc_id, Document.user_id == user_id)
    )
    return result.scalars().first() is not None

# Main method to remove a document


async def remove_doc(doc_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession):
    # 1. Check if the document belongs to the user
    is_owner = await check_document_ownership(doc_id, user_id, db)
    if not is_owner:
        raise PermissionError(
            "User does not own this document or it doesn't exist.")

    # 2. Get all DocVector entries for the document
    doc_vectors = await get_doc_vectors(doc_id, db)

    # 3. Reassign DocVector entries to the placeholder document
    await reassign_doc_vectors_to_placeholder(doc_vectors, db)

    # 4. Delete the document row and remove its file from the filesystem
    file_path = await delete_document(doc_id, db)

    # 5. Clean up unused DocVector entries linked to the placeholder document
    # await cleanup_unused_doc_vectors(db)

    return file_path
# Chat Related CRUD


async def create_chat(user_id: UUID, db: AsyncSession):
    chat = Chat(user_id=user_id)
    db.add(chat)
    await db.commit()
    return chat


async def user_chat_exists(user_id: UUID, chat_id: UUID, db: AsyncSession) -> bool:
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id, Chat.user_id == user_id)
    )
    chat = result.scalar_one_or_none()
    return chat


async def add_message(message: Message, db: AsyncSession) -> Message:
    db.add(message)
    await db.flush()  # Flush to get the ID and other defaults from the database
    await db.commit()
    return message  # Return the added message instance


async def add_response(response: Response, db: AsyncSession) -> Response:
    db.add(response)
    await db.flush()  # Flush to get the ID and other defaults from the database
    await db.commit()
    return response  # Return the added response instance


async def get_chats(user_id: UUID, db: AsyncSession):
    result = await db.execute(select(Chat).filter(Chat.user_id == user_id))
    return result.scalars().all()


async def get_chat(chat_id: UUID, db: AsyncSession):
    messages_result = await db.execute(select(Message).filter(Message.chat_id == chat_id))
    messages = messages_result.scalars().all()

    # Fetching responses linked to these messages
    responses_result = await db.execute(select(Response).filter(Response.message_id.in_([m.id for m in messages])))
    responses = responses_result.scalars().all()

    return messages, responses
