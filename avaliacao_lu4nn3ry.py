from flask import Flask, jsonify, request


app = Flask(__name__)


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
            "linguagem": self.linguagem,
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
            "pontos_funcao": self.pontos_funcao,
        }

    def adicionar_desenvolvedor(self, desenvolvedor):
        self.desenvolvedores.append(desenvolvedor)

    def calcular_capacidade_total(self):
        return sum(dev.pontos_por_dia for dev in self.desenvolvedores) * self.prazo_dias

    def verificar_viabilidade(self):
        capacidade = self.calcular_capacidade_total()

        if capacidade >= self.pontos_funcao:
            return "projeto viavel"

        return "projeto inviavel"


db_desenvolvedores = []
db_projetos = []
id_dev_seq = 1
id_proj_seq = 1


@app.post("/desenvolvedores")
def cadastrar_desenvolvedor():
    global id_dev_seq
    dados = request.get_json()

    desenvolvedor = Desenvolvedor(
        id=id_dev_seq,
        nome=dados["nome"],
        senioridade=dados["senioridade"],
        pontos_por_dia=dados["pontos_por_dia"],
        linguagem=dados["linguagem"],
    )

    db_desenvolvedores.append(desenvolvedor)
    id_dev_seq += 1

    return jsonify(desenvolvedor.cadastrar_desenvolvedor()), 201


@app.get("/desenvolvedores")
def listar_desenvolvedores():
    return jsonify([dev.cadastrar_desenvolvedor() for dev in db_desenvolvedores])


@app.get("/desenvolvedores/<int:id>")
def obter_desenvolvedor(id):
    desenvolvedor = next((dev for dev in db_desenvolvedores if dev.id == id), None)

    if not desenvolvedor:
        return jsonify({"erro": "Desenvolvedor nao encontrado"}), 404

    return jsonify(desenvolvedor.cadastrar_desenvolvedor())


@app.post("/projetos")
def criar_projeto():
    global id_proj_seq
    dados = request.get_json()

    projeto = Projeto(
        id=id_proj_seq,
        descricao=dados["descricao"],
        prazo_dias=dados["prazo_dias"],
        pontos_funcao=dados["pontos_funcao"],
    )

    db_projetos.append(projeto)
    id_proj_seq += 1

    return jsonify(projeto.criar_projeto()), 201


@app.get("/projetos")
def listar_projetos():
    return jsonify([proj.criar_projeto() for proj in db_projetos])


@app.get("/projetos/<int:id>")
def obter_projeto(id):
    projeto = next((proj for proj in db_projetos if proj.id == id), None)

    if not projeto:
        return jsonify({"erro": "Projeto nao encontrado"}), 404

    return jsonify(projeto.criar_projeto())


@app.post("/projetos/<int:id>/desenvolvedores")
def adicionar_desenvolvedor_projeto(id):
    dados = request.get_json()
    projeto = next((proj for proj in db_projetos if proj.id == id), None)
    desenvolvedor = next(
        (dev for dev in db_desenvolvedores if dev.id == dados["desenvolvedor_id"]),
        None,
    )

    if not projeto:
        return jsonify({"erro": "Projeto nao encontrado"}), 404

    if not desenvolvedor:
        return jsonify({"erro": "Desenvolvedor nao encontrado"}), 404

    projeto.adicionar_desenvolvedor(desenvolvedor)

    return jsonify({"mensagem": "Desenvolvedor adicionado ao projeto"})


@app.get("/projetos/<int:id>/desenvolvedores")
def listar_desenvolvedores_projeto(id):
    projeto = next((proj for proj in db_projetos if proj.id == id), None)

    if not projeto:
        return jsonify({"erro": "Projeto nao encontrado"}), 404

    return jsonify([dev.cadastrar_desenvolvedor() for dev in projeto.desenvolvedores])


@app.get("/projetos/<int:id>/viabilidade")
def verificar_viabilidade(id):
    projeto = next((proj for proj in db_projetos if proj.id == id), None)

    if not projeto:
        return jsonify({"erro": "Projeto nao encontrado"}), 404

    return jsonify({"viabilidade": projeto.verificar_viabilidade()})


if __name__ == "__main__":
    app.run(debug=True)
