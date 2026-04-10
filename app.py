from flask import Flask, request, jsonify

app = Flask(__name__)

# =========================
# CLASSES
# =========================

class Desenvolvedor:
    def __init__(self, id, nome, senioridade, pontos_por_dia, linguagem):
        self.id = id
        self.nome = nome
        self.senioridade = senioridade
        self.pontos_por_dia = pontos_por_dia
        self.linguagem = linguagem

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

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prazo_dias": self.prazo_dias,
            "pontos_funcao": self.pontos_funcao,
            "desenvolvedores": [dev.id for dev in self.desenvolvedores]
        }

    def adicionar_desenvolvedor(self, dev):
        self.desenvolvedores.append(dev)

    def calcular_capacidade_total(self):
        return sum(dev.pontos_por_dia for dev in self.desenvolvedores)

    def verificar_viabilidade(self):
        capacidade_total = self.calcular_capacidade_total() * self.prazo_dias

        if capacidade_total >= self.pontos_funcao:
            status = "projeto viável"
        else:
            status = "projeto inviável"

        return {
            "projeto_id": self.id,
            "descricao": self.descricao,
            "capacidade_total": capacidade_total,
            "pontos_funcao": self.pontos_funcao,
            "status": status
        }


# =========================
# "BANCO" EM MEMÓRIA
# =========================

desenvolvedores = []
projetos = []

contador_dev = 1
contador_proj = 1


# =========================
# ROTAS - DESENVOLVEDORES
# =========================

@app.route("/desenvolvedores", methods=["POST"])
def criar_desenvolvedor():
    global contador_dev

    dados = request.json

    dev = Desenvolvedor(
        id=contador_dev,
        nome=dados["nome"],
        senioridade=dados["senioridade"],
        pontos_por_dia=dados["pontos_por_dia"],
        linguagem=dados["linguagem"]
    )

    desenvolvedores.append(dev)
    contador_dev += 1

    return jsonify(dev.to_dict()), 201


@app.route("/desenvolvedores", methods=["GET"])
def listar_desenvolvedores():
    return jsonify([dev.to_dict() for dev in desenvolvedores])


@app.route("/desenvolvedores/<int:id>", methods=["GET"])
def buscar_desenvolvedor(id):
    for dev in desenvolvedores:
        if dev.id == id:
            return jsonify(dev.to_dict())

    return jsonify({"erro": "Desenvolvedor não encontrado"}), 404


# =========================
# ROTAS - PROJETOS
# =========================

@app.route("/projetos", methods=["POST"])
def criar_projeto():
    global contador_proj

    dados = request.json

    projeto = Projeto(
        id=contador_proj,
        descricao=dados["descricao"],
        prazo_dias=dados["prazo_dias"],
        pontos_funcao=dados["pontos_funcao"]
    )

    projetos.append(projeto)
    contador_proj += 1

    return jsonify(projeto.to_dict()), 201


@app.route("/projetos", methods=["GET"])
def listar_projetos():
    return jsonify([proj.to_dict() for proj in projetos])


@app.route("/projetos/<int:id>", methods=["GET"])
def buscar_projeto(id):
    for proj in projetos:
        if proj.id == id:
            return jsonify(proj.to_dict())

    return jsonify({"erro": "Projeto não encontrado"}), 404


@app.route("/projetos/<int:id>/desenvolvedores", methods=["POST"])
def adicionar_dev_projeto(id):
    dados = request.json

    projeto = next((p for p in projetos if p.id == id), None)
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    dev = next((d for d in desenvolvedores if d.id == dados["desenvolvedor_id"]), None)
    if not dev:
        return jsonify({"erro": "Desenvolvedor não encontrado"}), 404

    projeto.adicionar_desenvolvedor(dev)

    return jsonify({"mensagem": "Desenvolvedor adicionado"})


@app.route("/projetos/<int:id>/desenvolvedores", methods=["GET"])
def listar_devs_projeto(id):
    projeto = next((p for p in projetos if p.id == id), None)

    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    return jsonify([dev.to_dict() for dev in projeto.desenvolvedores])


@app.route("/projetos/<int:id>/viabilidade", methods=["GET"])
def viabilidade(id):
    projeto = next((p for p in projetos if p.id == id), None)

    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    return jsonify(projeto.verificar_viabilidade())


# =========================
# RODAR
# =========================

if __name__ == "__main__":
    app.run(debug=True)