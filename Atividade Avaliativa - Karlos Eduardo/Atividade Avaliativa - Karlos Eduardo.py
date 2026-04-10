from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Classes de Negócio ---

class Desenvolvedor:
    id_counter = 1
    def __init__(self, nome, senioridade, pontos_por_dia, linguagem):
        self.id = Desenvolvedor.id_counter
        Desenvolvedor.id_counter += 1
        self.nome = nome
        self.senioridade = senioridade
        self.pontos_por_dia = pontos_por_dia
        self.linguagem = linguagem

    def to_dict(self):
        return self.__dict__

class Projeto:
    id_counter = 1
    def __init__(self, descricao, prazo_dias, pontos_funcao):
        self.id = Projeto.id_counter
        Projeto.id_counter += 1
        self.descricao = descricao
        self.prazo_dias = prazo_dias
        self.pontos_funcao = pontos_funcao
        self.desenvolvedores = []

    def adicionar_desenvolvedor(self, dev):
        self.desenvolvedores.append(dev)

    def calcular_capacidade_total(self):
        # Soma os pontos por dia de todos os devs e multiplica pelo prazo
        soma_pontos_dia = sum(dev.pontos_por_dia for dev in self.desenvolvedores)
        return soma_pontos_dia * self.prazo_dias

    def verificar_viabilidade(self):
        capacidade = self.calcular_capacidade_total()
        if capacidade >= self.pontos_funcao:
            return "Projeto viável"
        return f"Projeto inviável (Capacidade: {capacidade} / Necessário: {self.pontos_funcao})"

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prazo_dias": self.prazo_dias,
            "pontos_funcao": self.pontos_funcao,
            "viabilidade": self.verificar_viabilidade(),
            "quantidade_devs": len(self.desenvolvedores)
        }

# --- Banco de Dados em Memória ---
db_desenvolvedores = []
db_projetos = []

# --- Rotas para Desenvolvedores ---

@app.route("/desenvolvedores", methods=["POST"])
def post_dev():
    data = request.get_json()
    novo_dev = Desenvolvedor(data['nome'], data['senioridade'], data['pontos_por_dia'], data['linguagem'])
    db_desenvolvedores.append(novo_dev)
    return jsonify(novo_dev.to_dict()), 201

@app.route("/desenvolvedores", methods=["GET"])
def get_devs():
    return jsonify([d.to_dict() for d in db_desenvolvedores])

@app.route("/desenvolvedores/<int:id>", methods=["GET"])
def get_dev_id(id):
    dev = next((d for d in db_desenvolvedores if d.id == id), None)
    return jsonify(dev.to_dict()) if dev else (jsonify({"erro": "Dev não encontrado"}), 404)

# --- Rotas para Projetos ---

@app.route("/projetos", methods=["POST"])
def post_projeto():
    data = request.get_json()
    novo_proj = Projeto(data['descricao'], data['prazo_dias'], data['pontos_funcao'])
    db_projetos.append(novo_proj)
    return jsonify(novo_proj.to_dict()), 201

@app.route("/projetos", methods=["GET"])
def get_projetos():
    return jsonify([p.to_dict() for p in db_projetos])

@app.route("/projetos/<int:id>", methods=["GET"])
def get_projeto_id(id):
    proj = next((p for p in db_projetos if p.id == id), None)
    return jsonify(proj.to_dict()) if proj else (jsonify({"erro": "Projeto não encontrado"}), 404)

@app.route("/projetos/<int:id>/desenvolvedores", methods=["POST"])
def add_dev_to_projeto(id):
    data = request.get_json()
    proj = next((p for p in db_projetos if p.id == id), None)
    dev = next((d for d in db_desenvolvedores if d.id == data['desenvolvedor_id']), None)
    
    if proj and dev:
        proj.adicionar_desenvolvedor(dev)
        return jsonify({"msg": f"Dev {dev.nome} adicionado ao projeto {proj.descricao}"}), 200
    return jsonify({"erro": "Projeto ou Dev não encontrado"}), 404

@app.route("/projetos/<int:id>/desenvolvedores", methods=["GET"])
def list_devs_projeto(id):
    proj = next((p for p in db_projetos if p.id == id), None)
    if proj:
        return jsonify([d.to_dict() for d in proj.desenvolvedores])
    return jsonify({"erro": "Projeto não encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)