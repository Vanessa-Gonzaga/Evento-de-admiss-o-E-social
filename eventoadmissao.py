from flask import Flask, request, Response
from dataclasses import dataclass
import json
from objetos.evento_admissao_request import EventoAdmissaoRequestVO
import requests
from ambiente import E_SOCIAL_URL
from objetos.evento_admissao_response import EventoAdmissaoResponseVO

app = Flask(__name__)

@app.route('/evento-admissao', methods=['POST'])
def evento_admissao():

    dados_admissao: dict = request.json
    req = EventoAdmissaoRequestVO(**dados_admissao)
    
    response = requests.get(E_SOCIAL_URL,
                            data=json.dumps(req.__dict__),
                            headers={"Content-Type": "application/json"})

    response_data: dict = response.text

    resposta = EventoAdmissaoResponseVO(response_data)

    return Response(response=json.dumps(resposta.__dict__,
                                        ensure_ascii=False,
                                        indent=4))
    
if __name__ == '__main__':
    app.run()
