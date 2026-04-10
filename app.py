from flask import Flask, request, jsonify, abort

app = Flask(__name__)

next_developer_id = 1
next_project_id = 1
developers = []
projects = []


class Desenvolvedor:
    def __init__(self, nome, senioridade, pontos_por_dia, linguagem):
        self.id = None
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
            "linguagem": self.linguagem,
        }


class Projeto:
    def __init__(self, descricao, prazo_dias, pontos_funcao):
        self.id = None
        self.descricao = descricao
        self.prazo_dias = prazo_dias
        self.pontos_funcao = pontos_funcao
        self.desenvolvedores = []

    def adicionar_desenvolvedor(self, desenvolvedor):
        if desenvolvedor.id in [dev.id for dev in self.desenvolvedores]:
            return False
        self.desenvolvedores.append(desenvolvedor)
        return True

    def calcular_capacidade_total(self):
        return sum(dev.pontos_por_dia for dev in self.desenvolvedores)

    def verificar_viabilidade(self):
        if self.prazo_dias == 0:
            return False
        capacidade_por_dia = self.calcular_capacidade_total()
        media_necessaria = self.pontos_funcao / self.prazo_dias
        return capacidade_por_dia >= media_necessaria

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prazo_dias": self.prazo_dias,
            "pontos_funcao": self.pontos_funcao,
            "desenvolvedores": [dev.id for dev in self.desenvolvedores],
        }


def find_developer(dev_id):
    return next((dev for dev in developers if dev.id == dev_id), None)


def find_project(project_id):
    return next((proj for proj in projects if proj.id == project_id), None)


@app.route("/desenvolvedores", methods=["POST"])
def create_developer():
    global next_developer_id
    data = request.get_json(force=True)
    required = ["nome", "senioridade", "pontos_por_dia", "linguagem"]
    if not all(field in data for field in required):
        return jsonify({"error": "Campos obrigatórios: nome, senioridade, pontos_por_dia, linguagem"}), 400

    try:
        pontos_por_dia = int(data["pontos_por_dia"])
    except (TypeError, ValueError):
        return jsonify({"error": "pontos_por_dia deve ser um número inteiro"}), 400

    desenvolvedor = Desenvolvedor(
        nome=data["nome"],
        senioridade=data["senioridade"],
        pontos_por_dia=pontos_por_dia,
        linguagem=data["linguagem"],
    )
    desenvolvedor.id = next_developer_id
    next_developer_id += 1
    developers.append(desenvolvedor)

    print(f"Novo desenvolvedor cadastrado: {desenvolvedor.to_dict()}")
    return jsonify(desenvolvedor.to_dict()), 201


@app.route("/desenvolvedores", methods=["GET"])
def list_developers():
    return jsonify([dev.to_dict() for dev in developers]), 200


@app.route("/desenvolvedores/<int:dev_id>", methods=["GET"])
def get_developer(dev_id):
    desenvolvedor = find_developer(dev_id)
    if desenvolvedor is None:
        abort(404, description="Desenvolvedor não encontrado")
    return jsonify(desenvolvedor.to_dict()), 200


@app.route("/projetos", methods=["POST"])
def create_project():
    global next_project_id
    data = request.get_json(force=True)
    required = ["descricao", "prazo_dias", "pontos_funcao"]
    if not all(field in data for field in required):
        return jsonify({"error": "Campos obrigatórios: descricao, prazo_dias, pontos_funcao"}), 400

    try:
        prazo_dias = int(data["prazo_dias"])
        pontos_funcao = int(data["pontos_funcao"])
    except (TypeError, ValueError):
        return jsonify({"error": "prazo_dias e pontos_funcao devem ser números inteiros"}), 400

    projeto = Projeto(
        descricao=data["descricao"],
        prazo_dias=prazo_dias,
        pontos_funcao=pontos_funcao,
    )
    projeto.id = next_project_id
    next_project_id += 1
    projects.append(projeto)

    print(f"Novo projeto criado: {projeto.to_dict()}")
    return jsonify(projeto.to_dict()), 201


@app.route("/projetos/<int:project_id>/desenvolvedores", methods=["POST"])
def add_developer_to_project(project_id):
    projeto = find_project(project_id)
    if projeto is None:
        abort(404, description="Projeto não encontrado")

    data = request.get_json(force=True)
    if "desenvolvedor_id" not in data:
        return jsonify({"error": "Campo obrigatório: desenvolvedor_id"}), 400

    desenvolvedor = find_developer(int(data["desenvolvedor_id"]))
    if desenvolvedor is None:
        abort(404, description="Desenvolvedor não encontrado")

    if not projeto.adicionar_desenvolvedor(desenvolvedor):
        return jsonify({"error": "Desenvolvedor já está vinculado a este projeto"}), 400

    print(
        f"Desenvolvedor {desenvolvedor.id} adicionado ao projeto {projeto.id}")
    return jsonify(projeto.to_dict()), 200


@app.route("/projetos", methods=["GET"])
def list_projects():
    return jsonify([proj.to_dict() for proj in projects]), 200


@app.route("/projetos/<int:project_id>", methods=["GET"])
def get_project(project_id):
    projeto = find_project(project_id)
    if projeto is None:
        abort(404, description="Projeto não encontrado")
    return jsonify(projeto.to_dict()), 200


@app.route("/projetos/<int:project_id>/desenvolvedores", methods=["GET"])
def get_project_developers(project_id):
    projeto = find_project(project_id)
    if projeto is None:
        abort(404, description="Projeto não encontrado")
    return jsonify([dev.to_dict() for dev in projeto.desenvolvedores]), 200


@app.route("/projetos/<int:project_id>/viabilidade", methods=["GET"])
def project_viability(project_id):
    projeto = find_project(project_id)
    if projeto is None:
        abort(404, description="Projeto não encontrado")

    viavel = projeto.verificar_viabilidade()
    mensagem = "Projeto viável" if viavel else "Projeto não viável"
    resultado = {
        "id": projeto.id,
        "descricao": projeto.descricao,
        "viavel": viavel,
        "mensagem": mensagem,
        "capacidade_total_por_dia": projeto.calcular_capacidade_total(),
        "pontos_funcao": projeto.pontos_funcao,
        "prazo_dias": projeto.prazo_dias,
    }

    print(f"Verificação de viabilidade para projeto {project_id}: {mensagem}")
    return jsonify(resultado), 200


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({"error": str(error)}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    print("Iniciando servidor Flask para atividade avaliativa em memória...")
    print("Ao reiniciar o servidor, todos os dados serão perdidos.")
    app.run(debug=True)
