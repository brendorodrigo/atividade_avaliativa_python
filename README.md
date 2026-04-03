<h1> Atividade Avaliativa para NPC I</h1>
<ul>
<li>Implemente a organização das classes Projetos e Desenvolvedores</li>
<pre>
Projeto:
  Atributos:
    - ID
    - Descrição
    - Prazo em dias
    - Pontos de função
    - [Desenvolvedores]
  Metodos:
    - criar_projeto
    - adicionar_desenvolvedor
    - calcular_capacidade_total
    - verificar_viabilidade
      - projeto viável
      - projeto inviável
</pre>
<pre>
Desenvolvedor:
  - id
  - Nome
  - Senioridade
  - Pontos por dia
  - Linguagem

  Metodos: 
  - cadastrar_desenvolvedor
</pre>

<li>Criar as seguintes APIs com os seguintes retornos</li>


Desenvolvedores: 
<pre>
POST /desenvolvedores
        body: {
            "nome": "João",
            "senioridade": "Pleno",
            "pontos_por_dia": 5,
            "linguagem": "Python"
        }
GET /desenvolvedores
GET /desenvolvedores/{id}
</pre>

Projeto: 
<pre>
POST /projetos
        body: {
            "descricao": "Sistema de pagamentos",
            "prazo_dias": 30,
            "pontos_funcao": 200
        } 
POST /projetos/{id}/desenvolvedores
        body: {
            "desenvolvedor_id": 1
        }
GET /projetos
GET /projetos/{id}
GET /projetos/{id}/desenvolvedores
GET /projetos/{id}/viabilidade

</pre>

