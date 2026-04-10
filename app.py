from flask import Flask, request, jsonify

app = Flask(__name__)

desenvolvedores = []
projetos = []

@app.route('/desenvolvedores', methods=['POST'])
def cadastrar_desenvolvedor():
    dados = request.get_json()
    novo_dev = {
        "id": len(desenvolvedores) + 1,
        "nome": dados['nome'],
        "senioridade": dados['senioridade'],
        "pontos_por_dia": dados['pontos_por_dia'],
        "linguagem": dados['linguagem']
    }
    desenvolvedores.append(novo_dev)
    return jsonify(novo_dev), 201

@app.route('/desenvolvedores', methods=['GET'])
def listar_desenvolvedores():
    return jsonify(desenvolvedores), 200

@app.route('/projetos', methods=['POST'])
def criar_projeto():
    dados = request.get_json()
    novo_p = {
        "id": len(projetos) + 1, 
        "descricao": dados['descricao'], 
        "prazo_dias": dados['prazo_dias'], 
        "pontos_funcao": dados['pontos_funcao'], 
        "desenvolvedores": []
    }
    projetos.append(novo_p)
    return jsonify(novo_p), 201

@app.route('/projetos/<int:id>/desenvolvedores', methods=['POST'])
def add_dev_proj(id):
    dados = request.get_json()
    for p in projetos:
        if p['id'] == id:
            p['desenvolvedores'].append(dados['desenvolvedor_id'])
            return jsonify(p), 200
    return jsonify({"erro": "nao encontrado"}), 404

@app.route('/projetos/<int:id>/viabilidade', methods=['GET'])
def verificar_viabilidade(id):
    projeto = next((p for p in projetos if p['id'] == id), None)
    if not projeto:
        return jsonify({"erro": "nao encontrado"}), 404
    
    # Soma a capacidade de todos os devs que estão nesse projeto
    cap_total = 0
    for dev_id in projeto['desenvolvedores']:
        dev = next((d for d in desenvolvedores if d['id'] == dev_id), None)
        if dev:
            cap_total += dev['pontos_por_dia']
            
    necessario = projeto['pontos_funcao'] / projeto['prazo_dias']
    
    return jsonify({
        "projeto": projeto['descricao'],
        "viavel": cap_total >= necessario,
        "capacidade_equipe": cap_total,
        "necessario_por_dia": necessario
    }), 200

if __name__ == '__main__':
    app.run(debug=True)