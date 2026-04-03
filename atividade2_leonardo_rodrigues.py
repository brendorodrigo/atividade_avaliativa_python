from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Contadores para IDs
contador_projetos = 0
contador_desenvolvedores = 0

# Armazenamento em memória
projetos = {}
desenvolvedores = {}


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

    @staticmethod
    def cadastrar_desenvolvedor(nome, senioridade, pontos_por_dia, linguagem):
        """Método para cadastrar um desenvolvedor"""
        global contador_desenvolvedores
        contador_desenvolvedores += 1
        dev = Desenvolvedor(contador_desenvolvedores, nome,
                            senioridade, pontos_por_dia, linguagem)
        desenvolvedores[contador_desenvolvedores] = dev
        return dev


class Projeto:
    def __init__(self, id, descricao, prazo_em_dias, pontos_funcao):
        self.id = id
        self.descricao = descricao
        self.prazo_em_dias = prazo_em_dias
        self.pontos_funcao = pontos_funcao
        self.desenvolvedores = []

    def adicionar_desenvolvedor(self, desenvolvedor):
        """Adiciona um desenvolvedor ao projeto"""
        self.desenvolvedores.append(desenvolvedor)

    def calcular_capacidade_total(self):
        """Calcula a capacidade total de pontos que os desenvolvedores conseguem fazer"""
        capacidade_pontos = 0
        for desenvolvedor in self.desenvolvedores:
            capacidade_pontos += desenvolvedor.pontos_por_dia
        return capacidade_pontos * self.prazo_em_dias

    def verificar_viabilidade(self):
        """
        Verifica se o projeto é viável comparando se a capacidade total
        dos desenvolvedores é suficiente para completar os pontos de função no prazo
        """
        capacidade_total = self.calcular_capacidade_total()
        if capacidade_total >= self.pontos_funcao:
            return {"status": "Projeto viável", "detalhes": {
                "pontos_requeridos": self.pontos_funcao,
                "capacidade_total": capacidade_total
            }}
        else:
            return {"status": "Projeto não viável", "detalhes": {
                "pontos_requeridos": self.pontos_funcao,
                "capacidade_total": capacidade_total
            }}

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prazo_em_dias": self.prazo_em_dias,
            "pontos_funcao": self.pontos_funcao,
            "desenvolvedores": [dev.id for dev in self.desenvolvedores]
        }

    @staticmethod
    def criar_projeto(descricao, prazo_em_dias, pontos_funcao):
        """Método para criar um projeto"""
        global contador_projetos
        contador_projetos += 1
        proj = Projeto(contador_projetos, descricao,
                       prazo_em_dias, pontos_funcao)
        projetos[contador_projetos] = proj
        return proj


# =============== ROTAS DA API - DESENVOLVEDORES ===============

@app.route('/desenvolvedores', methods=['POST'])
def criar_desenvolvedor():
    """POST /desenvolvedores - Cria um novo desenvolvedor"""
    data = request.json

    if not all(key in data for key in ['nome', 'senioridade', 'pontos_por_dia', 'linguagem']):
        return jsonify({"erro": "Faltam campos obrigatórios"}), 400

    dev = Desenvolvedor.cadastrar_desenvolvedor(
        nome=data['nome'],
        senioridade=data['senioridade'],
        pontos_por_dia=data['pontos_por_dia'],
        linguagem=data['linguagem']
    )

    return jsonify(dev.to_dict()), 201


@app.route('/desenvolvedores', methods=['GET'])
def listar_desenvolvedores():
    """GET /desenvolvedores - Lista todos os desenvolvedores"""
    lista = [dev.to_dict() for dev in desenvolvedores.values()]
    return jsonify(lista), 200


@app.route('/desenvolvedores/<int:id>', methods=['GET'])
def obter_desenvolvedor(id):
    """GET /desenvolvedores/{id} - Obtém um desenvolvedor específico"""
    if id not in desenvolvedores:
        return jsonify({"erro": "Desenvolvedor não encontrado"}), 404

    return jsonify(desenvolvedores[id].to_dict()), 200


# =============== ROTAS DA API - PROJETOS ===============

@app.route('/projetos', methods=['POST'])
def criar_projeto():
    """POST /projetos - Cria um novo projeto"""
    data = request.json

    if not all(key in data for key in ['descricao', 'prazo_dias', 'pontos_funcao']):
        return jsonify({"erro": "Faltam campos obrigatórios"}), 400

    proj = Projeto.criar_projeto(
        descricao=data['descricao'],
        prazo_em_dias=data['prazo_dias'],
        pontos_funcao=data['pontos_funcao']
    )

    return jsonify(proj.to_dict()), 201


