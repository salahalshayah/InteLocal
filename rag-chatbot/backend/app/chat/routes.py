from uuid import UUID

from app.auth.utils import get_current_user
from app.chat.schemas import ChatMessage
from app.db.crud import (
    add_message,
    add_response,
    create_chat,
    get_chat,
    get_chats,
    user_chat_exists,
)
from app.db.database import get_db
from app.db.models import Chat, ChatVector, Message, Response
from app.db.vectors import add_chat_vector
from fastapi import APIRouter, Depends, HTTPException
from rag.chatbot.chat import ask
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/")
async def create_new_chat(request: ChatMessage, current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    chat = await create_chat(user_id=current_user.id, db=db)
    message = Message(chat_id=chat.id, content=request.content)
    message = await add_message(message=message, db=db)
    answer, source = await ask(query=request.content, user_id=current_user.id, chat_id=chat.id, db=db)
    response = Response(message_id=message.id,
                        content=answer)
    response = await add_response(response=response, db=db)
# Save message vector to database
    message_embedding = await get_embeddings(message.content)
    message_chat_vector = ChatVector(is_message=True, chat_id=chat.id,
                                     content=message.content, vector=message_embedding)
    await add_chat_vector(chat_vector=chat_vector, db=db)
# Save response vector to database
    response_embedding = await get_embeddings(answer)
    response_chat_vector = ChatVector(is_message=False, chat_id=chat.id,
                                      content=answer, vector=response_embedding)
    await add_chat_vector(chat_vector=chat_vector, db=db)
    return {"chat_id": chat.id, "response": response, "sources": source}


@router.post("/{chat_id}")
async def create_new_chat(chat_id: UUID, request: ChatMessage, current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    chat = await user_chat_exists(user_id=current_user.id, chat_id=chat_id, db=db)
    if chat is None:
        raise HTTPException(
            status_code=404, detail="Chat not found or access denied")
    message = Message(chat_id=chat.id, content=request.content)
    message = await add_message(message=message, db=db)
    answer, source = await ask(query=request.content, user_id=current_user.id, chat_id=chat.id, db=db)
    response = Response(message_id=message.id,
                        content=answer)
    response = await add_response(response=response, db=db)
# Save message vector to database
    message_embedding = await get_embeddings(message.content)
    message_chat_vector = ChatVector(is_message=True, chat_id=chat.id,
                                     content=message.content, vector=message_embedding)
    await add_chat_vector(chat_vector=chat_vector, db=db)
# Save response vector to database
    response_embedding = await get_embeddings(answer)
    response_chat_vector = ChatVector(is_message=False, chat_id=chat.id,
                                      content=answer, vector=response_embedding)
    await add_chat_vector(chat_vector=chat_vector, db=db)
    return {"chat_id": chat.id, "response": response, "sources": source}


@router.get("")
async def list_user_chats(current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    chats = await get_chats(current_user.id, db)
    return {"chats": chats}


@router.get("/{chat_id}")
async def get_chat_details(chat_id: UUID, current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    chat = await user_chat_exists(user_id=current_user.id, chat_id=chat_id, db=db)
    if chat is None:
        raise HTTPException(
            status_code=404, detail="Chat not found or access denied")
    messages, responses = await get_chat(chat_id=chat.id, db=db)
    return {"messages": messages, "responses": responses}
