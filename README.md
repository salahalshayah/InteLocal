# InteLocal

## RAG Chatbot Development Project Plan

### How to run the project

```
git clone https://github.com/salahalshayah/InteLocal.git
```

```
cd InteLocal
```

rename the .env.example to .env


```
bash setup.sh
```
### Project Objectives

1. Develop a fully asynchronous FastAPI backend

2. Implement secure user authentication and document management

3. Integrate Langchain with Ollama for local LLM inference

4. Utilize PostgreSQL with pg_vector for efficient vector storage and retrieval

5. Create a responsive Streamlit frontend

6. Containerize the application using Docker for easy deployment

### Technical Architecture

#### Backend (FastAPI)

Postman: https://www.postman.com/salahalshayah/intelocal/overview

##### Authentication Module

- Endpoints:

- POST /auth/register

- POST /auth/login

- JWT-based authentication with user_id payload

##### Chat Module

- Endpoints:

- POST /chats

- POST /chats/{chat_id}

- GET /chats

- GET /chats/{chat_id}

- Asynchronous CRUD operations

##### Document Management Module

- Endpoints:

- GET /docs

- POST /docs

- DELETE /docs/{doc_id}

- UUID-based file storage system

#### Database (PostgreSQL with pg_vector)

- Schema:

- Users

- Documents

- Chats

- Messages

- Doc Embeddings

- Chat Embeddings

- Indexing: Utilize pg_vector for embedding storage and retrieval

#### Langchain Integration

##### Document Processing Pipeline

1. File ingestion (PDF, TXT, Markdown)

2. Text extraction and cleaning

3. Semantic chunking with metadata

4. Embedding generation using nomic-embed-text

5. Vector storage in PostgreSQL

##### LLM Integration

- Model: llama3.2:1b via Ollama

- Prompt engineering for optimal performance

##### RAG Implementation

- Query rewriting for context and retrieval enhancement

- Semantic chunking for improved accuracy

- Using RAG on the messages of the chat to provide context-aware responses

#### Frontend (Streamlit)

- Features:

- Real-time chat interface

- Document upload functionality

- Conversation history display

- JWT-based authentication management

#### Containerization

- Docker Compose for FastAPI and PostgreSQL

- Separate Ollama container for LLM inference

### Future Enhancements

- Implement rate limiting and request throttling

- Develop caching mechanisms for frequent queries
