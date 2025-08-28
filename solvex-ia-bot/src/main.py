# src/main.py
from fastapi import FastAPI, HTTPException
from langgraph.graph import StateGraph, END
import logging

# Importamos nuestras nuevas definiciones de estado y agentes
from .models import QueryRequest, QueryResponse
from .state import AgentState
from .agents import retriever_node, responder_node

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 1. Construcción del Grafo de Agentes ---

# Creamos una nueva instancia del grafo, especificando cuál es nuestro objeto de estado
workflow = StateGraph(AgentState)

# Añadimos los nodos al grafo. Cada nodo es un agente (una función)
workflow.add_node("retriever", retriever_node)
workflow.add_node("responder", responder_node)

# Definimos el flujo de trabajo (las conexiones entre nodos)
workflow.set_entry_point("retriever") # El primer nodo en ejecutarse es el recuperador
workflow.add_edge("retriever", "responder") # Después del recuperador, se ejecuta el respondedor
workflow.set_finish_point("responder") # El respondedor es el último nodo

# Compilamos el grafo en un objeto ejecutable
graph = workflow.compile()


# --- 2. Inicialización de la Aplicación FastAPI ---

app = FastAPI(
    title="Solvex IA Product Bot (Multi-Agent)",
    description="Un microservicio con una arquitectura multi-agente usando LangGraph.",
    version="1.0.1"
)

# --- 3. Definición del Endpoint de la API ---

@app.post("/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    """
    Recibe una consulta, la procesa con el grafo de agentes
    y devuelve la respuesta final.
    """
    logger.info(f"Recibida consulta del usuario '{request.user_id}': '{request.query}'")
    
    # El input para el grafo es un diccionario que coincide con la estructura del estado inicial
    initial_state = {"query": request.query}
    
    try:
        # Invocamos el grafo con el estado inicial
        final_state = graph.invoke(initial_state)
        final_answer = final_state["answer"]
        logger.info(f"Respuesta generada: '{final_answer}'")
        return QueryResponse(answer=final_answer)
    except Exception as e:
        logger.error(f"Error al procesar la consulta con el grafo: {e}")
        raise HTTPException(status_code=500, detail="Ocurrió un error al procesar la consulta.")

@app.get("/", summary="Endpoint de salud")
def read_root():
    return {"status": "ok", "message": "Bienvenido al Bot Multi-Agente de Solvex IA"}