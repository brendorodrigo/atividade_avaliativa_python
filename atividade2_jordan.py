import logging
import sys

from flask import Flask, jsonify, request


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)

app = Flask(__name__)

desenvolvedores = {}
projetos = {}
dev_id = 1
proj_id = 1


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
            "linguagem": self.linguagem,
        }


class Projeto:
    def __init__(self, id, descricao, prazo_em_dias, pontos_de_funcao):
        self.id = id
        self.descricao = descricao
        self.prazo_em_dias = prazo_em_dias
        self.pontos_de_funcao = pontos_de_funcao
        self.desenvolvedores = []

    def adicionar_desenvolvedor(self, dev):
        if dev.id not in [d.id for d in self.desenvolvedores]:
            self.desenvolvedores.append(dev)

    def calcular_capacidade_total(self):
        return sum(d.pontos_por_dia for d in self.desenvolvedores) * self.prazo_em_dias

    def verificar_viabilidade(self):
        return self.calcular_capacidade_total() >= self.pontos_de_funcao

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prazo_dias": self.prazo_em_dias,
            "pontos_funcao": self.pontos_de_funcao,
            "desenvolvedores": [d.id for d in self.desenvolvedores],
        }


@app.before_request
def _log():
    data = request.get_json(silent=True)
    if data is None:
        data = request.args.to_dict() or None
    logging.info("%s %s dados=%s", request.method, request.path, data)


def err(msg, code):
    return jsonify({"erro": msg}), code


@app.post("/desenvolvedores")
def criar_dev():
    global dev_id
    data = request.get_json(silent=True) or {}
    try:
        dev = Desenvolvedor(
            dev_id,
            data["nome"],
            data["senioridade"],
            float(data["pontos_por_dia"]),
            data["linguagem"],
        )
    except KeyError as e:
        return err(f"Campo obrigatório ausente: {e.args[0]}", 400)
    desenvolvedores[dev_id] = dev
    dev_id += 1
    return jsonify(dev.to_dict()), 201


@app.get("/desenvolvedores")
def listar_dev():
    return jsonify([d.to_dict() for d in desenvolvedores.values()])


@app.get("/desenvolvedores/<int:id>")
def buscar_dev(id):
    dev = desenvolvedores.get(id)
    return jsonify(dev.to_dict()) if dev else err("Não encontrado", 404)


@app.post("/projetos")
def criar_proj():
    global proj_id
    data = request.get_json(silent=True) or {}
    try:
        proj = Projeto(
            proj_id,
            data["descricao"],
            int(data["prazo_dias"]),
            float(data["pontos_funcao"]),
        )
    except KeyError as e:
        return err(f"Campo obrigatório ausente: {e.args[0]}", 400)
    projetos[proj_id] = proj
    proj_id += 1
    return jsonify(proj.to_dict()), 201


@app.get("/projetos")
def listar_projetos():
    return jsonify([p.to_dict() for p in projetos.values()])


@app.get("/projetos/<int:id>")
def buscar_projeto(id):
    proj = projetos.get(id)
    return jsonify(proj.to_dict()) if proj else err("Não encontrado", 404)


@app.post("/projetos/<int:id>/desenvolvedores")
def adicionar_dev_projeto(id):
    data = request.get_json(silent=True) or {}
    if "desenvolvedor_id" not in data:
        return err("Campo obrigatório ausente: desenvolvedor_id", 400)
    proj = projetos.get(id)
    dev = desenvolvedores.get(int(data["desenvolvedor_id"]))
    if not proj:
        return err("Projeto não encontrado", 404)
    if not dev:
        return err("Desenvolvedor não encontrado", 404)
    proj.adicionar_desenvolvedor(dev)
    return jsonify({"projeto_id": proj.id, "desenvolvedor_id": dev.id})


@app.get("/projetos/<int:id>/desenvolvedores")
def listar_devs_projeto(id):
    proj = projetos.get(id)
    return jsonify([d.to_dict() for d in proj.desenvolvedores]) if proj else err("Projeto não encontrado", 404)


@app.get("/projetos/<int:id>/viabilidade")
def viabilidade(id):
    proj = projetos.get(id)
    if not proj:
        return err("Projeto não encontrado", 404)
    cap = proj.calcular_capacidade_total()
    ok = proj.verificar_viabilidade()
    return jsonify({"capacidade_total": cap, "viavel": ok, "status": "projeto viável" if ok else "projeto inviável"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)