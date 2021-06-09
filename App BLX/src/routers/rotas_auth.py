from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_505_HTTP_VERSION_NOT_SUPPORTED
from src.schemas.schemas import Usuario, UsuarioSimples, LoginData, LoginSucesso
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositoriousuario import RepositorioUsuario
from src.infra.providers import hash_provider, token_provider
from src.routers.auth_utils import obter_usuario_logado


router = APIRouter()


#Cadastrar USUARIO
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSimples)
def criar_usuario(usuario: Usuario, session: Session = Depends(get_db)):
    #Verificar se já existe um para o telefone
    usuario_localizado = RepositorioUsuario(session).obter_por_telefone(usuario.telefone)

    if usuario_localizado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Já existe um usuário para este telefone')

    #Cria novo usuario
    usuario.senha = hash_provider.gerar_hash(usuario.senha)
    usuario_criado = RepositorioUsuario(session).criar_user(usuario)
    return usuario_criado


#Rota Signin
@router.post('/token', response_model=LoginSucesso)
def login(login_data: LoginData, session: Session = Depends(get_db)):
    senha = login_data.senha
    telefone = login_data.telefone

    usuario = RepositorioUsuario(session).obter_por_telefone(telefone)

    if not usuario:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Telefone ou senha estão incorretas!')
    
    senha_valida = hash_provider.verificar_hash(senha, usuario.senha)
    if not senha_valida:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Telefone ou senha estão incorretas!') 

    #Gerar o token JWT
    '''O sub é um padrão do JWT que é uma carga, que envia um telefone do usuario'''
    token = token_provider.criar_access_token({'sub': usuario.telefone})
    return {'usuario': usuario, 'access_token': token}       


#Pega o usuário logado.
@router.get('/me', response_model=UsuarioSimples)
def me(usuario: Usuario = Depends(obter_usuario_logado)):
    #decodificar o token, pegar o telefone, buscar usuario no bd e retornar
    return usuario