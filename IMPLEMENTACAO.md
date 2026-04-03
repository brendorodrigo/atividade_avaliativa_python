# Atividade Avaliativa - NPC I
## Sistema de Gestão de Projetos e Desenvolvedores com API Flask

### 📋 Descrição da Atividade

Implementação completa de um sistema de gestão de projetos e desenvolvedores com as seguintes funcionalidades:

1. **Classe Desenvolvedor** com atributos (ID, Nome, Senioridade, Pontos por dia, Linguagem)
2. **Classe Projeto** com atributos (ID, Descrição, Prazo em dias, Pontos de função, Desenvolvedores)
3. **Métodos para gerenciamento**:
   - Cadastrar desenvolvedores
   - Criar projetos
   - Adicionar desenvolvedores aos projetos
   - Calcular capacidade total de trabalho
   - Verificar viabilidade de projetos

4. **API REST com Flask** com os seguintes endpoints:
   - CRUD de desenvolvedores
   - CRUD de projetos
   - Gerenciamento de desenvolvedores por projeto
   - Verificação de viabilidade

---

### 🚀 Como Usar

#### 1. Instalar Dependências

```bash
pip install flask requests
```

#### 2. Executar a API

```bash
python atividade2_leonardo_rodrigues.py
```

O servidor iniciará em `http://localhost:5000`

#### 3. Testar a Implementação

**Teste das Classes:**
```bash
python test_validacao.py
```

**Teste da API:**
```bash
# Em outro terminal, enquanto o servidor está rodando:
python test_api.py
```

---

### 📁 Estrutura dos Arquivos

```
atividade_avaliativa_python/
├── atividade1_leonardo_rodrigues.py     # Atividade 1: Validação de alunos
├── atividade2_leonardo_rodrigues.py     # Atividade 2: Classes + API Flask
├── test_validacao.py                     # Teste de validação das classes
├── test_api.py                           # Teste completo da API
├── API_EXEMPLOS.md                       # Exemplos de requisições cURL
├── IMPLEMENTACAO.md                      # Este arquivo
└── README.md                             # Arquivo original da atividade
```

---

### 🔌 Endpoints da API

#### Desenvolvedores

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/desenvolvedores` | Criar novo desenvolvedor |
| GET | `/desenvolvedores` | Listar todos os desenvolvedores |
| GET | `/desenvolvedores/{id}` | Obter desenvolvedor específico |

**Exemplo POST:**
```json
{
  "nome": "João",
  "senioridade": "Pleno",
  "pontos_por_dia": 5,
  "linguagem": "Python"
}
```

#### Projetos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/projetos` | Criar novo projeto |
| GET | `/projetos` | Listar todos os projetos |
| GET | `/projetos/{id}` | Obter projeto específico |
| POST | `/projetos/{id}/desenvolvedores` | Adicionar desenvolvedor ao projeto |
| GET | `/projetos/{id}/desenvolvedores` | Listar desenvolvedores do projeto |
| GET | `/projetos/{id}/viabilidade` | Verificar viabilidade do projeto |

**Exemplo POST Projeto:**
```json
{
  "descricao": "Sistema de pagamentos",
  "prazo_dias": 30,
  "pontos_funcao": 200
}
```

**Exemplo POST Adicionar Desenvolvedor:**
```json
{
  "desenvolvedor_id": 1
}
```

---

### 🧪 Exemplo de Uso Completo

```python
from atividade2_leonardo_rodrigues import Projeto, Desenvolvedor

# 1. Criar desenvolvedores
dev1 = Desenvolvedor.cadastrar_desenvolvedor("Leonardo", "Sênior", 15, "Python")
dev2 = Desenvolvedor.cadastrar_desenvolvedor("Maria", "Pleno", 10, "Java")
dev3 = Desenvolvedor.cadastrar_desenvolvedor("João", "Júnior", 5, "COBOL")

# 2. Criar projeto
projeto = Projeto.criar_projeto("Sistema de pagamentos", 30, 300)

# 3. Adicionar desenvolvedores
projeto.adicionar_desenvolvedor(dev1)
projeto.adicionar_desenvolvedor(dev2)
projeto.adicionar_desenvolvedor(dev3)

# 4. Calcular capacidade
capacidade = projeto.calcular_capacidade_total()  # 900 pontos (30 dias * 30 pontos/dia)

# 5. Verificar viabilidade
resultado = projeto.verificar_viabilidade()
# Resultado: {"status": "Projeto viável", "detalhes": {...}}
```

---

### 📊 Lógica de Viabilidade de Projeto

Um projeto é viável quando:
$$\text{Capacidade Total} \geq \text{Pontos de Função}$$

Onde:
$$\text{Capacidade Total} = \sum \text{(Pontos por dia de cada dev)} \times \text{Prazo em dias}$$

**Exemplo:**
- Desenvolvedores: Leonardo (15) + Maria (10) + João (5) = 30 pontos/dia
- Prazo: 30 dias
- Capacidade Total: 30 × 30 = 900 pontos
- Pontos requeridos: 300 pontos
- **Resultado: Viável** ✅

---

### 🛠️ Tecnologias Utilizadas

- **Python 3.14+**
- **Flask** - Framework web para criar a API REST
- **Requests** - Biblioteca para testar requisições HTTP

---

### ✅ Requisitos Atendidos

- [x] Classe Desenvolvedor com todos os atributos
- [x] Classe Projeto com todos os atributos
- [x] Método cadastrar_desenvolvedor
- [x] Método criar_projeto
- [x] Método adicionar_desenvolvedor
- [x] Método calcular_capacidade_total
- [x] Método verificar_viabilidade
- [x] API POST /desenvolvedores
- [x] API GET /desenvolvedores
- [x] API GET /desenvolvedores/{id}
- [x] API POST /projetos
- [x] API POST /projetos/{id}/desenvolvedores
- [x] API GET /projetos
- [x] API GET /projetos/{id}
- [x] API GET /projetos/{id}/desenvolvedores
- [x] API GET /projetos/{id}/viabilidade
- [x] Instalação de dependências (Flask e Requests)

---

### 📝 Notas Importantes

1. A API armazena dados em **memória RAM**, portanto os dados serão perdidos ao reiniciar
2. IDs são gerados automaticamente de forma sequencial
3. Todos os campos são obrigatórios nas requisições POST
4. A validação de viabilidade considera: capacidade_total >= pontos_funcao
5. Senioridade esperada: "Sênior", "Pleno", "Júnior"

---

### 🐛 Tratamento de Erros

A API retorna mensagens de erro apropriadas:

| Status | Situação |
|--------|----------|
| 201 | Criação bem-sucedida |
| 200 | Sucesso |
| 400 | Faltam campos obrigatórios |
| 404 | Recurso não encontrado |

---

### 📧 Autor

Leonardo Rodrigues - CCP - CIESA

---

### 📚 Referências

- README.md - Especificações da atividade
- atividade1_leonardo_rodrigues.py - Atividade 1 (Validação de alunos)
- API_EXEMPLOS.md - Exemplos de requisições cURL
