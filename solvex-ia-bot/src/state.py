from typing import List, TypedDict
from langchain_core.documents import Document

class AgentState(TypedDict):
    """
    Define la estructura de nuestro estado. Es la "mochila" de datos
    que se pasa entre los nodos (agentes) del grafo.
    """
    # La pregunta original del usuario
    query: str

    # La lista de documentos recuperados del almacén de vectores
    documents: List[Document]

    # La respuesta final generada por el LLM
    answer: str