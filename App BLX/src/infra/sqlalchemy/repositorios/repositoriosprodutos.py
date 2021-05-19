from sqlalchemy.orm import Session
from sqlalchemy import update, select, delete
from src.schemas import schemas
from src.infra.sqlalchemy.models import models


class RepositorioProduto():

    def __init__(self, db: Session):
        self.db = db

    def criar(self, produto: schemas.Produto):
        db_produto = models.Produtos(nome=produto.nome,
                                    detalhes=produto.detalhes,
                                    preco=produto.preco,
                                    disponivel=produto.disponivel,
                                    usuario_id=produto.usuario_id
                                    )
        self.db.add(db_produto)
        self.db.commit()
        self.db.refresh(db_produto)
        return db_produto

    def editar_produto(self, produto_id: int, produto: schemas.Produto):
        update_stmt = update(models.Produtos).where(models.Produtos.id == produto_id).values(nome=produto.nome,
                                                                    detalhes=produto.detalhes,
                                                                    preco=produto.preco,
                                                                    disponivel=produto.disponivel)
        self.db.execute(update_stmt)
        self.db.commit()


    def listar(self):
        produtos = self.db.query(models.Produtos).all()
        return produtos


    def buscarPorId(self, id: int):
        consulta = select(models.Produtos).where(models.Produtos.id == id)
        produto = self.db.execute(consulta).scalars().first()
        return produto


    def remover_produto(self, id_produto):
        exibir = self.db.query(models.Produtos)
        if exibir := exibir.filter(
            models.Produtos.id == id_produto
        ).first():
            self.db.delete(exibir)
            self.db.commit()
            return {'Mensagem': f'Produto {exibir.nome} removido com sucesso!.'}
        return {'Mensagem': f'Produto {id} não encontrado!.'}