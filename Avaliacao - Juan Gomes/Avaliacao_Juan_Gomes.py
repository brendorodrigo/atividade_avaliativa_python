from flask import Flask, request, jsonify

# --- CLASSES ---

class Programador:
    def __init__(self, codigo, nome, comprometimento, produtividade_dia, tecnologia):
        self.codigo = codigo
        self.nome = nome
        self.comprometimento = comprometimento
        self.produtividade_dia = produtividade_dia
        self.tecnologia = tecnologia


class SistemaProjeto:
    def __init__(self, codigo, titulo, duracao_dias, total_pontos):
        self.codigo = codigo
        self.titulo = titulo
        self.duracao_dias = duracao_dias
        self.total_pontos = total_pontos
        self.equipe = []

    def incluir_programador(self, programador):
        self.equipe.append(programador)

    def calcular_produtividade(self):
        return sum(p.produtividade_dia for p in self.equipe)

    def analisar_viabilidade(self):
        produtividade = self.calcular_produtividade()
        demanda_diaria = self.total_pontos / self.duracao_dias

        if produtividade >= demanda_diaria:
            return "Viável"
        else:
            return "Inviável"


# --- API ---

app = Flask(__name__)

# Armazenamento temporário
lista_programadores = []
lista_projetos = []
contador_prog = 1
contador_proj = 1

# --- ROTAS PROGRAMADORES ---

@app.route('/programadores', methods=['POST'])
def cadastrar_programador():
    global contador_prog
    info = request.get_json()

    prog = Programador(
        contador_prog,
        info.get('nome'),
        info.get('comprometimento'),
        info.get('produtividade_dia'),
        info.get('tecnologia')
    )

    lista_programadores.append(prog)
    contador_prog += 1

    return jsonify({
        'mensagem': 'Programador cadastrado',
        'codigo': prog.codigo
    }), 201


@app.route('/programadores', methods=['GET'])
def obter_programadores():
    return jsonify([{
        'codigo': p.codigo,
        'nome': p.nome,
        'tecnologia': p.tecnologia,
        'produtividade': p.produtividade_dia
    } for p in lista_programadores])


# --- ROTAS PROJETOS ---

@app.route('/projetos', methods=['POST'])
def cadastrar_projeto():
    global contador_proj
    info = request.get_json()

    projeto = SistemaProjeto(
        contador_proj,
        info.get('titulo'),
        info.get('duracao_dias'),
        info.get('total_pontos')
    )

    lista_projetos.append(projeto)
    contador_proj += 1

    return jsonify({
        'mensagem': 'Projeto cadastrado',
        'codigo': projeto.codigo
    }), 201


@app.route('/projetos/<int:codigo>/adicionar_programador', methods=['POST'])
def adicionar_programador_ao_projeto(codigo):
    info = request.get_json()
    cod_prog = info.get('codigo_programador')

    projeto = next((p for p in lista_projetos if p.codigo == codigo), None)
    prog = next((p for p in lista_programadores if p.codigo == cod_prog), None)

    if projeto and prog:
        projeto.incluir_programador(prog)
        return jsonify({
            'mensagem': f'{prog.nome} adicionado ao projeto {projeto.titulo}'
        })

    return jsonify({'erro': 'Projeto ou programador não encontrado'}), 404


@app.route('/projetos/<int:codigo>/status', methods=['GET'])
def verificar_status_projeto(codigo):
    projeto = next((p for p in lista_projetos if p.codigo == codigo), None)

    if projeto:
        resultado = projeto.analisar_viabilidade()
        return jsonify({
            'projeto': projeto.titulo,
            'status': resultado,
            'produtividade_total': projeto.calcular_produtividade(),
            'demanda_diaria': projeto.total_pontos / projeto.duracao_dias
        })

    return jsonify({'erro': 'Projeto não encontrado'}), 404


if __name__ == '__main__':
    app.run(debug=True)