@app.route('/projetos', methods=['GET'])
def listar_projetos():
    """GET /projetos - Lista todos os projetos"""
    lista = [proj.to_dict() for proj in projetos.values()]
    return jsonify(lista), 200


@app.route('/projetos/<int:id>', methods=['GET'])
def obter_projeto(id):
    """GET /projetos/{id} - Obtém um projeto específico"""
    if id not in projetos:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    return jsonify(projetos[id].to_dict()), 200


@app.route('/projetos/<int:id>/desenvolvedores', methods=['POST'])
def adicionar_desenvolvedor_projeto(id):
    """POST /projetos/{id}/desenvolvedores - Adiciona um desenvolvedor ao projeto"""
    if id not in projetos:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    data = request.json

    if 'desenvolvedor_id' not in data:
        return jsonify({"erro": "Campo 'desenvolvedor_id' obrigatório"}), 400

    dev_id = data['desenvolvedor_id']

    if dev_id not in desenvolvedores:
        return jsonify({"erro": "Desenvolvedor não encontrado"}), 404

    projetos[id].adicionar_desenvolvedor(desenvolvedores[dev_id])

    return jsonify({
        "mensagem": "Desenvolvedor adicionado com sucesso",
        "projeto": projetos[id].to_dict()
    }), 200


@app.route('/projetos/<int:id>/desenvolvedores', methods=['GET'])
def listar_desenvolvedores_projeto(id):
    """GET /projetos/{id}/desenvolvedores - Lista desenvolvedores de um projeto"""
    if id not in projetos:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    lista = [dev.to_dict() for dev in projetos[id].desenvolvedores]
    return jsonify(lista), 200


@app.route('/projetos/<int:id>/viabilidade', methods=['GET'])
def verificar_viabilidade_projeto(id):
    """GET /projetos/{id}/viabilidade - Verifica a viabilidade de um projeto"""
    if id not in projetos:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    resultado = projetos[id].verificar_viabilidade()
    return jsonify(resultado), 200


# =============== ROTA RAIZ ===============

@app.route('/', methods=['GET'])
def home():
    """Rota inicial - Informações sobre a API"""
    return jsonify({
        "mensagem": "API de Projetos e Desenvolvedores",
        "versao": "1.0",
        "endpoints": {
            "desenvolvedores": {
                "POST": "/desenvolvedores",
                "GET": "/desenvolvedores",
                "GET_ID": "/desenvolvedores/<id>"
            },
            "projetos": {
                "POST": "/projetos",
                "GET": "/projetos",
                "GET_ID": "/projetos/<id>",
                "ADICIONAR_DEV": "POST /projetos/<id>/desenvolvedores",
                "LISTAR_DEVS": "GET /projetos/<id>/desenvolvedores",
                "VIABILIDADE": "GET /projetos/<id>/viabilidade"
            }
        }
    }), 200


if __name__ == "__main__":
    # Exemplo de uso
    print("="*60)
    print("INICIANDO APLICAÇÃO")
    print("="*60)

    # Criar alguns desenvolvedores de exemplo
    dev1 = Desenvolvedor.cadastrar_desenvolvedor(
        "Leonardo", "Sênior", 15, "Python")
    dev2 = Desenvolvedor.cadastrar_desenvolvedor("Maria", "Pleno", 10, "Java")
    dev3 = Desenvolvedor.cadastrar_desenvolvedor("João", "Júnior", 5, "COBOL")

    # Criar um projeto de exemplo
    proj = Projeto.criar_projeto("Sistema de pagamentos", 30, 300)

    # Adicionar desenvolvedores ao projeto
    proj.adicionar_desenvolvedor(dev1)
    proj.adicionar_desenvolvedor(dev2)
    proj.adicionar_desenvolvedor(dev3)

    # Verificar viabilidade
    print("\nProjeto:", proj.descricao)
    print("Viabilidade:", proj.verificar_viabilidade())
    print("\n" + "="*60)
    print("Iniciando servidor Flask na porta 5000")
    print("Acesse http://localhost:5000 para ver os endpoints")
    print("="*60 + "\n")

    app.run(debug=True, port=5000)
