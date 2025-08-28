# src/agents.py

import os
from dotenv import load_dotenv
from pathlib import Path

# Componentes de LangChain que necesitamos
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .state import AgentState

# Cargar variables de entorno
load_dotenv()

# --- 1. Lógica para crear los componentes (Retriever y Generador) ---
# Esta parte es muy similar a nuestro antiguo archivo pipeline.py

# Definimos las constantes
BASE_DIR = Path(__file__).resolve().parent.parent
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
PERSIST_DIRECTORY = BASE_DIR / "db"
SOURCE_DOCUMENT = BASE_DIR / "data" / "productos.txt"

# Creamos el retriever una sola vez para reutilizarlo
loader = TextLoader(str(SOURCE_DOCUMENT), encoding="utf-8")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
db = Chroma.from_documents(docs, embeddings, persist_directory=str(PERSIST_DIRECTORY))
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": int(os.getenv("TOP_K", 3))}
)

# Creamos la cadena de generación de respuesta
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

# Esta es la "cadena" que usará nuestro Agente Respondedor
responder_chain = prompt | llm | StrOutputParser()


# --- 2. Definición de los Nodos (Agentes) ---

def retriever_node(state: AgentState):
    """
    Agente Recuperador: Toma la pregunta del estado y recupera los documentos relevantes.
    """
    print("--- Ejecutando Nodo Recuperador ---")
    query = state["query"]
    documents = retriever.invoke(query)
    # Actualizamos el estado con los documentos recuperados
    return {"documents": documents}

def responder_node(state: AgentState):
    """
    Agente Respondedor: Toma la pregunta y los documentos del estado para generar una respuesta.
    """
    print("--- Ejecutando Nodo Respondedor ---")
    query = state["query"]
    documents = state["documents"]
    
    # Formateamos el contexto para pasarlo a la cadena de respuesta
    context = "\n\n".join([doc.page_content for doc in documents])
    
    # Invocamos la cadena con el contexto y la pregunta
    answer = responder_chain.invoke({"context": context, "question": query})
    
    # Actualizamos el estado con la respuesta final
    return {"answer": answer}