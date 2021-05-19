from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.schemas.schemas import Produto, ProdutoSimples
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositoriosprodutos import RepositorioProduto

router = APIRouter()

#Cadastrar Produtos.
@router.post('/produtos', status_code=status.HTTP_201_CREATED, response_model=ProdutoSimples)
def criar_produto(produto: Produto, db: Session = Depends(get_db)):
    produto_criado = RepositorioProduto(db).criar(produto)
    return produto_criado


#Listar Produtos.
@router.get('/produtos', response_model=List[Produto])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = RepositorioProduto(db).listar()
    return produtos


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
