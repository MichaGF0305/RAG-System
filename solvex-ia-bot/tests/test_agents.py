# tests/test_agents.py

from langchain_core.documents import Document
from unittest.mock import MagicMock

# --- IMPORTACIONES ABSOLUTAS CORREGIDAS ---
# Le decimos a pytest que busque desde la raíz del proyecto, dentro de la carpeta 'src'
from src.state import AgentState
from src.agents import retriever_node, responder_node

# --- Prueba 1: Nodo Recuperador ---
def test_retriever_node_returns_documents():
    initial_state: AgentState = { "query": "¿Cuál es la garantía?", "documents": [], "answer": "" }
    result = retriever_node(initial_state)
    assert "documents" in result
    assert len(result["documents"]) > 0
    assert isinstance(result["documents"][0], Document)
    print("\nPrueba para retriever_node pasada con éxito.")

# --- Prueba 2: Nodo Respondedor (con Mock) ---
def test_responder_node_generates_answer(mocker):
    mock_documents = [ Document(page_content="La garantía es de 2 años."), ]
    current_state: AgentState = { "query": "¿Cuál es la garantía?", "documents": mock_documents, "answer": "" }
    respuesta_simulada = "La respuesta simulada es de 2 años."
    
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = respuesta_simulada
    mocker.patch('src.agents.responder_chain', new=mock_chain)

    result = responder_node(current_state)

    assert "answer" in result
    assert result["answer"] == respuesta_simulada
    mock_chain.invoke.assert_called_once_with({
        "context": "La garantía es de 2 años.",
        "question": "¿Cuál es la garantía?"
    })
    print("Prueba para responder_node pasada con éxito.")