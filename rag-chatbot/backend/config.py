import os

from dotenv import load_dotenv

# from langchain_ollama import OllamaEmbeddings
# from langchain_ollama.llms import OllamaLLM
from langchain_groq import ChatGroq

load_dotenv()


class Settings:
    PROJECT_NAME: str = "RAG Chatbot"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


settings = Settings()


llm = OllamaLLM(
    model="llama3.2:1b",
    temperature=0.4,
    base_url="http://localhost:5000"
)

embedding = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:5000"
)


class Models:
    LLM: OllamaLLM = llm
    EMBEDDING: OllamaEmbeddings = embedding


models = Models()
