from flask import Flask, request, jsonify
from typing import List, Dict

app = Flask(__name__)


class Desenvolvedor:
    def __init__(self, id_dev: int, nome: str, senioridade: str, pontos_por_dia: int, linguagem: str):
        self.id = id_dev
        self.nome = nome
        self.senioridade = senioridade
        self.pontos_por_dia = pontos_por_dia
        self.linguagem = linguagem

    @classmethod
    def cadastrar_desenvolvedor(cls, id_dev: int, nome: str, senioridade: str, pontos_por_dia: int, linguagem: str):
        return cls(id_dev, nome, senioridade, pontos_por_dia, linguagem)
        
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "senioridade": self.senioridade,
            "pontos_por_dia": self.pontos_por_dia,
            "linguagem": self.linguagem
        }


class Projeto:
    def __init__(self, id_proj: int, descricao: str, prazo_dias: int, pontos_funcao: int):
        self.id = id_proj
        self.descricao = descricao
        self.prazo_dias = prazo_dias
        self.pontos_funcao = pontos_funcao
        self.desenvolvedores: List[Desenvolvedor] = []

    @classmethod
    def criar_projeto(cls, id_proj: int, descricao: str, prazo_dias: int, pontos_funcao: int):
        return cls(id_proj, descricao, prazo_dias, pontos_funcao)

    def adicionar_desenvolvedor(self, dev: Desenvolvedor):
        self.desenvolvedores.append(dev)

    def calcular_capacidade_total(self) -> int:
        capacidade_diaria = sum(dev.pontos_por_dia for dev in self.desenvolvedores)
        return capacidade_diaria * self.prazo_dias

    def verificar_viabilidade(self) -> str:
        if self.calcular_capacidade_total() >= self.pontos_funcao:
            return "projeto viável"
        else:
            return "projeto inviável"
            
    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prazo_dias": self.prazo_dias,
            "pontos_funcao": self.pontos_funcao,
            "desenvolvedores": [dev.to_dict() for dev in self.desenvolvedores]
        }

banco_devs: Dict[int, Desenvolvedor] = {}
banco_projetos: Dict[int, Projeto] = {}

gerador_id_dev = 1
gerador_id_proj = 1

@app.route("/desenvolvedores", methods=["POST"])
def post_desenvolvedor():
    global gerador_id_dev
    dados = request.get_json()
    
    novo_dev = Desenvolvedor.cadastrar_desenvolvedor(
        gerador_id_dev, 
        dados.get("nome"), 
        dados.get("senioridade"), 
        dados.get("pontos_por_dia"), 
        dados.get("linguagem")
    )
    banco_devs[gerador_id_dev] = novo_dev
    gerador_id_dev += 1
    
    return jsonify({"mensagem": "Desenvolvedor cadastrado", "id": novo_dev.id}), 201

@app.route("/desenvolvedores", methods=["GET"])
def get_desenvolvedores():
    return jsonify([dev.to_dict() for dev in banco_devs.values()]), 200

@app.route("/desenvolvedores/<int:id>", methods=["GET"])
def get_desenvolvedor_por_id(id):
    if id not in banco_devs:
        return jsonify({"erro": "Desenvolvedor não encontrado"}), 404
    return jsonify(banco_devs[id].to_dict()), 200


@app.route("/projetos", methods=["POST"])
def post_projeto():
    global gerador_id_proj
    dados = request.get_json()
    
    novo_proj = Projeto.criar_projeto(
        gerador_id_proj, 
        dados.get("descricao"), 
        dados.get("prazo_dias"), 
        dados.get("pontos_funcao")
    )
    banco_projetos[gerador_id_proj] = novo_proj
    gerador_id_proj += 1
    
    return jsonify({"mensagem": "Projeto criado", "id": novo_proj.id}), 201

@app.route("/projetos/<int:id>/desenvolvedores", methods=["POST"])
def post_dev_no_projeto(id):
    if id not in banco_projetos:
        return jsonify({"erro": "Projeto não encontrado"}), 404
        
    dados = request.get_json()
    desenvolvedor_id = dados.get("desenvolvedor_id")
    
    if desenvolvedor_id not in banco_devs:
        return jsonify({"erro": "Desenvolvedor não encontrado"}), 404
    
    projeto = banco_projetos[id]
    dev = banco_devs[desenvolvedor_id]
    
    projeto.adicionar_desenvolvedor(dev)
    return jsonify({"mensagem": f"Desenvolvedor '{dev.nome}' adicionado ao projeto '{projeto.descricao}'."}), 200

@app.route("/projetos", methods=["GET"])
def get_projetos():
    return jsonify([proj.to_dict() for proj in banco_projetos.values()]), 200

@app.route("/projetos/<int:id>", methods=["GET"])
def get_projeto_por_id(id):
    if id not in banco_projetos:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    return jsonify(banco_projetos[id].to_dict()), 200

@app.route("/projetos/<int:id>/desenvolvedores", methods=["GET"])
def get_devs_do_projeto(id):
    if id not in banco_projetos:
        return jsonify({"erro": "Projeto não encontrado"}), 404
        
    devs = banco_projetos[id].desenvolvedores
    return jsonify([dev.to_dict() for dev in devs]), 200

@app.route("/projetos/<int:id>/viabilidade", methods=["GET"])
def get_viabilidade_projeto(id):
    if id not in banco_projetos:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    
    projeto = banco_projetos[id]
    return jsonify({
        "projeto_id": projeto.id,
        "descricao": projeto.descricao,
        "pontos_funcao": projeto.pontos_funcao,
        "capacidade_equipe": projeto.calcular_capacidade_total(),
        "status_viabilidade": projeto.verificar_viabilidade()
    }), 200

if __name__ == "__main__":
    app.run(debug=True)