from pydantic import BaseModel

class QueryRequest(BaseModel):
    """
    Define la estructura esperada para el JSON de entrada.
    FastAPI usará esto para validar automáticamente la solicitud.
    """
    user_id: str
    query: str

class QueryResponse(BaseModel):
    """
    Define la estructura de la respuesta JSON.
    """
    answer: str