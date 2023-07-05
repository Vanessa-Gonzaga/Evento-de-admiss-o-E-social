from dataclasses import dataclass
from objetos.endereco import EnderecoVO
from objetos.vinculo import VinculoVO

@dataclass
class EventoAdmissaoRequestVO:
    cpf:str
    nome:str
    sexo:str
    data_nascimento:str
    email: str
    telefone: str
    endereco: EnderecoVO
    vinculo: VinculoVO
