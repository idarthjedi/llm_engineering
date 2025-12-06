from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
#from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_huggingface import HuggingFaceEmbeddings
import gradio as gr




MODEL = "gpt-oss:20b" #"gpt-4.1-nano"
DB_NAME = Path(__file__).resolve().parent / "vector_db"
load_dotenv(override=True)

embeddings = HuggingFaceEmbeddings(model_name="Qwen/Qwen3-Embedding-8B")
vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)

retriever = vectorstore.as_retriever()
#llm = ChatOpenAI(temperature=0, model_name=MODEL)
llm = ChatOllama(temperature=0, model=MODEL)

SYSTEM_PROMPT_TEMPLATE = """
You are a knowledgeable, friendly assistant representing the company Insurellm.
You are chatting with a user about Insurellm.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:
{context}
"""

def answer_question(question: str, history):
    docs = retriever.invoke(question)
    print(f"Relevant Documents Retrieved: {len(docs)}")
    #print(f"{[for x in x in docs]}")
    context = "\n\n".join(doc.page_content for doc in docs)
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)
    print(f"System Prompt:\n\n{system_prompt}")
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=question)])
    #print(response)
    return response.content

while True:
    prompt=input("Enter a question: ")
    print(answer_question(prompt, []))
    print("\n\n")

answer_question("What is the compensation history for Brandon Walker?", [])
#gr.ChatInterface(answer_question).launch(inbrowser=True)

