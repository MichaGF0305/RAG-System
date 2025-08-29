# src/agents.py

import os
from dotenv import load_dotenv
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- IMPORTACIÓN RELATIVA CORREGIDA ---
from .state import AgentState

# Cargar variables de entorno
load_dotenv()

# --- Lógica para crear los componentes (Retriever y Generador) ---
BASE_DIR = Path(__file__).resolve().parent.parent
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
PERSIST_DIRECTORY = BASE_DIR / "db"
SOURCE_DIRECTORY = BASE_DIR / "data"

print("Cargando documentos...")
loader = DirectoryLoader(
    path=str(SOURCE_DIRECTORY), 
    glob="**/*.txt", 
    show_progress=True, 
    use_multithreading=True,
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'}
)
documents = loader.load()
print(f"Documentos cargados: {len(documents)}")

print("Dividiendo documentos en trozos...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)
print(f"Número de trozos: {len(docs)}")

print("Creando embeddings y almacén de vectores...")
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
db = Chroma.from_documents(docs, embeddings, persist_directory=str(PERSIST_DIRECTORY))

print("Creando recuperador...")
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": int(os.getenv("TOP_K", 3))}
)

prompt_template = """
Eres un asistente experto en los productos de Solvex.
Tu tarea es responder las preguntas del usuario basándote únicamente en el contexto proporcionado.
Si la información no se encuentra en el contexto, responde amablemente que no tienes esa información.
No inventes respuestas.

Contexto:
{context}

Pregunta del usuario:
{question}

Respuesta del asistente:
"""
prompt = ChatPromptTemplate.from_template(prompt_template)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.1, convert_system_message_to_human=True)
responder_chain = prompt | llm | StrOutputParser()
print("Componentes de IA listos.")

# --- Definición de los Nodos (Agentes) ---
def retriever_node(state: AgentState):
    print("--- Ejecutando Nodo Recuperador ---")
    query = state["query"]
    documents = retriever.invoke(query)
    return {"documents": documents}

def responder_node(state: AgentState):
    print("--- Ejecutando Nodo Respondedor ---")
    query = state["query"]
    documents = state["documents"]
    context = "\n\n".join([doc.page_content for doc in documents])
    answer = responder_chain.invoke({"context": context, "question": query})
    return {"answer": answer}