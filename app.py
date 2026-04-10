from flask import Flask, jsonify, request

app = Flask(__name__)

desenvolvedores = []
projetos = []

class Desenvolvedor:
    def __init__(self, id, nome, senioridade, pontos_por_dia, linguagem):
        self.id = id
        self.nome = nome
        self.senioridade = senioridade
        self.pontos_por_dia = pontos_por_dia
        self.linguagem = linguagem

class Projeto:
    def __init__(self, id, descricao, prazo_dias, pontos_funcao):
        self.id = id
        self.descricao = descricao
        self.prazo_dias = prazo_dias
        self.pontos_funcao = pontos_funcao
        self.devs_equipe = [] 
    def calcular_capacidade(self):
        soma_pontos = sum(d.pontos_por_dia for d in self.devs_equipe)
        return soma_pontos * self.prazo_dias


@app.route('/desenvolvedores', methods=['POST'])
def cadastrar_dev():
    dados = request.get_json()
    novo_id = len(desenvolvedores) + 1
    
    dev = Desenvolvedor(novo_id, dados['nome'], dados['senioridade'], 
                        dados['pontos_por_dia'], dados['linguagem'])
    
    desenvolvedores.append(dev)
    return jsonify({"mensagem": "Dev cadastrado!", "id": dev.id}), 201

@app.route('/desenvolvedores', methods=['GET'])
def listar_devs():
    lista_limpa = [dev.__dict__ for dev in desenvolvedores]
    return jsonify(lista_limpa)

@app.route('/projetos', methods=['POST'])
def criar_projeto():
    dados = request.get_json()
    novo_id = len(projetos) + 1
    
    proj = Projeto(novo_id, dados['descricao'], dados['prazo_dias'], dados['pontos_funcao'])
    projetos.append(proj)
    return jsonify({"mensagem": "Projeto criado!", "id": proj.id}), 201

@app.route('/projetos/<int:proj_id>/desenvolvedores', methods=['POST'])
def adicionar_dev_ao_projeto(proj_id):
    dados = request.get_json()
    dev_id = dados['desenvolvedor_id']
    
    projeto = next((p for p in projetos if p.id == proj_id), None)
    desenvolvedor = next((d for d in desenvolvedores if d.id == dev_id), None)
    
    if projeto and desenvolvedor:
        projeto.devs_equipe.append(desenvolvedor)
        return jsonify({"mensagem": f"Dev {desenvolvedor.nome} adicionado ao projeto!"})
    
    return jsonify({"erro": "Não encontrado"}), 404

@app.route('/projetos/<int:proj_id>/viabilidade', methods=['GET'])
def verificar_viabilidade(proj_id):
    projeto = next((p for p in projetos if p.id == proj_id), None)
    
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    
    capacidade = projeto.calcular_capacidade()
    viavel = capacidade >= projeto.pontos_funcao
    
    return jsonify({
        "projeto": projeto.descricao,
        "capacidade_total": capacidade,
        "pontos_necessarios": projeto.pontos_funcao,
        "status": "Viável" if viavel else "Inviável"
    })

if __name__ == '__main__':
    app.run(debug=True)