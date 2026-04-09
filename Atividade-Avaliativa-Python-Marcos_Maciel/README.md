# API de Gerenciamento de Projetos e Desenvolvedores

Aplicação REST API para gerenciar projetos, desenvolvedores e análise de viabilidade de projetos.

## Instalação

### 1. Criar um ambiente virtual (recomendado)

```bash
python -m venv venv
```

### 2. Ativar o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## Executando a API

```bash
python main.py
```

A API estará disponível em: **http://localhost:8000**

### Acessar documentação interativa

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints da API

### Desenvolvedores

#### POST /desenvolvedores
Criar um novo desenvolvedor
```json
{
    "nome": "João",
    "senioridade": "Pleno",
    "pontos_por_dia": 5,
    "linguagem": "Python"
}
```

#### GET /desenvolvedores
Lista todos os desenvolvedores

#### GET /desenvolvedores/{id}
Obtém um desenvolvedor específico

### Projetos

#### POST /projetos
Criar um novo projeto
```json
{
    "descricao": "Sistema de pagamentos",
    "prazo_dias": 30,
    "pontos_funcao": 200
}
```

#### GET /projetos
Lista todos os projetos

#### GET /projetos/{id}
Obtém um projeto específico

#### POST /projetos/{id}/desenvolvedores
Adicionar desenvolvedor ao projeto
```json
{
    "desenvolvedor_id": 1
}
```

#### GET /projetos/{id}/desenvolvedores
Lista desenvolvedores alocados ao projeto

#### GET /projetos/{id}/viabilidade
Verifica viabilidade do projeto (e retorna a análise detalhada)

**Resposta exemplo:**
```json
{
    "projeto_id": 1,
    "descricao": "Sistema de pagamentos",
    "viavel": true,
    "motivo": "Projeto viável",
    "capacidade_total": 300,
    "pontos_necessarios": 200,
    "deficit": 0,
    "prazo_dias": 30,
    "desenvolvedores_alocados": 2
}
```

### Saúde da API

#### GET /health
Verifica o status da API

## Estrutura do Projeto

```
.
├── main.py              # Aplicação principal com os endpoints
├── models.py            # Modelos de dados (Desenvolvedor, Projeto)
├── requirements.txt     # Dependências do projeto
└── README.md           # Esta documentação
```

## Classes

### Desenvolvedor
- **id**: Identificador único
- **nome**: Nome do desenvolvedor
- **senioridade**: Junior, Pleno ou Senior
- **pontos_por_dia**: Capacidade de trabalho em pontos/dia
- **linguagem**: Linguagem de programação principal

**Métodos:**
- `cadastrar_desenvolvedor()`: Registra o desenvolvedor

### Projeto
- **id**: Identificador único
- **descricao**: Descrição do projeto
- **prazo_dias**: Prazo em dias
- **pontos_funcao**: Pontos de função a entregar
- **desenvolvedores**: Lista de IDs dos desenvolvedores alocados

**Métodos:**
- `criar_projeto()`: Cria o projeto
- `adicionar_desenvolvedor(desenvolvedor_id)`: Adiciona desenvolvedor ao projeto
- `calcular_capacidade_total(desenvolvedores_list)`: Calcula pontos que podem ser entregues
- `verificar_viabilidade(desenvolvedores_list)`: Verifica se projeto é viável

## Lógica de Viabilidade

Um projeto é considerado **viável** quando:

```
capacidade_total >= pontos_funcao

Onde: capacidade_total = Σ(pontos_por_dia × prazo_dias) para cada desenvolvedor
```

Um projeto é considerado **inviável** quando não há desenvolvedores alocados ou a capacidade é insuficiente.
