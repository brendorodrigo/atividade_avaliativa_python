from flask import Flask, jsonify, request

app = Flask(__name__)

class Desenvolvedor:
    def __init__(self, id, nome, senioridade, pontos_por_dia, linguagem):
        self.id = id
        self.nome = nome
        self.senioridade = senioridade
        self.pontos_por_dia = pontos_por_dia
        self.linguagem = linguagem

    @classmethod
    def cadastrar_desenvolvedor(cls, id, nome, senioridade, pontos_por_dia, linguagem):
        return cls(id, nome, senioridade, pontos_por_dia, linguagem)

    def to_dict(self):
        return self.__dict__

class Projeto:
    def __init__(self, id, descricao, prazo_em_dias, pontos_de_funcao):
        self.id = id
        self.descricao = descricao
        self.prazo_em_dias = prazo_em_dias
        self.pontos_de_funcao = pontos_de_funcao
        self.desenvolvedores = []

    @classmethod
    def criar_projeto(cls, id, descricao, prazo_em_dias, pontos_de_funcao):
        return cls(id, descricao, prazo_em_dias, pontos_de_funcao)

    def adicionar_desenvolvedor(self, desenvolvedor):
        self.desenvolvedores.append(desenvolvedor)

    def calcular_capacidade_total(self):
        soma_pontos_dia = sum(dev.pontos_por_dia for dev in self.desenvolvedores)
        return soma_pontos_dia * self.prazo_em_dias

    def verificar_viabilidade(self):
        capacidade = self.calcular_capacidade_total()
        if capacidade >= self.pontos_de_funcao:
            return "Projeto Viável"
        else:
            return "Projeto Inviável"

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prazo_em_dias": self.prazo_em_dias,
            "pontos_de_funcao": self.pontos_de_funcao,
            "desenvolvedores": [d.to_dict() for d in self.desenvolvedores]
        }

banco_devs = []
banco_projetos = []

@app.route('/desenvolvedores', methods=['POST'])
def api_cadastrar_dev():
    data = request.get_json()
    novo_id = len(banco_devs) + 1
    novo_dev = Desenvolvedor.cadastrar_desenvolvedor(
        novo_id, data['nome'], data['senioridade'], data['pontos_por_dia'], data['linguagem']
    )
    banco_devs.append(novo_dev)
    return jsonify(novo_dev.to_dict()), 201

@app.route('/desenvolvedores', methods=['GET'])
def api_listar_devs():
    return jsonify([d.to_dict() for d in banco_devs])

@app.route('/projetos', methods=['POST'])
def api_criar_projeto():
    data = request.get_json()
    novo_id = len(banco_projetos) + 1
    novo_proj = Projeto.criar_projeto(
        novo_id, data['descricao'], data['prazo_dias'], data['pontos_funcao']
    )
    banco_projetos.append(novo_proj)
    return jsonify(novo_proj.to_dict()), 201

@app.route('/projetos/<int:id>/desenvolvedores', methods=['POST'])
def api_alocar_dev(id):
    data = request.get_json()
    proj = next((p for p in banco_projetos if p.id == id), None)
    dev = next((d for d in banco_devs if d.id == data['desenvolvedor_id']), None)
    
    if proj and dev:
        proj.adicionar_desenvolvedor(dev)
        return jsonify(proj.to_dict()), 200
    return jsonify({"erro": "Não encontrado"}), 404

@app.route('/projetos/<int:id>/viabilidade', methods=['GET'])
def api_verificar_viabilidade(id):
    proj = next((p for p in banco_projetos if p.id == id), None)
    if proj:
        return jsonify({
            "projeto": proj.descricao,
            "status": proj.verificar_viabilidade()
        })
    return jsonify({"erro": "Projeto não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
