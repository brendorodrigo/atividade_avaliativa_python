# Documentação Técnica - Atividade Avaliativa NPC I

## 📋 Descrição da Atividade

Implementação de um sistema de gerenciamento de projetos e desenvolvedores com análise de viabilidade de projetos através de uma API REST.

## 🏗️ Diagrama de Classes

```
┌─────────────────────────────┐
│      Desenvolvedor          │
├─────────────────────────────┤
│ - id: int                   │
│ - nome: str                 │
│ - senioridade: str          │
│ - pontos_por_dia: float     │
│ - linguagem: str            │
├─────────────────────────────┤
│ + cadastrar_desenvolvedor() │
└─────────────────────────────┘
           △
           │
           │ alocado em
           │
┌─────────────────────────────┐
│        Projeto              │
├─────────────────────────────┤
│ - id: int                   │
│ - descricao: str            │
│ - prazo_dias: int           │
│ - pontos_funcao: int        │
│ - desenvolvedores: List[int]│
├─────────────────────────────┤
│ + criar_projeto()           │
│ + adicionar_desenvolvedor() │
│ + calcular_capacidade()     │
│ + verificar_viabilidade()   │
└─────────────────────────────┘
```

## 📊 Fluxo de Viabilidade

```
                    ANÁLISE DE VIABILIDADE
                           │
                    ┌──────┴──────┐
                    │             │
            Há desenvolvedores?   │
               SIM│   │NÃO        │
                  │   └──→ INVIÁVEL│
                  │                │
          Calcular Capacidade      │
                  │                │
          capacidade = Σ(pontos_por_dia × prazo_dias)
                  │
          ┌───────┴────────┐
          │                │
    capacidade >= VIÁVEL   INVIÁVEL
    pontos_funcao?
         │
       SIM │ NÃO
```

## 🔧 Tecnologias Utilizadas

- **Framework**: FastAPI (Python)
- **Validação**: Pydantic
- **Servidor**: Uvicorn
- **Documentação**: Swagger/ReDoc (automático)

## 📝 Especificações de Implementação

### Classe Desenvolvedor

```python
class Desenvolvedor:
    - id: Optional[int]
    - nome: str
    - senioridade: str (Junior, Pleno, Senior)
    - pontos_por_dia: float
    - linguagem: str
    
    Métodos:
    - cadastrar_desenvolvedor() → dict
```

**Exemplo:**
```json
{
    "id": 1,
    "nome": "João Silva",
    "senioridade": "Pleno",
    "pontos_por_dia": 5,
    "linguagem": "Python"
}
```

### Classe Projeto

```python
class Projeto:
    - id: Optional[int]
    - descricao: str
    - prazo_dias: int
    - pontos_funcao: int
    - desenvolvedores: List[int]
    
    Métodos:
    - criar_projeto() → dict
    - adicionar_desenvolvedor(dev_id) → dict
    - calcular_capacidade_total(devs_list) → float
    - verificar_viabilidade(devs_list) → dict
```

**Exemplo:**
```json
{
    "id": 1,
    "descricao": "Sistema de pagamentos",
    "prazo_dias": 30,
    "pontos_funcao": 200,
    "desenvolvedores": [1, 2]
}
```

## 🔌 Endpoints da API

### Desenvolvedores

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | /desenvolvedores | Criar desenvolvedor |
| GET | /desenvolvedores | Listar todos |
| GET | /desenvolvedores/{id} | Obter um |

### Projetos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | /projetos | Criar projeto |
| GET | /projetos | Listar todos |
| GET | /projetos/{id} | Obter um |
| POST | /projetos/{id}/desenvolvedores | Adicionar desenvolvedor |
| GET | /projetos/{id}/desenvolvedores | Listar desenvolvedores |
| GET | /projetos/{id}/viabilidade | Verificar viabilidade |

## 📈 Lógica de Cálculo de Viabilidade

**Fórmula:**
```
Capacidade Total = Σ(pontos_por_dia[i] × prazo_dias) para cada desenvolvedor i

Viável = Capacidade Total ≥ Pontos de Função
```

**Exemplo Prático:**

Projeto: "Sistema de Pagamentos"
- Prazo: 30 dias
- Pontos: 200

Desenvolvedores alocados:
1. João (Pleno): 5 pontos/dia → 5 × 30 = 150 pontos
2. Maria (Senior): 8 pontos/dia → 8 × 30 = 240 pontos

**Capacidade Total = 150 + 240 = 390 pontos**

**Resultado:** 390 ≥ 200 → ✅ **VIÁVEL**

## 🎯 Resposta de Viabilidade

```json
{
    "projeto_id": 1,
    "descricao": "Sistema de pagamentos",
    "viavel": true,
    "motivo": "Projeto viável",
    "capacidade_total": 390,
    "pontos_necessarios": 200,
    "deficit": 0,
    "prazo_dias": 30,
    "desenvolvedores_alocados": 2
}
```

## 🚀 Como Iniciar

### 1. Instalação de dependências
```bash
pip install -r requirements.txt
```

### 2. Executar a API
```bash
python main.py
```

### 3. Acessar documentação (Swagger)
```
http://localhost:8000/docs
```

### 4. Testar com o script
```bash
python test_api.py
```

## 📁 Estrutura de Arquivos

```
Atividade-Avaliativa-Python-Marcos_Maciel/
│
├── main.py                 # API Principal (FastAPI)
├── models.py              # Classes Desenvolvedor e Projeto
├── test_api.py            # Script de teste com requests
├── requests.http          # Exemplos de requisições HTTP
├── requirements.txt       # Dependências Python
├── README.md             # Documentação básica
└── SPEC.md              # Esta documentação técnica
```

## 🧪 Casos de Teste

### Caso 1: Projeto Viável
```
1. Criar projeto: 100 pontos, 20 dias
2. Alocar Senior (8 pt/dia): 8 × 20 = 160 pontos
3. Resultado: 160 ≥ 100 ✅ VIÁVEL
```

### Caso 2: Projeto Inviável (sem dev)
```
1. Criar projeto: 500 pontos
2. Não alocar desenvolvedores
3. Resultado: 0 < 500 ❌ INVIÁVEL
```

### Caso 3: Projeto Inviável (capacidade baixa)
```
1. Criar projeto: 300 pontos, 10 dias
2. Alocar Junior (2 pt/dia): 2 × 10 = 20 pontos
3. Resultado: 20 < 300 ❌ INVIÁVEL (DEFICIT: 280)
```

## 🔐 Tratamento de Erros

A API retorna:

| Código | Situação |
|--------|----------|
| 201 | Recurso criado com sucesso |
| 200 | Requisição bem-sucedida |
| 400 | Dados inválidos ou desenvolvedor já alocado |
| 404 | Recurso não encontrado |
| 500 | Erro interno do servidor |

## 💡 Características Adicionais

✅ Validação automática de dados (Pydantic)
✅ Documentação automática (Swagger/ReDoc)
✅ CORS habilitado
✅ Incrementadores automáticos de ID
✅ Tratamento de erros consistente
✅ Armazenamento em memória
✅ Exemplos de requisições HTTP

## 📚 Referências

- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/
- Uvicorn: https://www.uvicorn.org/
