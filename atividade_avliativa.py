from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Desenvolvedor:
    def __init__(self, id, nome, senioridade, pontos_por_dia, linguagem):
        self.id = id
        self.nome = nome
        self.senioridade = senioridade
        self.pontos_por_dia = pontos_por_dia
        self.linguagem = linguagem

class Projeto:
    def __init__(self, id, descricao, prazo_dias, pontos_funcao):
        self.id = id
        self.descricao = descricao
        self.prazo_dias = prazo_dias
        self.pontos_funcao = pontos_funcao
        self.desenvolvedores: List[Desenvolvedor] = []

    def adicionar_desenvolvedor(self, dev: Desenvolvedor):
        self.desenvolvedores.append(dev)

    def calcular_capacidade_total(self):
        # Soma dos pontos por dia de todos os devs * prazo do projeto
        soma_pontos_dia = sum(dev.pontos_por_dia for dev in self.desenvolvedores)
        return soma_pontos_dia * self.prazo_dias

    def verificar_viabilidade(self):
        capacidade = self.calcular_capacidade_total()
        if capacidade >= self.pontos_funcao:
            return {
                "viável": True,
                "mensagem": f"Projeto viável. Capacidade total ({capacidade}) atende a demanda ({self.pontos_funcao})."
            }
        else:
            return {
                "viável": False,
                "mensagem": f"Projeto inviável. Capacidade total ({capacidade}) é inferior aos pontos necessários ({self.pontos_funcao})."
            }


db_desenvolvedores = []
db_projetos = []

class DevCreate(BaseModel):
    nome: str
    senioridade: str
    pontos_por_dia: int
    linguagem: str

class ProjetoCreate(BaseModel):
    descricao: str
    prazo_dias: int
    pontos_funcao: int

class AddDevToProject(BaseModel):
    desenvolvedor_id: int



@app.post("/desenvolvedores", status_code=201)
def cadastrar_desenvolvedor(dev: DevCreate):
    novo_id = len(db_desenvolvedores) + 1
    novo_dev = Desenvolvedor(novo_id, **dev.dict())
    db_desenvolvedores.append(novo_dev)
    return novo_dev

@app.get("/desenvolvedores")
def listar_desenvolvedores():
    return db_desenvolvedores

@app.get("/desenvolvedores/{id}")
def obter_desenvolvedor(id: int):
    dev = next((d for d in db_desenvolvedores if d.id == id), None)
    if not dev:
        raise HTTPException(status_code=404, detail="Desenvolvedor não encontrado")
    return dev



@app.post("/projetos", status_code=201)
def criar_projeto(proj: ProjetoCreate):
    novo_id = len(db_projetos) + 1
    novo_projeto = Projeto(novo_id, **proj.dict())
    db_projetos.append(novo_projeto)
    return novo_projeto

@app.get("/projetos")
def listar_projetos():
    return db_projetos

@app.get("/projetos/{id}")
def obter_projeto(id: int):
    projeto = next((p for p in db_projetos if p.id == id), None)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return projeto

@app.post("/projetos/{id}/desenvolvedores")
def vincular_desenvolvedor(id: int, payload: AddDevToProject):
    projeto = next((p for p in db_projetos if p.id == id), None)
    dev = next((d for d in db_desenvolvedores if d.id == payload.desenvolvedor_id), None)
    
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    if not dev:
        raise HTTPException(status_code=404, detail="Desenvolvedor não encontrado")
    
    projeto.adicionar_desenvolvedor(dev)
    return {"message": f"Desenvolvedor {dev.nome} adicionado ao projeto {projeto.descricao}"}

@app.get("/projetos/{id}/desenvolvedores")
def listar_devs_do_projeto(id: int):
    projeto = next((p for p in db_projetos if p.id == id), None)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return projeto.desenvolvedores

@app.get("/projetos/{id}/viabilidade")
def checar_viabilidade(id: int):
    projeto = next((p for p in db_projetos if p.id == id), None)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return projeto.verificar_viabilidade()
