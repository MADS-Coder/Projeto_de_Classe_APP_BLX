from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select
from src.schemas import schemas
from src.infra.sqlalchemy.models import models



class RepositorioPedidos():


    def __init__(self, db: Session) :
        self.db = db
 

    def gravar_pedido(self, pedido: schemas.Pedido):
        db_pedidos = models.Pedidos(quantidade=pedido.quantidade, 
                                   entrega_ou_retirada=pedido.entrega_ou_retirada, 
                                   local_de_entrega=pedido.local_de_entrega, 
                                   observacoes=pedido.observacoes,
                                   usuario_id=pedido.usuario_id,
                                   produto_id=pedido.produto_id)
        self.db.add(db_pedidos)
        self.db.commit()
        self.db.refresh(db_pedidos)
        return db_pedidos


    def buscar_por_id(self, id: int):
        consulta_id = select(models.Pedidos).where(models.Pedidos.id == id)
        pedidos = self.db.execute(consulta_id).scalars().all()
        return pedidos


    def listar_meus_pedidos_por_usuario_id(self, user_id: int):     
        consulta_usuario = select(models.Pedidos).where(models.Pedidos.usuario_id == user_id)
        resultado = self.db.execute(consulta_usuario).scalars().all()
        return resultado
        

    def listar_minhas_vendas_por_usuario_id(self, user_id: int):
        consulta_usuario = select(models.Pedidos).join_from(models.Pedidos, models.Produtos).where(models.Produtos.usuario_id == user_id)
        resultado = self.db.execute(consulta_usuario).scalars().all()
        return resultado