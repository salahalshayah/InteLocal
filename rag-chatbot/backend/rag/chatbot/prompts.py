
from langchain_core.prompts import ChatPromptTemplate

chat_query_variation_template = """You are an assistant that helps create variations of a user's query to improve retrieval of relevant messages from a conversation history. Given a query, generate two alternative versions that could help find related messages in the chat history. The variations should maintain the original intent but use different wording or phrasing to capture a broader range of relevant messages.

Respond in the following JSON format:
{{
  "variation1": "<first_variation>",
  "variation2": "<second_variation>"
}}

Examples:
Query: "When is the project deadline?"
Response:
{{
  "variation1": "What's the due date for our current project?",
  "variation2": "Has anyone mentioned the project completion timeline?"
}}

Query: "Did Sarah share her presentation?"
Response:
{{
  "variation1": "Has Sarah uploaded or sent her slides?",
  "variation2": "Any updates from Sarah about her presentation materials?"
}}

NOTE: Ensure your answer is Valid JSON format, and only the JSON, do not include any additional text before or after the JSON

Now, create variations for the following query:
Query: "{query}"
"""

chat_query_variation_prompt = ChatPromptTemplate.from_template(
    chat_query_variation_template)


document_query_variation_template = """You are an assistant that helps create variations of a user's query to improve retrieval of relevant information from uploaded documents. The user's query has already been enhanced with relevant chat history. Your task is to generate two alternative versions of this query that could help find related information in the document chunks. The variations should maintain the original intent but use different wording or phrasing to capture a broader range of relevant document sections.

Respond in the following JSON format:
{{
  "variation1": "<first_variation>",
  "variation2": "<second_variation>"
}}

Examples:
Query: "What's our company's policy on remote work?"
Response:
{{
  "variation1": "Guidelines for working from home in our organization",
  "variation2": "Company rules regarding telecommuting and flexible work arrangements"
}}

Query: "How do we calculate employee bonuses?"
Response:
{{
  "variation1": "Bonus structure and computation methods for staff",
  "variation2": "Performance-based rewards and incentive calculations for employees"
}}
NOTE: Ensure your answer is Valid JSON format, and only the JSON, do not include any additional text before or after the JSON

Now, create variations for the following query:
Query: "{query}"
"""

document_query_variation_prompt = ChatPromptTemplate.from_template(
    document_query_variation_template)


contextual_query_enhancement_template = """You are an AI assistant tasked with enhancing a user's query by incorporating relevant context from a chat history. Your goal is to create a more comprehensive query that captures the full intent and context of the user's question, without requiring to go through the entire chat history.

Given:
1. The original user query
2. Relevant selected messages from the chat history (which may include both user and AI assitant messages)

Important Note: The relevant messages provided are not necessarily in chronological order. They are selected based on relevance to the current query, so you'll need to piece together the context logically, not sequentially.

Your task is to:
1. Analyze the provided chat messages, understanding that they may be out of order.
2. Identify key information relevant to the user's query, regardless of the message order.
3. Logically piece together the context from these messages.
4. Incorporate this relevant context into an enhanced version of the user's query.
5. Ensure the enhanced query is concise yet comprehensive, capturing the essential context without being overly verbose.
6. Present the enhanced query in a natural language format that can be easily understood and processed.

Please provide the enhanced query in the following JSON format:
{{
    "enhanced_query": <your enhanced query here>
}}
Example:
Original User Query: "What's the status of the project?"
Relevant Chat Messages:
- AI assistant: "The next team meeting is scheduled for Friday at 2 PM."
- User: "We started the new marketing campaign last week."
- User: "It's been positive. We're seeing a 15% increase in engagement."
- AI: "That's great! How's the initial response been?"
- User: "By the way, when is our next team meeting?"
{{
    "enhanced_query": "What's the current status of our new marketing campaign that started last week, particularly regarding the 15% increase in engagement, and how does this relate to our project's overall progress? Also, how might this be discussed in our upcoming team meeting on Friday?"
}}
NOTE: Ensure your answer is Valid JSON format, and only the JSON, do not include any additional text before or after the JSON

Now, please enhance the following query using the provided chat history:

Original User Query: {original_query}

Relevant Chat Messages:
{relevant_chat_messages}
"""

contextual_query_enhancement_prompt = ChatPromptTemplate.from_template(
    contextual_query_enhancement_template)


answer_synthesis_template = """You are an AI assistant answering queries based on provided document chunks. Your task:

1. Analyze the enhanced query (includes previous conversation context).
2. Review document chunks and extract relevant information.
3. Synthesize a comprehensive answer that addresses all query aspects.
4. Integrate information from multiple chunks when necessary.
5. State if any aspects can't be answered from the given chunks.
6. Highlight and balance any contradictions between chunks.

Provide your answer in this JSON format:
{{
    "answer": <your comprehensive answer here>
}}

Example:
Enhanced Query: What are our remote work policies, how do they compare to industry standards, and how has this affected productivity?

Document Chunks:
1. "XYZ Corp allows full-time remote work, with quarterly in-office requirements."
2. "68% of tech companies offer hybrid models, 25% offer full-time remote."
3. "22% increase in job satisfaction since implementing remote work."
4. "15% increase in project completion rates with remote work options."
{{
    "answer": "XYZ Corp offers full-time remote work with quarterly in-office requirements, more flexible than the industry norm where only 25% offer full-time remote options. This policy has positively impacted the team, with a 22% increase in job satisfaction and a 15% boost in project completion rates. However, we lack data on other productivity aspects or potential challenges of remote work."
}}

NOTE: Ensure your answer is Valid JSON format, and only the JSON, do not include any additional text before or after the JSON
Now, please answer the following:

Enhanced Query: {enhanced_query}

Document Chunks:
{document_chunks}
"""

answer_synthesis_prompt = ChatPromptTemplate.from_template(
    answer_synthesis_template)
