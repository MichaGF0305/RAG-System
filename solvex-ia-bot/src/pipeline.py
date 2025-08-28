# src/pipeline.py

import os
from dotenv import load_dotenv
from pathlib import Path

# Cargadores de LangChain
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Modelos de Embeddings y LLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# Almacén de Vectores
from langchain_community.vectorstores import Chroma

# Prompting y Cadenas (Chains)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# --- CONSTANTES Y CONFIGURACIÓN ---
BASE_DIR = Path(__file__).resolve().parent.parent
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
PERSIST_DIRECTORY = BASE_DIR / "db"
SOURCE_DOCUMENT = BASE_DIR / "data" / "productos.txt"

def get_rag_chain():
    """
    Configura y devuelve una cadena RAG (Retrieval-Augmented Generation) completa.
    """
    # ... (El código de carga, división, embeddings y retriever no cambia) ...
    # 1. Cargar documentos
    loader = TextLoader(str(SOURCE_DOCUMENT), encoding="utf-8")
    documents = loader.load()

    # 2. Dividir documentos en trozos (chunks)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    # 3. Crear el modelo de embeddings
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # 4. Crear el almacén de vectores (Vector Store) y guardarlo en disco
    db = Chroma.from_documents(
        docs, embeddings, persist_directory=str(PERSIST_DIRECTORY)
    )

    # 5. Crear el recuperador (Retriever) desde la base de datos
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": int(os.getenv("TOP_K", 3))}
    )

    # 6. Definir el prompt para el LLM
    template = """
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
    prompt = ChatPromptTemplate.from_template(template)

    # 7. Inicializar el modelo LLM
    # --- ¡AQUÍ ESTÁ EL CAMBIO! ---
    # Usamos el nombre oficial y estable del modelo: "gemini-1.0-pro"
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.1, convert_system_message_to_human=True)

    # 8. Construir la cadena RAG
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain