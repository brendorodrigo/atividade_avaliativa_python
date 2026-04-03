# API de Projetos e Desenvolvedores - Exemplos de Uso

## Como Iniciar a API

Para iniciar o servidor Flask, execute:

```bash
python atividade2_leonardo_rodrigues.py
```

O servidor iniciará em `http://localhost:5000`

---

## Exemplos de Requisições com cURL

### DESENVOLVEDORES

#### 1. Criar um novo desenvolvedor
```bash
curl -X POST http://localhost:5000/desenvolvedores \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João",
    "senioridade": "Pleno",
    "pontos_por_dia": 5,
    "linguagem": "Python"
  }'
```

**Resposta esperada:**
```json
{
  "id": 1,
  "nome": "João",
  "senioridade": "Pleno",
  "pontos_por_dia": 5,
  "linguagem": "Python"
}
```

#### 2. Listar todos os desenvolvedores
```bash
curl http://localhost:5000/desenvolvedores
```

#### 3. Obter um desenvolvedor específico
```bash
curl http://localhost:5000/desenvolvedores/1
```

---

### PROJETOS

#### 1. Criar um novo projeto
```bash
curl -X POST http://localhost:5000/projetos \
  -H "Content-Type: application/json" \
  -d '{
    "descricao": "Sistema de pagamentos",
    "prazo_dias": 30,
    "pontos_funcao": 200
  }'
```

**Resposta esperada:**
```json
{
  "id": 1,
  "descricao": "Sistema de pagamentos",
  "prazo_em_dias": 30,
  "pontos_funcao": 200,
  "desenvolvedores": []
}
```

#### 2. Listar todos os projetos
```bash
curl http://localhost:5000/projetos
```

#### 3. Obter um projeto específico
```bash
curl http://localhost:5000/projetos/1
```

#### 4. Adicionar um desenvolvedor a um projeto
```bash
curl -X POST http://localhost:5000/projetos/1/desenvolvedores \
  -H "Content-Type: application/json" \
  -d '{
    "desenvolvedor_id": 1
  }'
```

#### 5. Listar desenvolvedores de um projeto
```bash
curl http://localhost:5000/projetos/1/desenvolvedores
```

#### 6. Verificar viabilidade de um projeto
```bash
curl http://localhost:5000/projetos/1/viabilidade
```

**Resposta esperada:**
```json
{
  "status": "Projeto viável",
  "detalhes": {
    "pontos_requeridos": 200,
    "capacidade_total": 750
  }
}
```

---

## Exemplo Completo de Fluxo

1. **Criar desenvolvedores:**
```bash
curl -X POST http://localhost:5000/desenvolvedores \
  -H "Content-Type: application/json" \
  -d '{"nome": "Leonardo", "senioridade": "Sênior", "pontos_por_dia": 15, "linguagem": "Python"}'

curl -X POST http://localhost:5000/desenvolvedores \
  -H "Content-Type: application/json" \
  -d '{"nome": "Maria", "senioridade": "Pleno", "pontos_por_dia": 10, "linguagem": "Java"}'
```

2. **Criar um projeto:**
```bash
curl -X POST http://localhost:5000/projetos \
  -H "Content-Type: application/json" \
  -d '{"descricao": "App Mobile", "prazo_dias": 45, "pontos_funcao": 500}'
```

3. **Adicionar desenvolvedores ao projeto:**
```bash
curl -X POST http://localhost:5000/projetos/1/desenvolvedores \
  -H "Content-Type: application/json" \
  -d '{"desenvolvedor_id": 1}'

curl -X POST http://localhost:5000/projetos/1/desenvolvedores \
  -H "Content-Type: application/json" \
  -d '{"desenvolvedor_id": 2}'
```

4. **Verificar viabilidade:**
```bash
curl http://localhost:5000/projetos/1/viabilidade
```

---

## Estrutura das Classes

### Classe Desenvolvedor
- **Atributos:** id, nome, senioridade, pontos_por_dia, linguagem
- **Métodos:** cadastrar_desenvolvedor(), to_dict()

### Classe Projeto
- **Atributos:** id, descricao, prazo_em_dias, pontos_funcao, desenvolvedores
- **Métodos:**
  - `criar_projeto()`: Cria um novo projeto
  - `adicionar_desenvolvedor()`: Adiciona um desenvolvedor ao projeto
  - `calcular_capacidade_total()`: Calcula pontos totais que podem ser feitos
  - `verificar_viabilidade()`: Verifica se é possível completar o projeto no prazo
  - `to_dict()`: Serializa o projeto para JSON

---

## Requisitos Instalados

- Flask
- Python 3.14+

---

## Notas Importantes

- A API armazena dados em memória, portanto serão perdidos ao reiniciar o servidor
- IDs são gerados automaticamente
- Todos os campos são obrigatórios nas requisições POST
