from flask import Flask, request, jsonify

# --- MODELOS ---

class MembroEquipe:
    def __init__(self, id, nome, cargo, produtividade):
        self.id = id
        self.nome = nome
        self.cargo = cargo
        self.produtividade = produtividade  # Pontos de esforço que consegue entregar por dia

class Tarefa:
    def __init__(self, id, titulo, esforco_total):
        self.id = id
        self.titulo = titulo
        self.esforco_total = esforco_total  # Total de "pontos" para concluir
        self.responsavel = None
        self.status = "Pendente"

    def atribuir(self, membro):
        self.responsavel = membro
        self.status = "Em andamento"

    def calcular_dias_estimados(self):
        if not self.responsavel:
            return None
        return self.esforco_total / self.responsavel.produtividade

# --- APP FLASK ----

app = Flask(__name__)

# Simulação de Banco de Dados
equipe = {}
tarefas = {}
id_membro_seq = 1
id_tarefa_seq = 1

# --- ROTAS ---

@app.route('/equipe', methods=['POST'])
def adicionar_membro():
    global id_membro_seq
    dados = request.get_json()
    
    novo_membro = MembroEquipe(
        id_membro_seq,
        dados['nome'],
        dados['cargo'],
        dados['produtividade']
    )
    
    equipe[id_membro_seq] = novo_membro
    id_membro_seq += 1
    return jsonify({"msg": "Membro da equipe registrado!", "id": novo_membro.id}), 201

@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    global id_tarefa_seq
    dados = request.get_json()
    
    nova_tarefa = Tarefa(id_tarefa_seq, dados['titulo'], dados['esforco'])
    tarefas[id_tarefa_seq] = nova_tarefa
    id_tarefa_seq += 1
    return jsonify({"msg": "Tarefa criada!", "id": nova_tarefa.id}), 201

@app.route('/tarefas/<int:t_id>/atribuir/<int:m_id>', methods=['PATCH'])
def atribuir_tarefa(t_id, m_id):
    tarefa = tarefas.get(t_id)
    membro = equipe.get(m_id)
    
    if not tarefa or not membro:
        return jsonify({"erro": "Tarefa ou Membro não encontrado"}), 404
        
    tarefa.atribuir(membro)
    dias = tarefa.calcular_dias_estimados()
    
    return jsonify({
        "tarefa": tarefa.titulo,
        "responsavel": membro.nome,
        "estimativa_conclusao": f"{dias:.1f} dias"
    })

@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Retorna um resumo de tudo
    resultado = []
    for t in tarefas.values():
        info = {
            "id": t.id,
            "titulo": t.titulo,
            "status": t.status,
            "responsavel": t.responsavel.nome if t.responsavel else "Ninguém"
        }
        resultado.append(info)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)