from starlette import responses
from starlette.requests import Request
from starlette.types import ASGIApp, Scope, Receive, Send


class SimpleASGIMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    # Middlewares, são fragmentos de códigos que é executado, antes ou após da execução da tarefa que o usuário está querendo. Portanto na ida ele pode pega o (Request) e na volta pode pegar o (Response).
    #@app.middleware('http')
    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        await self.app(scope, receive, send)
        assert scope['type'] == 'http'
        # Realiza qualquer código antes de prosseguir.
        print('Interceptou Chegada')
        
        # O (Next) dar prosseguimento a requisição.
        response = Request(scope, receive)

        print(response.method)
        # Realiza qualquer código após prosseguir.
        print('Interceptou a Volta')