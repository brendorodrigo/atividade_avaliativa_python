class Desenvolvedor:
    _contador_id = 0

    def __init__(self, nome, senioridade, pontos_por_dia, linguagem):
        Desenvolvedor._contador_id += 1
        self.id = Desenvolvedor._contador_id
        self.nome = nome
        self.senioridade = senioridade
        self.pontos_por_dia = pontos_por_dia
        self.linguagem = linguagem

    def cadastrar_desenvolvedor(self):
        return self.to_dict()

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "senioridade": self.senioridade,
            "pontos_por_dia": self.pontos_por_dia,
            "linguagem": self.linguagem,
        }


class Projeto:
    _contador_id = 0

    def __init__(self, descricao, prazo_dias, pontos_funcao):
        Projeto._contador_id += 1
        self.id = Projeto._contador_id
        self.descricao = descricao
        self.prazo_dias = prazo_dias
        self.pontos_funcao = pontos_funcao
        self.desenvolvedores = []

    @staticmethod
    def criar_projeto(descricao, prazo_dias, pontos_funcao):
        return Projeto(descricao, prazo_dias, pontos_funcao)

    def adicionar_desenvolvedor(self, desenvolvedor):
        self.desenvolvedores.append(desenvolvedor)

    def calcular_capacidade_total(self):
        capacidade = sum(d.pontos_por_dia for d in self.desenvolvedores) * self.prazo_dias
        return capacidade

    def verificar_viabilidade(self):
        capacidade = self.calcular_capacidade_total()
        if capacidade >= self.pontos_funcao:
            return {
                "viavel": True,
                "mensagem": "Projeto viável",
                "capacidade_total": capacidade,
                "pontos_funcao": self.pontos_funcao,
            }
        else:
            return {
                "viavel": False,
                "mensagem": "Projeto inviável",
                "capacidade_total": capacidade,
                "pontos_funcao": self.pontos_funcao,
            }

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prazo_dias": self.prazo_dias,
            "pontos_funcao": self.pontos_funcao,
            "desenvolvedores": [d.to_dict() for d in self.desenvolvedores],
        }
