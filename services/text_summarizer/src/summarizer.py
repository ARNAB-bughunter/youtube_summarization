from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

def summarize_text(text):
    prompt = "Break down the script into a structured markdown format(do not menstion the output format in final response), the most important points while maintaining coherence and readability. Focus on the major plot beats, character motivations, and any twists. Avoid unnecessary details.Here is the script: {content}"
    model = OllamaLLM(model="llama3.2:1b")
    prompt = ChatPromptTemplate.from_template(prompt)
    chain = prompt | model
    return chain.invoke({"content": text})