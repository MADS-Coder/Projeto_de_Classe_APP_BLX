#Define a validade, fazendo operações com datas.
from datetime import datetime, timedelta 
#Serve para gerar e verificar o JWT token.
from jose import jwt                     


#CONFIG
SECRET_KEY = '698dc19d489c4e4db73e28a713eab07b'
ALGORITHM = 'HS256'
#Validade do token é 3000 minutos.
EXPIRES_IN_MIN = 3000             



#CRIA E RETORNA O TOKEN
'''Tem que enviar um dicionário que será uma carga de dados que ficará criptografada
dentro do token, essa carga vai criptografa para o usuárioe vai guardar la.'''
def criar_access_token(data: dict):
    #Faz uma copia do dicionario (data)
    dados = data.copy()
    #A expiração é vai ser através do (utcnow - que é pegar o agora), e faz uma operação utilizando
    #timedelta recebendo o minutos que está sendo passado a constante com valor de 3000 minutos.
    expiracao = datetime.utcnow() + timedelta(minutes=EXPIRES_IN_MIN)


    #Precisa ser feito um update dessa expiração, pois ela receberá o (sub) que é o telefone da (rotas_auth) e passará a ser um (exp) que é a experiração.
    dados.update({'exp': expiracao})

    #Chama o (encode) no jwt e vai encriptar os dados, passando a chave secreta usando o algoritimo e por fim retorna retorna o (token_jwt).
    token_jwt = jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt



#VALIDA E VERIFICA O ACCESS TOKEN, O OBJETIVO É RETORNAR O NÚMERO DE TELEFONE.
'''Em cada requisição feita pelo usuário ele manda para essa função, onde vai receber
o token criptografado e vai consegui extrair os dados dentro do banco de dados do usuario'''
def verificar_access_token(token: str):
    carga = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #Retorna um telefone do usuário que ele cadastrou como senha.
    return carga.get('sub')


#EM LINHAS GERAIS, O TELEFONE É CRIPTOGRAFADO.