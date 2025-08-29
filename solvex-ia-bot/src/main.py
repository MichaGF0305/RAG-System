# src/main.py

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from langgraph.graph import StateGraph, END
import logging

# --- IMPORTACIONES RELATIVAS CORREGIDAS ---
# Le decimos a Python que busque estos módulos en el mismo paquete (directorio 'src')
from .models import QueryRequest, QueryResponse
from .state import AgentState
from .agents import retriever_node, responder_node

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Construcción del Grafo de Agentes ---
workflow = StateGraph(AgentState)
workflow.add_node("retriever", retriever_node)
workflow.add_node("responder", responder_node)
workflow.set_entry_point("retriever")
workflow.add_edge("retriever", "responder")
workflow.set_finish_point("responder")
graph = workflow.compile()
logger.info("Grafo de agentes compilado exitosamente.")

# --- Inicialización de la Aplicación FastAPI ---
app = FastAPI(
    title="Solvex IA Product Bot (Multi-Agent)",
    description="Un microservicio con una arquitectura multi-agente que incluye una interfaz de chat.",
    version="1.2.0" # Versión limpia
)

# --- Configuración para Servir la Interfaz de Chat ---
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=FileResponse)
async def read_index():
    return "static/index.html"

# --- Definición del Endpoint de la API ---
@app.post("/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    logger.info(f"Recibida consulta del usuario '{request.user_id}': '{request.query}'")
    initial_state = {"query": request.query}
    try:
        final_state = graph.invoke(initial_state)
        final_answer = final_state.get("answer", "No se pudo generar una respuesta.")
        logger.info(f"Respuesta generada: '{final_answer}'")
        return QueryResponse(answer=final_answer)
    except Exception as e:
        logger.error(f"Error al procesar la consulta con el grafo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ocurrió un error al procesar la consulta.")