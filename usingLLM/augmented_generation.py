from text_processor.retriever import get_retriever
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os

#mistral api key
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")


#mistral model
llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key=api_key,
)

def ask_question(query:str) -> str:
    retriever = get_retriever()
    docs = retriever.invoke(query)
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are a helpful assistant.
Context:
{context}

Question:
{query}
"""
    response = llm.invoke(prompt)
    return response.content
