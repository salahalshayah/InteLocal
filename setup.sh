#!/bin/bash

BASE_DIR=$(pwd)

docker run -d \
  -v "$BASE_DIR/rag-chatbot/models:/root/.ollama" \
  -p 5000:11434 \
  --name llm ollama/ollama

docker exec llm ollama pull llama3.2:1b
docker exec llm ollama pull nomic-embed-text

cd "$BASE_DIR/rag-chatbot/docker"
docker compose up --build