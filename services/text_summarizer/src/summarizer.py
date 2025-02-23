from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

def summarize_text(text):
    model = OllamaLLM(model="llama3.2:1b")
    prompt = ChatPromptTemplate.from_template("You task is to summarizing the following text content: {content}.")
    chain = prompt | model
    return chain.invoke({"content": text})