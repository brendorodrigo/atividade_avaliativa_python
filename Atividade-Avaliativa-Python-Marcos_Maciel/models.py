from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class Desenvolvedor(BaseModel):
    id: Optional[int] = None
    nome: str
    senioridade: str  # Junior, Pleno, Senior
    pontos_por_dia: float
    linguagem: str

    def cadastrar_desenvolvedor(self):
        """Registra o desenvolvedor no sistema"""
        return {
            "status": "Desenvolvedor cadastrado com sucesso",
            "desenvolvedor": self.dict()
        }


class Projeto(BaseModel):
    id: Optional[int] = None
    descricao: str
    prazo_dias: int
    pontos_funcao: int
    desenvolvedores: List[int] = []  # Lista de IDs dos desenvolvedores

    def criar_projeto(self):
        """Cria um novo projeto"""
        return {
            "status": "Projeto criado com sucesso",
            "projeto": self.dict()
        }

    def adicionar_desenvolvedor(self, desenvolvedor_id: int):
        """Adiciona um desenvolvedor ao projeto"""
        if desenvolvedor_id not in self.desenvolvedores:
            self.desenvolvedores.append(desenvolvedor_id)
            return {
                "status": "Desenvolvedor adicionado com sucesso",
                "desenvolvedor_id": desenvolvedor_id,
                "projeto_id": self.id
            }
        return {
            "status": "Desenvolvedor já está no projeto",
            "desenvolvedor_id": desenvolvedor_id
        }

    def calcular_capacidade_total(self, desenvolvedores_list: List[Desenvolvedor]) -> float:
        """Calcula a capacidade total de pontos que podem ser entregues no prazo"""
        capacidade = 0
        for dev_id in self.desenvolvedores:
            # Encontra o desenvolvedor na lista
            dev = next((d for d in desenvolvedores_list if d.id == dev_id), None)
            if dev:
                capacidade += dev.pontos_por_dia * self.prazo_dias
        return capacidade

    def verificar_viabilidade(self, desenvolvedores_list: List[Desenvolvedor]) -> dict:
        """
        Verifica se o projeto é viável com os desenvolvedores alocados
        Retorna status do projeto (viável ou inviável)
        """
        if not self.desenvolvedores:
            return {
                "projeto_id": self.id,
                "viavel": False,
                "motivo": "Nenhum desenvolvedor alocado ao projeto",
                "capacidade_total": 0,
                "pontos_necessarios": self.pontos_funcao,
                "deficit": self.pontos_funcao
            }

        capacidade_total = self.calcular_capacidade_total(desenvolvedores_list)
        viavel = capacidade_total >= self.pontos_funcao

        return {
            "projeto_id": self.id,
            "descricao": self.descricao,
            "viavel": viavel,
            "motivo": "Projeto viável" if viavel else "Projeto inviável - capacidade insuficiente",
            "capacidade_total": capacidade_total,
            "pontos_necessarios": self.pontos_funcao,
            "deficit": max(0, self.pontos_funcao - capacidade_total),
            "prazo_dias": self.prazo_dias,
            "desenvolvedores_alocados": len(self.desenvolvedores)
        }
