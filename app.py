from flask import Flask, request, jsonify
from models import Desenvolvedor, Projeto

app = Flask(__name__)

desenvolvedores = []
projetos = []


# --- Desenvolvedores ---

@app.route("/desenvolvedores", methods=["POST"])
def criar_desenvolvedor():
    dados = request.get_json()
    dev = Desenvolvedor(
        nome=dados["nome"],
        senioridade=dados["senioridade"],
        pontos_por_dia=dados["pontos_por_dia"],
        linguagem=dados["linguagem"],
    )
    dev.cadastrar_desenvolvedor()
    desenvolvedores.append(dev)
    return jsonify(dev.to_dict()), 201


@app.route("/desenvolvedores", methods=["GET"])
def listar_desenvolvedores():
    return jsonify([d.to_dict() for d in desenvolvedores])


@app.route("/desenvolvedores/<int:id>", methods=["GET"])
def buscar_desenvolvedor(id):
    for d in desenvolvedores:
        if d.id == id:
            return jsonify(d.to_dict())
    return jsonify({"erro": "Desenvolvedor não encontrado"}), 404


# --- Projetos ---

@app.route("/projetos", methods=["POST"])
def criar_projeto():
    dados = request.get_json()
    projeto = Projeto.criar_projeto(
        descricao=dados["descricao"],
        prazo_dias=dados["prazo_dias"],
        pontos_funcao=dados["pontos_funcao"],
    )
    projetos.append(projeto)
    return jsonify(projeto.to_dict()), 201


@app.route("/projetos", methods=["GET"])
def listar_projetos():
    return jsonify([p.to_dict() for p in projetos])


@app.route("/projetos/<int:id>", methods=["GET"])
def buscar_projeto(id):
    for p in projetos:
        if p.id == id:
            return jsonify(p.to_dict())
    return jsonify({"erro": "Projeto não encontrado"}), 404


@app.route("/projetos/<int:id>/desenvolvedores", methods=["POST"])
def adicionar_desenvolvedor_projeto(id):
    dados = request.get_json()
    projeto = None
    for p in projetos:
        if p.id == id:
            projeto = p
            break
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    dev = None
    for d in desenvolvedores:
        if d.id == dados["desenvolvedor_id"]:
            dev = d
            break
    if not dev:
        return jsonify({"erro": "Desenvolvedor não encontrado"}), 404

    projeto.adicionar_desenvolvedor(dev)
    return jsonify(projeto.to_dict()), 200


@app.route("/projetos/<int:id>/desenvolvedores", methods=["GET"])
def listar_desenvolvedores_projeto(id):
    for p in projetos:
        if p.id == id:
            return jsonify([d.to_dict() for d in p.desenvolvedores])
    return jsonify({"erro": "Projeto não encontrado"}), 404


@app.route("/projetos/<int:id>/viabilidade", methods=["GET"])
def verificar_viabilidade_projeto(id):
    for p in projetos:
        if p.id == id:
            return jsonify(p.verificar_viabilidade())
    return jsonify({"erro": "Projeto não encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
