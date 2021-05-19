from pydantic import BaseModel
from typing import Optional, List


class ProdutoSimples(BaseModel):
    id: Optional[int] = None
    nome: str
    preco: float
    disponivel: bool

    class Config:
        orm_mode = True


class Usuario(BaseModel):
    id: Optional[int] = None
    nome: str
    senha: str
    telefone: str
    produtos: List[ProdutoSimples] = []

    class Config:
        orm_mode = True


class UsuarioSimples(BaseModel):
    id: Optional[int] = None
    nome: str
    senha: str
    telefone: str

    class Config:
        orm_mode = True
        

class Produto(BaseModel):
    id: Optional[int] = None
    nome: str
    detalhes: str
    preco: float
    disponivel: bool = False
    usuario_id: Optional[int]
    usuario: Optional[UsuarioSimples]

    class Config:
        orm_mode = True


class Pedido(BaseModel):
    id: Optional[int] = None
    quantidade: int
    entrega_ou_retirada: Optional[str]
    local_de_entrega: str
    observacoes: Optional[str] = 'Sem observações'

    usuario_id: Optional[int]
    produto_id: Optional[int]

    usuario: Optional[UsuarioSimples]
    produto: Optional[ProdutoSimples]

    class Config:
        orm_mode = True
    
    
class PedidoSimples(BaseModel):
    id: Optional[int] = None
    quantidade: int
    local_de_entrega: str
    observacoes: Optional[str] = 'Sem observações'
    produto: Optional[ProdutoSimples]

    class Config:
        orm_mode = True