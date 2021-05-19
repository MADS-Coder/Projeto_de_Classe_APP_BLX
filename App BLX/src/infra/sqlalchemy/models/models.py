from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.infra.sqlalchemy.config.database import Base


class Usuarios(Base):
    __tablename__= 'usuario'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    senha = Column(String)
    telefone = Column(String)

    produtos = relationship('Produtos', back_populates='usuario')    #Produtos que o usuario vende.
    pedidos = relationship('Pedidos', back_populates='usuario')      #Pedidos que o usuario compra.


class Produtos(Base):
    __tablename__ = 'produto'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    detalhes = Column(String)
    preco = Column(Float)
    disponivel = Column(Boolean)
    tamanhos = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuario.id', name='fk_usuario'))

    usuario = relationship('Usuarios', back_populates='produtos')


class Pedidos(Base) :

    __tablename__ = 'pedido'

    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer)
    entrega_ou_retirada = Column(String) 
    local_de_entrega = Column(String)
    observacoes = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuario.id', name='fk_pedido_usuario'))
    produto_id = Column(Integer, ForeignKey('produto.id', name='fk_pedido_produto'))

    usuario = relationship('Usuarios', back_populates='pedidos')
    produto = relationship('Produtos')