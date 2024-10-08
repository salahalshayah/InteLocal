
from config import models
from langchain_core.output_parsers import JsonOutputParser
from rag.chatbot.prompts import (
    answer_synthesis_prompt,
    chat_query_variation_prompt,
    contextual_query_enhancement_prompt,
    document_query_variation_prompt,
)

llm = models.LLM

chat_query_variation_chain = (
    chat_query_variation_prompt
    | llm
    | JsonOutputParser()
)

document_query_variation_chain = (
    document_query_variation_prompt
    | llm
    | JsonOutputParser()
)

contextual_query_enhancement_chain = (
    contextual_query_enhancement_prompt
    | llm
    | JsonOutputParser()
)

answer_synthesis_chain = (
    answer_synthesis_prompt
    | llm
    | JsonOutputParser()
)
