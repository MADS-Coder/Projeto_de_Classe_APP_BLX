from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.schemas.schemas import Pedido, PedidoSimples
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositoriopedidos import RepositorioPedidos


router = APIRouter()


@router.post('/pedidos', status_code=status.HTTP_201_CREATED, response_model=Pedido)
def fazer_pedido(pedido: Pedido, session: Session = Depends(get_db)):
    pedido_criado = RepositorioPedidos(session).gravar_pedido(pedido)
    return pedido_criado


#Lista todos os Pedidos por ID.
@router.get('/pedidos/{id}', response_model=List[Pedido])
def exibir_pedido(id: int, session: Session = Depends(get_db)):
    pedido = RepositorioPedidos(session).buscar_por_id(id)
    if not pedido:
        raise HTTPException(status_code=404, detail=f"ID {id} não foi localizado!")
    return pedido


#Lista todos os Pedidos de Compra por USUARIO ID.
@router.get('/pedidos/{usuario_id}/pedidos', response_model=List[PedidoSimples])
def listar_pedidos(usuario_id: int, session: Session = Depends(get_db)):
    pedidos = RepositorioPedidos(session).listar_meus_pedidos_por_usuario_id(usuario_id)
    if not pedidos:
        raise HTTPException(status_code=404, detail=f"Usuário {usuario_id} não foi localizado!")
    return pedidos


#Lista todos os Pedidos de Venda por USUARIO ID.
@router.get('/usuarios/{usuario_id}/vendas', response_model=List[PedidoSimples])
def listar_pedidos(usuario_id: int, session: Session = Depends(get_db)):
    pedidos = RepositorioPedidos(session).listar_minhas_vendas_por_usuario_id(usuario_id)
    return pedidos