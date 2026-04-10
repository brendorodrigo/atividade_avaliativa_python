from flask import Flask, request, jsonify

app = Flask(__name__)

desenvolvedores = []
projetos = []

class Desenvolvedor:
    def __init__(self, id, nome, senioridade, pontos_por_dia, linguagem):
        self.id = id
        self.nome = nome
        self.senioridade = senioridade
        self.pontos_por_dia = pontos_por_dia
        self.linguagem = linguagem

    def to_dict(self):
        return self.__dict__


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
        return sum(dev.pontos_por_dia for dev in self.desenvolvedores)

    def verificar_viabilidade(self):
        capacidade_total = self.calcular_capacidade_total()
        capacidade_no_prazo = capacidade_total * self.prazo_dias

        if capacidade_no_prazo >= self.pontos_funcao:
            return "Projeto viável"
        else:
            return "Projeto inviável"

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prazo_dias": self.prazo_dias,
            "pontos_funcao": self.pontos_funcao
        }


@app.route("/desenvolvedores", methods=["POST"])
def criar_desenvolvedor():
    data = request.json
    novo = Desenvolvedor(
        id=len(desenvolvedores) + 1,
        nome=data["nome"],
        senioridade=data["senioridade"],
        pontos_por_dia=data["pontos_por_dia"],
        linguagem=data["linguagem"]
    )
    desenvolvedores.append(novo)
    return jsonify(novo.to_dict()), 201


@app.route("/desenvolvedores", methods=["GET"])
def listar_desenvolvedores():
    return jsonify([d.to_dict() for d in desenvolvedores])


@app.route("/desenvolvedores/<int:id>", methods=["GET"])
def buscar_desenvolvedor(id):
    for d in desenvolvedores:
        if d.id == id:
            return jsonify(d.to_dict())
    return {"erro": "Desenvolvedor não encontrado"}, 404


@app.route("/projetos", methods=["POST"])
def criar_projeto():
    data = request.json
    novo = Projeto(
        id=len(projetos) + 1,
        descricao=data["descricao"],
        prazo_dias=data["prazo_dias"],
        pontos_funcao=data["pontos_funcao"]
    )
    projetos.append(novo)
    return jsonify(novo.to_dict()), 201


@app.route("/projetos", methods=["GET"])
def listar_projetos():
    return jsonify([p.to_dict() for p in projetos])


@app.route("/projetos/<int:id>", methods=["GET"])
def buscar_projeto(id):
    for p in projetos:
        if p.id == id:
            return jsonify(p.to_dict())
    return {"erro": "Projeto não encontrado"}, 404


@app.route("/projetos/<int:id>/desenvolvedores", methods=["POST"])
def adicionar_dev_projeto(id):
    data = request.json

    projeto = next((p for p in projetos if p.id == id), None)
    dev = next((d for d in desenvolvedores if d.id == data["desenvolvedor_id"]), None)

    if not projeto or not dev:
        return {"erro": "Projeto ou desenvolvedor não encontrado"}, 404

    projeto.adicionar_desenvolvedor(dev)
    return {"mensagem": "Desenvolvedor adicionado ao projeto"}


@app.route("/projetos/<int:id>/desenvolvedores", methods=["GET"])
def listar_devs_projeto(id):
    projeto = next((p for p in projetos if p.id == id), None)

    if not projeto:
        return {"erro": "Projeto não encontrado"}, 404

    return jsonify([d.to_dict() for d in projeto.desenvolvedores])


@app.route("/projetos/<int:id>/viabilidade", methods=["GET"])
def viabilidade_projeto(id):
    projeto = next((p for p in projetos if p.id == id), None)

    if not projeto:
        return {"erro": "Projeto não encontrado"}, 404

    return {"viabilidade": projeto.verificar_viabilidade()}


if __name__ == "__main__":
    app.run(debug=True)