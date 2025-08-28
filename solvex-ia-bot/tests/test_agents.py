# tests/test_agents.py

from langchain_core.documents import Document
from src.state import AgentState
from src.agents import retriever_node, responder_node # Importamos ambos nodos
from unittest.mock import MagicMock # Importamos MagicMock para la segunda prueba

# --- Prueba 1: Nodo Recuperador ---
def test_retriever_node_returns_documents():
    """
    Prueba unitaria para el nodo recuperador.
    Verifica que, dada una pregunta, el nodo devuelve una lista de documentos.
    """
    initial_state: AgentState = {
        "query": "¿Cuál es la garantía de la laptop?",
        "documents": [],
        "answer": ""
    }
    result = retriever_node(initial_state)

    assert isinstance(result, dict)
    assert "documents" in result
    documents = result["documents"]
    assert isinstance(documents, list)
    assert len(documents) > 0
    assert all(isinstance(doc, Document) for doc in documents)
    
    print("\nPrueba para retriever_node pasada con éxito.")


# --- Prueba 2: Nodo Respondedor (con Mock) ---
def test_responder_node_generates_answer(mocker):
    """
    Prueba unitaria para el nodo respondedor, simulando la cadena de generación.
    """
    # 1. Arrange (Preparar)
    mock_documents = [
        Document(page_content="La garantía de la laptop es de 2 años."),
    ]
    
    current_state: AgentState = {
        "query": "¿Cuál es la garantía de la laptop?",
        "documents": mock_documents,
        "answer": ""
    }

    respuesta_simulada = "La respuesta simulada por el LLM es de 2 años."
    
    # Creamos un objeto de cadena simulado que simplemente devuelve nuestra respuesta
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = respuesta_simulada

    # Reemplazamos el objeto 'responder_chain' completo en el módulo 'src.agents'
    # con nuestro objeto simulado.
    mocker.patch('src.agents.responder_chain', new=mock_chain)

    # 2. Act (Actuar)
    result = responder_node(current_state)

    # 3. Assert (Verificar)
    assert "answer" in result
    assert result["answer"] == respuesta_simulada
    
    # Verificamos que la cadena simulada fue llamada con los argumentos correctos.
    # Esto prueba que la lógica DENTRO de responder_node funciona.
    mock_chain.invoke.assert_called_once_with({
        "context": "La garantía de la laptop es de 2 años.",
        "question": "¿Cuál es la garantía de la laptop?"
    })

    print("Prueba para responder_node pasada con éxito.")