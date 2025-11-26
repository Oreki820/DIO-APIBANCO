from pydantic import BaseModel, Field


class ClienteCreate(BaseModel):
    nome: str = Field(..., min_length=2)


class ContaCreate(BaseModel):
    cliente_id: int


class Operacao(BaseModel):
    conta_id: int
    valor: float = Field(..., gt=0)


class Transferencia(BaseModel):
    origem_id: int
    destino_id: int
    valor: float = Field(..., gt=0)
