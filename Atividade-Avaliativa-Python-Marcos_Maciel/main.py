from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models import Desenvolvedor, Projeto

app = FastAPI(
    title="API de Gerenciamento de Projetos e Desenvolvedores",
    description="API para gerenciar projetos e desenvolvedores com análise de viabilidade",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulando um banco de dados em memória
desenvolvedores_db: dict = {}
projetos_db: dict = {}
desenvolvedor_id_counter = 1
projeto_id_counter = 1


# ==================== ENDPOINTS DE DESENVOLVEDORES ====================

@app.post("/desenvolvedores", response_model=Desenvolvedor, status_code=status.HTTP_201_CREATED)
def criar_desenvolvedor(desenvolvedor: Desenvolvedor):
    """
    Cria um novo desenvolvedor.
    
    Body esperado:
    ```json
    {
        "nome": "João",
        "senioridade": "Pleno",
        "pontos_por_dia": 5,
        "linguagem": "Python"
    }
    ```
    """
    global desenvolvedor_id_counter
    desenvolvedor.id = desenvolvedor_id_counter
    desenvolvedores_db[desenvolvedor_id_counter] = desenvolvedor
    desenvolvedor_id_counter += 1
    
    return desenvolvedor


@app.get("/desenvolvedores", response_model=List[Desenvolvedor])
def listar_desenvolvedores():
    """
    Lista todos os desenvolvedores cadastrados.
    
    Retorna uma lista com todos os desenvolvedores do sistema.
    """
    return list(desenvolvedores_db.values())


@app.get("/desenvolvedores/{desenvolvedor_id}", response_model=Desenvolvedor)
def obter_desenvolvedor(desenvolvedor_id: int):
    """
    Obtém um desenvolvedor específico pelo ID.
    
    Retorna os detalhes do desenvolvedor solicitado ou erro 404 se não encontrado.
    """
    if desenvolvedor_id not in desenvolvedores_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Desenvolvedor com ID {desenvolvedor_id} não encontrado"
        )
    
    return desenvolvedores_db[desenvolvedor_id]


# ==================== ENDPOINTS DE PROJETOS ====================

@app.post("/projetos", response_model=Projeto, status_code=status.HTTP_201_CREATED)
def criar_projeto(projeto: Projeto):
    """
    Cria um novo projeto.
    
    Body esperado:
    ```json
    {
        "descricao": "Sistema de pagamentos",
        "prazo_dias": 30,
        "pontos_funcao": 200
    }
    ```
    """
    global projeto_id_counter
    projeto.id = projeto_id_counter
    projetos_db[projeto_id_counter] = projeto
    projeto_id_counter += 1
    
    return projeto


@app.post("/projetos/{projeto_id}/desenvolvedores", response_model=dict, status_code=status.HTTP_200_OK)
def adicionar_desenvolvedor_ao_projeto(projeto_id: int, body: dict):
    """
    Adiciona um desenvolvedor a um projeto.
    
    Body esperado:
    ```json
    {
        "desenvolvedor_id": 1
    }
    ```
    """
    if projeto_id not in projetos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projeto com ID {projeto_id} não encontrado"
        )
    
    desenvolvedor_id = body.get("desenvolvedor_id")
    
    if desenvolvedor_id not in desenvolvedores_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Desenvolvedor com ID {desenvolvedor_id} não encontrado"
        )
    
    projeto = projetos_db[projeto_id]
    
    if desenvolvedor_id in projeto.desenvolvedores:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este desenvolvedor já está alocado ao projeto"
        )
    
    projeto.desenvolvedores.append(desenvolvedor_id)
    
    return {
        "status": "Desenvolvedor adicionado com sucesso",
        "projeto_id": projeto_id,
        "desenvolvedor_id": desenvolvedor_id,
        "total_desenvolvedores": len(projeto.desenvolvedores)
    }


@app.get("/projetos", response_model=List[Projeto])
def listar_projetos():
    """
    Lista todos os projetos cadastrados.
    
    Retorna uma lista com todos os projetos do sistema.
    """
    return list(projetos_db.values())


@app.get("/projetos/{projeto_id}", response_model=Projeto)
def obter_projeto(projeto_id: int):
    """
    Obtém um projeto específico pelo ID.
    
    Retorna os detalhes do projeto solicitado ou erro 404 se não encontrado.
    """
    if projeto_id not in projetos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projeto com ID {projeto_id} não encontrado"
        )
    
    return projetos_db[projeto_id]


@app.get("/projetos/{projeto_id}/desenvolvedores", response_model=List[Desenvolvedor])
def obter_desenvolvedores_do_projeto(projeto_id: int):
    """
    Obtém todos os desenvolvedores alocados a um projeto específico.
    
    Retorna uma lista com todos os desenvolvedores do projeto ou erro 404.
    """
    if projeto_id not in projetos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projeto com ID {projeto_id} não encontrado"
        )
    
    projeto = projetos_db[projeto_id]
    desenvolvedores = [
        desenvolvedores_db[dev_id] 
        for dev_id in projeto.desenvolvedores 
        if dev_id in desenvolvedores_db
    ]
    
    return desenvolvedores


@app.get("/projetos/{projeto_id}/viabilidade", response_model=dict)
def verificar_viabilidade_projeto(projeto_id: int):
    """
    Verifica a viabilidade do projeto.
    
    Analisa se os desenvolvedores alocados têm capacidade suficiente 
    para entregar a quantidade de pontos de função no prazo.
    
    Retorna:
    - viavel: boolean indicando se o projeto é viável
    - motivo: descrição da análise
    - capacidade_total: pontos que podem ser entregues
    - pontos_necessarios: pontos do projeto
    - deficit: pontos faltando (se inviável)
    """
    if projeto_id not in projetos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projeto com ID {projeto_id} não encontrado"
        )
    
    projeto = projetos_db[projeto_id]
    resultado = projeto.verificar_viabilidade(list(desenvolvedores_db.values()))
    
    return resultado


# ==================== ENDPOINT DE SAÚDE ====================

@app.get("/health", response_model=dict)
def health_check():
    """
    Verifica o status da API.
    """
    return {
        "status": "API rodando normalmente",
        "total_desenvolvedores": len(desenvolvedores_db),
        "total_projetos": len(projetos_db)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
