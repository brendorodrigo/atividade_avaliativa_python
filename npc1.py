from flask import Flask, jsonify, request

app = Flask(__name__)



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

    def adicionar_desenvolvedor(self, desenvolvedor):
        self.desenvolvedores.append(desenvolvedor)
    
    def calcular_capacidade_total(self):
        return sum(dev.pontos_por_dia for dev in self.desenvolvedores)
    
    def verificar_viabilidade(self):
        
        capacidade_total_periodo = self.calcular_capacidade_total() * self.prazo_dias
        if capacidade_total_periodo < self.pontos_funcao:
            return "Projeto Inviável"
        return "Projeto viável"

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prazo_dias": self.prazo_dias,
            "pontos_funcao": self.pontos_funcao,
            "desenvolvedores": [dev.to_dict() for dev in self.desenvolvedores]
        }


lista_desenvolvedores = []
lista_projetos = []
id_dev_counter = 1
id_projeto_counter = 1



@app.route('/desenvolvedores', methods=['POST'])
def cadastrar_desenvolvedor():
    global id_dev_counter
    dados = request.get_json()
    novo_dev = Desenvolvedor(
        id=id_dev_counter,
        nome=dados['nome'],
        senioridade=dados['senioridade'],
        pontos_por_dia=dados['pontos_por_dia'],
        linguagem=dados['linguagem']
    )
    lista_desenvolvedores.append(novo_dev)
    id_dev_counter += 1
    return jsonify(novo_dev.to_dict()), 201

@app.route('/desenvolvedores', methods=['GET'])
def get_desenvolvedores():
    return jsonify([dev.to_dict() for dev in lista_desenvolvedores]), 200

@app.route('/desenvolvedores/<int:id>', methods=['GET'])
def get_dev_por_id(id):
    for dev in lista_desenvolvedores:
        if dev.id == id:
            return jsonify(dev.to_dict()), 200
    return jsonify({"erro": "Desenvolvedor não encontrado"}), 404



@app.route('/projetos', methods=['POST'])
def criar_projeto():
    global id_projeto_counter
    dados = request.get_json()
    novo_projeto = Projeto(
        id=id_projeto_counter,
        descricao=dados['descricao'],
        prazo_dias=dados['prazo_dias'],
        pontos_funcao=dados['pontos_funcao']
    )
    lista_projetos.append(novo_projeto)
    id_projeto_counter += 1
    return jsonify(novo_projeto.to_dict()), 201

@app.route('/projetos', methods=['GET'])
def get_projetos():
    return jsonify([p.to_dict() for p in lista_projetos]), 200

@app.route('/projetos/<int:id>', methods=['GET'])
def get_projeto_por_id(id):
    for p in lista_projetos:
        if p.id == id:
            return jsonify(p.to_dict()), 200
    return jsonify({"erro": "Projeto não encontrado"}), 404

@app.route('/projetos/<int:id_projeto>/desenvolvedores', methods=['POST'])
def add_dev_ao_projeto(id_projeto):
    dados = request.get_json()
    id_dev = dados['desenvolvedor_id']
    
    projeto = next((p for p in lista_projetos if p.id == id_projeto), None)
    desenvolvedor = next((d for d in lista_desenvolvedores if d.id == id_dev), None)
    
    if projeto and desenvolvedor:
        projeto.adicionar_desenvolvedor(desenvolvedor)
        return jsonify(projeto.to_dict()), 200
    return jsonify({"erro": "Projeto ou Desenvolvedor não encontrado"}), 404

@app.route('/projetos/<int:id>/desenvolvedores', methods=['GET'])
def listar_devs_do_projeto(id):
    projeto = next((p for p in lista_projetos if p.id == id), None)
    if projeto:
        return jsonify([dev.to_dict() for dev in projeto.desenvolvedores]), 200
    return jsonify({"erro": "Projeto não encontrado"}), 404

@app.route('/projetos/<int:id>/viabilidade', methods=['GET'])
def checar_viabilidade(id):
    projeto = next((p for p in lista_projetos if p.id == id), None)
    if projeto:
        return jsonify({
            "projeto": projeto.descricao,
            "viabilidade": projeto.verificar_viabilidade(),
            "capacidade_total": projeto.calcular_capacidade_total()
        }), 200
    return jsonify({"erro": "Projeto não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)