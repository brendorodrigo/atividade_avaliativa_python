#Aluno: Carlos Johnatan Silva Souza Rodrigues
from flask import Flask, request, jsonify

app = Flask(__name__)

class Desenvolvedor:
    def __init__(self, id, nome, senioridade, pontos_por_dia, linguagem):
        self.id = id
        self.nome = nome
        self.senioridade = senioridade
        self.pontos_por_dia = pontos_por_dia
        self.linguagem = linguagem

class Projeto:
    def __init__(self, id, descricao, prazo_dias, pontos_funcao):
        self.id = id
        self.descricao = descricao
        self.prazo_dias = prazo_dias
        self.pontos_funcao = pontos_funcao
        self.desenvolvedores = []

    def adicionar_desenvolvedor(self, dev):
        self.desenvolvedores.append(dev)

    def calcular_capacidade_total(self):
        return sum(dev.pontos_por_dia for dev in self.desenvolvedores) * self.prazo_dias

    def verificar_viabilidade(self):
        capacidade = self.calcular_capacidade_total()
        if capacidade >= self.pontos_funcao:
            return "Projeto viável"
        else:
            return "Projeto inviável"

desenvolvedores = []
projetos = []

@app.route('/desenvolvedores', methods=['POST'])
def criar_desenvolvedor():
    data = request.json

    dev = Desenvolvedor(
        len(desenvolvedores) + 1,
        data['nome'],
        data['senioridade'],
        data['pontos_por_dia'],
        data['linguagem']
    )

    desenvolvedores.append(dev)

    return jsonify({"msg": "Desenvolvedor criado com sucesso"})


@app.route('/desenvolvedores', methods=['GET'])
def listar_desenvolvedores():
    return jsonify([dev.__dict__ for dev in desenvolvedores])


@app.route('/desenvolvedores/<int:id>', methods=['GET'])
def buscar_desenvolvedor(id):
    for dev in desenvolvedores:
        if dev.id == id:
            return jsonify(dev.__dict__)
    return jsonify({"erro": "Desenvolvedor não encontrado"}), 404

@app.route('/projetos', methods=['POST'])
def criar_projeto():
    data = request.json

    proj = Projeto(
        len(projetos) + 1,
        data['descricao'],
        data['prazo_dias'],
        data['pontos_funcao']
    )

    projetos.append(proj)

    return jsonify({"msg": "Projeto criado com sucesso"})


@app.route('/projetos', methods=['GET'])
def listar_projetos():
    return jsonify([
        {
            "id": p.id,
            "descricao": p.descricao,
            "prazo_dias": p.prazo_dias,
            "pontos_funcao": p.pontos_funcao
        }
        for p in projetos
    ])


@app.route('/projetos/<int:id>', methods=['GET'])
def buscar_projeto(id):
    for p in projetos:
        if p.id == id:
            return jsonify({
                "id": p.id,
                "descricao": p.descricao,
                "prazo_dias": p.prazo_dias,
                "pontos_funcao": p.pontos_funcao
            })
    return jsonify({"erro": "Projeto não encontrado"}), 404


@app.route('/projetos/<int:id>/desenvolvedores', methods=['POST'])
def adicionar_dev_ao_projeto(id):
    data = request.json
    dev_id = data['desenvolvedor_id']

    if id > len(projetos) or dev_id > len(desenvolvedores):
        return jsonify({"erro": "Projeto ou desenvolvedor não encontrado"}), 404

    projeto = projetos[id - 1]
    dev = desenvolvedores[dev_id - 1]

    projeto.adicionar_desenvolvedor(dev)

    return jsonify({"msg": "Desenvolvedor adicionado ao projeto"})


@app.route('/projetos/<int:id>/desenvolvedores', methods=['GET'])
def listar_devs_do_projeto(id):
    if id > len(projetos):
        return jsonify({"erro": "Projeto não encontrado"}), 404

    projeto = projetos[id - 1]

    return jsonify([dev.__dict__ for dev in projeto.desenvolvedores])


@app.route('/projetos/<int:id>/viabilidade', methods=['GET'])
def verificar_viabilidade(id):
    if id > len(projetos):
        return jsonify({"erro": "Projeto não encontrado"}), 404

    projeto = projetos[id - 1]

    return jsonify({
        "viabilidade": projeto.verificar_viabilidade(),
        "capacidade_total": projeto.calcular_capacidade_total(),
        "pontos_necessarios": projeto.pontos_funcao
    })

if __name__ == '__main__':
    app.run(debug=True)
