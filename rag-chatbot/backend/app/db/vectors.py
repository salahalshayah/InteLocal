import uuid
from uuid import UUID

from app.db.database import get_db
from app.db.models import ChatVector, DocVector
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

DELETED_DOC_ID = uuid.UUID('00000000-0000-0000-0000-000000000000')

# Vector-Related CRUD


async def add_doc_vector(doc_vector: DocVector, db: AsyncSession):
    db.add(doc_vector)
    await db.commit()


async def add_chat_vector(chat_vector: ChatVector, db: AsyncSession):
    db.add(chat_vector)
    await db.commit()


async def search_docs(user_id: UUID, query_embedding, db: AsyncSession):

    result = await db.execute(
        select(DocVector)
        .filter(DocVector.user_id == user_id, DocVector.doc_id != DELETED_DOC_ID)
        .order_by(DocVector.vector.l2_distance(query_embedding))
        .limit(3)
    )
    return result.scalars().all()


async def search_chat(chat_id: UUID, query_embedding, db: AsyncSession):
    result = await db.execute(
        select(ChatVector)
        .filter(ChatVector.chat_id == chat_id)
        .order_by(ChatVector.vector.l2_distance(query_embedding))
        .limit(5)
    )
    return result.scalars().all()
