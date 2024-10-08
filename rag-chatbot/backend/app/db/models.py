import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID, VARCHAR
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)


class Document(Base):
    __tablename__ = 'documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)
    file_type = Column(Text, nullable=False)
    file_name = Column(Text, nullable=False)
    file_path = Column(Text, nullable=False)
    added_at = Column(TIMESTAMP(timezone=True),
                      server_default='CURRENT_TIMESTAMP')


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default='CURRENT_TIMESTAMP')


class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey(
        'chats.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default='CURRENT_TIMESTAMP')


class Response(Base):
    __tablename__ = 'responses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey(
        'messages.id'), nullable=False)
    content = Column(Text, nullable=False)
    sources = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default='CURRENT_TIMESTAMP')


class ChatVector(Base):
    __tablename__ = 'chat_vectors'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_message = Column(Boolean, nullable=False)
    chat_id = Column(UUID(as_uuid=True), ForeignKey(
        'chats.id'), nullable=False)
    content = Column(Text, nullable=False)
    vector = Column(Vector(768))


class DocVector(Base):
    __tablename__ = 'doc_vectors'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_id = Column(UUID(as_uuid=True), ForeignKey(
        'documents.id'), nullable=False)
    doc_index = Column(Integer, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)
    content = Column(Text, nullable=False)
    vector = Column(Vector(768))
