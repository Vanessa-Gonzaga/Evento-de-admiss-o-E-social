# Evento de admissão E-social
 
#importanto dos módulos e aplicando as instância do flask

from flask import Flask, request, jsonify
from datetime import datetime
from lxml import etree
from flask_restful import Api, Resource
from signxml import XMLSigner, methods

app = Flask(__name__)


#informando os dados do trabalhador
api = Api(app)

class Admissao(Resource):
    def get(self):
        # Adicione aqui a lógica para buscar os dados de admissão
        return {'dados': 'dados de admissão'}

    def post(self):
        admissao = request.json
        # Adicione aqui a lógica para processar os dados de admissão
        # por exemplo, inserir os dados no banco de dados
        return {'status': 'sucesso', 'mensagem': 'dados de admissão recebidos com sucesso'}

api.add_resource(Admissao, '/admissao')

if __name__ == '__main__':
    app.run(debug=True)


# Criando os endpoints 

@app.route('/enviar_lote_eventos', methods=['POST'])
def enviar_lote_eventos():
    # Recupere os dados do corpo da solicitação POST
    data = request.get_json()

    # Defina as variáveis necessárias
    cert_path = 'caminho/para/certificado.pfx'
    cert_pass = 'senha_do_certificado'
    url_webservice = 'https://webservices.producao.esocial.gov.br/esocial/services/EnvioLoteEventos'
    headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}

    # Crie o elemento raiz do XML
    eSocial = etree.Element('eSocial', xmlns='http://www.esocial.gov.br/schema/evt/evtAdmissao/v02_05_00')

    # Crie o elemento "evtAdmissao"
    evtAdmissao = etree.SubElement(eSocial, 'evtAdmissao')

    # Adicione os atributos do elemento "evtAdmissao"
    evtAdmissao.set('Id', 'ID1234567890123456789012345678901234567890')
    evtAdmissao.set('xmlns', 'http://www.esocial.gov.br/schema/evt/evtAdmissao/v02_05_00')

    # Crie o elemento "ideEvento"
    ideEvento = etree.SubElement(evtAdmissao, 'ideEvento')

    # Adicione os elementos filhos do "ideEvento"
    tpAmb = etree.SubElement(ideEvento, 'tpAmb')
    tpAmb.text = '2'

    procEmi = etree.SubElement(ideEvento, 'procEmi')
    procEmi.text = '1'

    # Adicione o trabalhador como um elemento filho do "evtAdmissao"
    trabalhador = etree.SubElement(evtAdmissao, 'trabalhador')
    trabalhador.text = data['trabalhador']

    # Defina a data do início do vínculo empregatício
    dataInicio = '2022-01-01'

    # Crie um objeto XMLSigner e assine o XML com o certificado digital
    signer = XMLSigner(method=methods.enveloped, c14n_algorithm='http://www.w3.org/2001/10/xml-exc-c14n#')
    doc_signed = signer.sign(eSocial, key_file=cert_path, password=cert_pass)

    # Envie a solicitação POST para o webservice
    response = requests.post(url_webservice, data=etree.tostring(doc_signed), headers=headers)

    # Retorne a resposta como um documento XML assinado
    return jsonify(response.text)
