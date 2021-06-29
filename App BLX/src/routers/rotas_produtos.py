from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.schemas.schemas import Produto, ProdutoSimples, Usuario
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositoriosprodutos import RepositorioProduto
from src.routers.auth_utils import obter_usuario_logado

router = APIRouter()

#Cadastrar Produtos.
@router.post('/produtos', status_code=status.HTTP_201_CREATED, response_model=ProdutoSimples)
def criar_produto(produto: Produto, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    produto.usuario_id = usuario.id
    produto_criado = RepositorioProduto(db).criar(produto)
    return produto_criado


#Listar Produtos.
@router.get('/produtos', response_model=List[ProdutoSimples])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = RepositorioProduto(db).listar()
    return produtos

#Listar Produtos.
@router.get('/produtos', response_model=List[Produto])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = RepositorioProduto(db).listar()
    return produtos

#Listar Produtos por ID.
@router.get('/produtos/{id}', response_model=Produto)
def exibir_produto(id: int, session: Session = Depends(get_db)):
    produto_localizado = RepositorioProduto(session).buscarPorId(id)
    if not produto_localizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Não há um produto com o id = {id}')
    return produto_localizado


#Remove o produto pelo id.
@router.delete('/produtos/{produto_id}', status_code=status.HTTP_200_OK)
def remover_produto(produto_id: str, db: Session=Depends(get_db)):
    remover = RepositorioProduto(db).remover_produto(produto_id)
    if not remover:
        raise HTTPException(status_code=404, detail=f"Produto por ID {produto_id} não localizado!")
    return remover


#Editar produtos.
@router.put('/produtos/{id}', response_model=ProdutoSimples)
def atualizar_produto(id: int, produto: Produto, session: Session = Depends(get_db)):
    RepositorioProduto(session).editar_produto(id, produto)
    produto.id = id
    return produto
