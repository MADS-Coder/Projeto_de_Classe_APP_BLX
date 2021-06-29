from src.routers.auth_utils import obter_usuario_logado
from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositoriopedidos \
    import RepositorioPedidos
from src.schemas.schemas import Pedido, Usuario, PedidoSimples

router = APIRouter()


@router.post('/pedidos', status_code=status.HTTP_201_CREATED, response_model=PedidoSimples)
def fazer_pedido(pedido: Pedido, usuario: Usuario = Depends(obter_usuario_logado), session: Session = Depends(get_db)):
    pedido.usuario_id = usuario.id
    pedido_criado = RepositorioPedidos(session).gravar_pedido(pedido)
    return pedido_criado


@router.get('/pedidos', response_model=List[PedidoSimples])
def listar_pedidos(usuario: Usuario = Depends(obter_usuario_logado), session: Session = Depends(get_db)):
    print(usuario.id)
    pedidos = RepositorioPedidos(session).listar_meus_pedidos_por_usuario_id(usuario.id)
    return pedidos


@router.get('/pedidos/vendas', response_model=List[PedidoSimples])
def listar_vendas(usuario: Usuario = Depends(obter_usuario_logado), session: Session = Depends(get_db)):
    pedidos = RepositorioPedidos(session).listar_minhas_vendas_por_usuario_id(usuario.id)
    return pedidos