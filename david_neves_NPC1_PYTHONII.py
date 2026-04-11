from flask import Flask, jsonify, request

app = Flask(__name__)

desenvolvedores = {}
projetos = {}
dev_counter = 1
proj_counter = 1


class Desenvolvedor:
    def __init__(self, id, nome, senioridade, pontos_por_dia, linguagem):
        self.id = id
        self.nome = nome
        self.senioridade = senioridade
        self.pontos_por_dia = pontos_por_dia
        self.linguagem = linguagem

    def cadastrar_desenvolvedor(self):
        desenvolvedores[self.id] = self
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "senioridade": self.senioridade,
            "pontos_por_dia": self.pontos_por_dia,
            "linguagem": self.linguagem
        }


class Projeto:
    def __init__(self, id, descricao, prazo_dias, pontos_funcao):
        self.id = id
        self.descricao = descricao
        self.prazo_dias = prazo_dias
        self.pontos_funcao = pontos_funcao
        self.desenvolvedores = []

    def criar_projeto(self):
        projetos[self.id] = self
        return self

    def adicionar_desenvolvedor(self, desenvolvedor):
        self.desenvolvedores.append(desenvolvedor)

    def calcular_capacidade_total(self):
        return sum(dev.pontos_por_dia * self.prazo_dias for dev in self.desenvolvedores)

    def verificar_viabilidade(self):
        if self.calcular_capacidade_total() >= self.pontos_funcao:
            return "projeto viável"
        return "projeto inviável"

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prazo_dias": self.prazo_dias,
            "pontos_funcao": self.pontos_funcao,
            "desenvolvedores": [dev.to_dict() for dev in self.desenvolvedores]
        }


@app.route('/desenvolvedores', methods=['POST'])
def criar_desenvolvedor():
    global dev_counter
    data = request.json
    dev = Desenvolvedor(dev_counter, data['nome'], data['senioridade'], data['pontos_por_dia'], data['linguagem'])
    dev.cadastrar_desenvolvedor()
    dev_counter += 1
    return jsonify(dev.to_dict()), 201

@app.route('/desenvolvedores', methods=['GET'])
def listar_desenvolvedores():
    return jsonify([dev.to_dict() for dev in desenvolvedores.values()])

@app.route('/desenvolvedores/<int:id>', methods=['GET'])
def buscar_desenvolvedor(id):
    dev = desenvolvedores.get(id)
    if not dev:
        return jsonify({"erro": "Desenvolvedor não encontrado"}), 404
    return jsonify(dev.to_dict())

@app.route('/projetos', methods=['POST'])
def criar_projeto():
    global proj_counter
    data = request.json
    proj = Projeto(proj_counter, data['descricao'], data['prazo_dias'], data['pontos_funcao'])
    proj.criar_projeto()
    proj_counter += 1
    return jsonify(proj.to_dict()), 201

@app.route('/projetos', methods=['GET'])
def listar_projetos():
    return jsonify([proj.to_dict() for proj in projetos.values()])

@app.route('/projetos/<int:id>', methods=['GET'])
def buscar_projeto(id):
    proj = projetos.get(id)
    if not proj:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    return jsonify(proj.to_dict())

@app.route('/projetos/<int:id>/desenvolvedores', methods=['POST'])
def adicionar_dev_projeto(id):
    proj = projetos.get(id)
    if not proj:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    dev = desenvolvedores.get(request.json['desenvolvedor_id'])
    if not dev:
        return jsonify({"erro": "Desenvolvedor não encontrado"}), 404
    proj.adicionar_desenvolvedor(dev)
    return jsonify(proj.to_dict()), 200

@app.route('/projetos/<int:id>/desenvolvedores', methods=['GET'])
def listar_devs_projeto(id):
    proj = projetos.get(id)
    if not proj:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    return jsonify([dev.to_dict() for dev in proj.desenvolvedores])

@app.route('/projetos/<int:id>/viabilidade', methods=['GET'])
def verificar_viabilidade(id):
    proj = projetos.get(id)
    if not proj:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    return jsonify({
        "projeto_id": proj.id,
        "descricao": proj.descricao,
        "pontos_funcao": proj.pontos_funcao,
        "capacidade_total": proj.calcular_capacidade_total(),
        "viabilidade": proj.verificar_viabilidade()
    })


if __name__ == '__main__':
    app.run(debug=True)
