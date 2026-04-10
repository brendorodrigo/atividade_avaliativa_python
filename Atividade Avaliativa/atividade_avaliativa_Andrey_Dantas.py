from flask import Flask, request, jsonify

app = Flask(__name__)

desenvolvedores = []
projetos = []

id_dev = 1
id_proj = 1


class Desenvolvedor:
    def __init__(self, id, nome, senioridade, pontos_por_dia, linguagem):
        self.id = id
        self.nome = nome
        self.senioridade = senioridade
        self.pontos_por_dia = pontos_por_dia
        self.linguagem = linguagem

    def cadastrar_desenvolvedor(self):
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
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prazo_dias": self.prazo_dias,
            "pontos_funcao": self.pontos_funcao
        }

    def adicionar_desenvolvedor(self, dev):
        self.desenvolvedores.append(dev)

    def calcular_capacidade_total(self):
        total = 0
        for d in self.desenvolvedores:
            total += d.pontos_por_dia
        return total

    def verificar_viabilidade(self):
        capacidade = self.calcular_capacidade_total() * self.prazo_dias
        if capacidade >= self.pontos_funcao:
            return "projeto viavel"
        else:
            return "projeto inviavel"


@app.route("/desenvolvedores", methods=["POST"])
def criar_dev():
    global id_dev
    data = request.get_json()

    dev = Desenvolvedor(
        id_dev,
        data["nome"],
        data["senioridade"],
        data["pontos_por_dia"],
        data["linguagem"]
    )

    desenvolvedores.append(dev)
    id_dev += 1

    return jsonify(dev.cadastrar_desenvolvedor())


@app.route("/desenvolvedores", methods=["GET"])
def listar_dev():
    lista = []
    for d in desenvolvedores:
        lista.append(d.cadastrar_desenvolvedor())
    return jsonify(lista)


@app.route("/desenvolvedores/<int:id>", methods=["GET"])
def pegar_dev(id):
    for d in desenvolvedores:
        if d.id == id:
            return jsonify(d.cadastrar_desenvolvedor())
    return jsonify({"erro": "nao encontrado"})


@app.route("/projetos", methods=["POST"])
def criar_proj():
    global id_proj
    data = request.get_json()

    p = Projeto(
        id_proj,
        data["descricao"],
        data["prazo_dias"],
        data["pontos_funcao"]
    )

    projetos.append(p)
    id_proj += 1

    return jsonify(p.criar_projeto())


@app.route("/projetos", methods=["GET"])
def listar_proj():
    lista = []
    for p in projetos:
        lista.append(p.criar_projeto())
    return jsonify(lista)


@app.route("/projetos/<int:id>", methods=["GET"])
def pegar_proj(id):
    for p in projetos:
        if p.id == id:
            return jsonify(p.criar_projeto())
    return jsonify({"erro": "nao encontrado"})


@app.route("/projetos/<int:id>/desenvolvedores", methods=["POST"])
def add_dev_proj(id):
    data = request.get_json()

    for p in projetos:
        if p.id == id:
            for d in desenvolvedores:
                if d.id == data["desenvolvedor_id"]:
                    p.adicionar_desenvolvedor(d)
                    return jsonify({"msg": "adicionado"})
    return jsonify({"erro": "nao encontrado"})


@app.route("/projetos/<int:id>/desenvolvedores", methods=["GET"])
def listar_dev_proj(id):
    for p in projetos:
        if p.id == id:
            lista = []
            for d in p.desenvolvedores:
                lista.append(d.cadastrar_desenvolvedor())
            return jsonify(lista)
    return jsonify({"erro": "nao encontrado"})


@app.route("/projetos/<int:id>/viabilidade", methods=["GET"])
def ver_viabilidade(id):
    for p in projetos:
        if p.id == id:
            return jsonify({"viabilidade": p.verificar_viabilidade()})
    return jsonify({"erro": "nao encontrado"})


if __name__ == "__main__":
    app.run(debug=True)
