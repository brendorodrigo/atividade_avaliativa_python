from flask import Flask, request, jsonify

app = Flask(__name__)

desenvolvedor_id_counter = 1
projeto_id_counter = 1

desenvolvedores = []
projetos = []

class Desenvolvedor:
    def __init__(self, nome, senioridade, pontos_por_dia, linguagem):
        global desenvolvedor_id_counter
        self.id = desenvolvedor_id_counter
        desenvolvedor_id_counter += 1
        self.nome = nome
        self.senioridade = senioridade
        self.pontos_por_dia = pontos_por_dia
        self.linguagem = linguagem

    @classmethod
    def cadastrar_desenvolvedor(cls, nome, senioridade, pontos_por_dia, linguagem):
        return cls(nome, senioridade, pontos_por_dia, linguagem)

class Projeto:
    def __init__(self, descricao, prazo_dias, pontos_funcao):
        global projeto_id_counter
        self.id = projeto_id_counter
        projeto_id_counter += 1
        self.descricao = descricao
        self.prazo_dias = prazo_dias
        self.pontos_funcao = pontos_funcao
        self.desenvolvedores = []

    @classmethod
    def criar_projeto(cls, descricao, prazo_dias, pontos_funcao):
        return cls(descricao, prazo_dias, pontos_funcao)

    def adicionar_desenvolvedor(self, desenvolvedor):
        if desenvolvedor not in self.desenvolvedores:
            self.desenvolvedores.append(desenvolvedor)

    def calcular_capacidade_total(self):
        return sum(d.pontos_por_dia for d in self.desenvolvedores) * self.prazo_dias

    def verificar_viabilidade(self):
        capacidade = self.calcular_capacidade_total()
        if capacidade >= self.pontos_funcao:
            return "projeto viável"
        else:
            return "projeto inviável"

@app.route('/desenvolvedores', methods=['POST'])
def criar_desenvolvedor():
    data = request.get_json()
    nome = data.get('nome')
    senioridade = data.get('senioridade')
    pontos_por_dia = data.get('pontos_por_dia')
    linguagem = data.get('linguagem')
    if not all([nome, senioridade, pontos_por_dia, linguagem]):
        return jsonify({'error': 'Campos obrigatórios: nome, senioridade, pontos_por_dia, linguagem'}), 400
    dev = Desenvolvedor.cadastrar_desenvolvedor(nome, senioridade, pontos_por_dia, linguagem)
    desenvolvedores.append(dev)
    return jsonify({'id': dev.id, 'nome': dev.nome, 'senioridade': dev.senioridade, 'pontos_por_dia': dev.pontos_por_dia, 'linguagem': dev.linguagem}), 201

@app.route('/desenvolvedores', methods=['GET'])
def listar_desenvolvedores():
    return jsonify([{'id': d.id, 'nome': d.nome, 'senioridade': d.senioridade, 'pontos_por_dia': d.pontos_por_dia, 'linguagem': d.linguagem} for d in desenvolvedores])

@app.route('/desenvolvedores/<int:id>', methods=['GET'])
def obter_desenvolvedor(id):
    dev = next((d for d in desenvolvedores if d.id == id), None)
    if dev:
        return jsonify({'id': dev.id, 'nome': dev.nome, 'senioridade': dev.senioridade, 'pontos_por_dia': dev.pontos_por_dia, 'linguagem': dev.linguagem})
    return jsonify({'error': 'Desenvolvedor não encontrado'}), 404

@app.route('/projetos', methods=['POST'])
def criar_projeto():
    data = request.get_json()
    descricao = data.get('descricao')
    prazo_dias = data.get('prazo_dias')
    pontos_funcao = data.get('pontos_funcao')
    if not all([descricao, prazo_dias, pontos_funcao]):
        return jsonify({'error': 'Campos obrigatórios: descricao, prazo_dias, pontos_funcao'}), 400
    proj = Projeto.criar_projeto(descricao, prazo_dias, pontos_funcao)
    projetos.append(proj)
    return jsonify({'id': proj.id, 'descricao': proj.descricao, 'prazo_dias': proj.prazo_dias, 'pontos_funcao': proj.pontos_funcao, 'desenvolvedores': []}), 201

@app.route('/projetos/<int:id>/desenvolvedores', methods=['POST'])
def adicionar_desenvolvedor_projeto(id):
    proj = next((p for p in projetos if p.id == id), None)
    if not proj:
        return jsonify({'error': 'Projeto não encontrado'}), 404
    data = request.get_json()
    desenvolvedor_id = data.get('desenvolvedor_id')
    if not desenvolvedor_id:
        return jsonify({'error': 'Campo obrigatório: desenvolvedor_id'}), 400
    dev = next((d for d in desenvolvedores if d.id == desenvolvedor_id), None)
    if not dev:
        return jsonify({'error': 'Desenvolvedor não encontrado'}), 404
    proj.adicionar_desenvolvedor(dev)
    return jsonify({'message': 'Desenvolvedor adicionado ao projeto'}), 200

@app.route('/projetos', methods=['GET'])
def listar_projetos():
    return jsonify([{'id': p.id, 'descricao': p.descricao, 'prazo_dias': p.prazo_dias, 'pontos_funcao': p.pontos_funcao, 'desenvolvedores': [{'id': d.id, 'nome': d.nome} for d in p.desenvolvedores]} for p in projetos])

@app.route('/projetos/<int:id>', methods=['GET'])
def obter_projeto(id):
    proj = next((p for p in projetos if p.id == id), None)
    if proj:
        return jsonify({'id': proj.id, 'descricao': proj.descricao, 'prazo_dias': proj.prazo_dias, 'pontos_funcao': proj.pontos_funcao, 'desenvolvedores': [{'id': d.id, 'nome': d.nome} for d in proj.desenvolvedores]})
    return jsonify({'error': 'Projeto não encontrado'}), 404

@app.route('/projetos/<int:id>/desenvolvedores', methods=['GET'])
def listar_desenvolvedores_projeto(id):
    proj = next((p for p in projetos if p.id == id), None)
    if proj:
        return jsonify([{'id': d.id, 'nome': d.nome, 'senioridade': d.senioridade, 'pontos_por_dia': d.pontos_por_dia, 'linguagem': d.linguagem} for d in proj.desenvolvedores])
    return jsonify({'error': 'Projeto não encontrado'}), 404

@app.route('/projetos/<int:id>/viabilidade', methods=['GET'])
def verificar_viabilidade_projeto(id):
    proj = next((p for p in projetos if p.id == id), None)
    if proj:
        viabilidade = proj.verificar_viabilidade()
        return jsonify({'viabilidade': viabilidade})
    return jsonify({'error': 'Projeto não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)