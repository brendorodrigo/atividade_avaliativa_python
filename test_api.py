#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste da API Flask
Testa todos os endpoints da API de Projetos e Desenvolvedores
"""

import requests
import json
import time
import subprocess
import sys
from threading import Thread

BASE_URL = "http://localhost:5000"


def testar_api():
    """Testa todos os endpoints da API"""

    print("\n" + "="*70)
    print("TESTE COMPLETO DA API - PROJETOS E DESENVOLVEDORES")
    print("="*70 + "\n")

    # Aguardar o servidor iniciar
    print("⏳ Aguardando servidor iniciar...")
    time.sleep(3)

    try:
        # Teste 1: Home
        print("\n[TEST 1] GET / - Raiz da API")
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(
            f"Resposta:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")

        # Teste 2: Criar desenvolvedores
        print("[TEST 2] POST /desenvolvedores - Criando developed ores")

        dev_data_1 = {
            "nome": "Leonardo",
            "senioridade": "Sênior",
            "pontos_por_dia": 15,
            "linguagem": "Python"
        }
        response = requests.post(
            f"{BASE_URL}/desenvolvedores", json=dev_data_1)
        print(f"Status: {response.status_code}")
        dev1 = response.json()
        print(
            f"Desenvolvedor 1 criado: {json.dumps(dev1, indent=2, ensure_ascii=False)}")

        dev_data_2 = {
            "nome": "Maria",
            "senioridade": "Pleno",
            "pontos_por_dia": 10,
            "linguagem": "Java"
        }
        response = requests.post(
            f"{BASE_URL}/desenvolvedores", json=dev_data_2)
        dev2 = response.json()
        print(f"Desenvolvedor 2 criado: {dev2['nome']} (ID: {dev2['id']})")

        dev_data_3 = {
            "nome": "João",
            "senioridade": "Júnior",
            "pontos_por_dia": 5,
            "linguagem": "COBOL"
        }
        response = requests.post(
            f"{BASE_URL}/desenvolvedores", json=dev_data_3)
        dev3 = response.json()
        print(f"Desenvolvedor 3 criado: {dev3['nome']} (ID: {dev3['id']})\n")

        # Teste 3: Listar desenvolvedores
        print("[TEST 3] GET /desenvolvedores - Listando todos os desenvolvedores")
        response = requests.get(f"{BASE_URL}/desenvolvedores")
        print(f"Status: {response.status_code}")
        devs = response.json()
        print(f"Total de desenvolvedores: {len(devs)}")
        for dev in devs:
            print(
                f"  - {dev['nome']} ({dev['senioridade']}): {dev['pontos_por_dia']} pontos/dia\n")

        # Teste 4: Obter desenvolvedor específico
        print(
            f"[TEST 4] GET /desenvolvedores/{{id}} - Obtendo desenvolvedor ID 1")
        response = requests.get(f"{BASE_URL}/desenvolvedores/1")
        print(f"Status: {response.status_code}")
        print(
            f"Desenvolvedor:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")

        # Teste 5: Criar projetos
        print("[TEST 5] POST /projetos - Criando projetos")

        proj_data_1 = {
            "descricao": "Sistema de pagamentos",
            "prazo_dias": 30,
            "pontos_funcao": 300
        }
        response = requests.post(f"{BASE_URL}/projetos", json=proj_data_1)
        print(f"Status: {response.status_code}")
        proj1 = response.json()
        print(
            f"Projeto 1 criado: {json.dumps(proj1, indent=2, ensure_ascii=False)}\n")

        proj_data_2 = {
            "descricao": "App Mobile",
            "prazo_dias": 45,
            "pontos_funcao": 500
        }
        response = requests.post(f"{BASE_URL}/projetos", json=proj_data_2)
        proj2 = response.json()
        print(f"Projeto 2 criado: {proj2['descricao']} (ID: {proj2['id']})\n")

        # Teste 6: Listar projetos
        print("[TEST 6] GET /projetos - Listando todos os projetos")
        response = requests.get(f"{BASE_URL}/projetos")
        print(f"Status: {response.status_code}")
        projs = response.json()
        print(f"Total de projetos: {len(projs)}\n")

        # Teste 7: Obter projeto específico
        print(f"[TEST 7] GET /projetos/{{id}} - Obtendo projeto ID 1")
        response = requests.get(f"{BASE_URL}/projetos/1")
        print(f"Status: {response.status_code}")
        print(
            f"Projeto:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")

        # Teste 8: Adicionar desenvolvedores ao projeto
        print(
            "[TEST 8] POST /projetos/{id}/desenvolvedores - Adicionando desenvolvedores")

        add_dev = {"desenvolvedor_id": dev1['id']}
        response = requests.post(
            f"{BASE_URL}/projetos/1/desenvolvedores", json=add_dev)
        print(f"Status: {response.status_code}")
        print(f"Desenvolvedor 1 adicionado ao projeto 1")

        add_dev = {"desenvolvedor_id": dev2['id']}
        response = requests.post(
            f"{BASE_URL}/projetos/1/desenvolvedores", json=add_dev)
        print(f"Desenvolvedor 2 adicionado ao projeto 1")

        add_dev = {"desenvolvedor_id": dev3['id']}
        response = requests.post(
            f"{BASE_URL}/projetos/1/desenvolvedores", json=add_dev)
        print(f"Desenvolvedor 3 adicionado ao projeto 1\n")

        # Teste 9: Listar desenvolvedores de um projeto
        print(
            "[TEST 9] GET /projetos/{id}/desenvolvedores - Listando desenvolvedores do projeto")
        response = requests.get(f"{BASE_URL}/projetos/1/desenvolvedores")
        print(f"Status: {response.status_code}")
        devs_proj = response.json()
        print(f"Desenvolvedores no projeto 1: {len(devs_proj)}")
        for dev in devs_proj:
            print(f"  - {dev['nome']} ({dev['senioridade']})\n")

        # Teste 10: Verificar viabilidade
        print(
            "[TEST 10] GET /projetos/{id}/viabilidade - Verificando viabilidade")
        response = requests.get(f"{BASE_URL}/projetos/1/viabilidade")
        print(f"Status: {response.status_code}")
        viabilidade = response.json()
        print(
            f"Resultado:\n{json.dumps(viabilidade, indent=2, ensure_ascii=False)}\n")

        # Teste 11: Adicionar apenas um desenvolvedor ao projeto 2
        print("[TEST 11] Teste com projeto inviável")
        # Apenas júnior (5 pontos/dia)
        add_dev = {"desenvolvedor_id": dev3['id']}
        response = requests.post(
            f"{BASE_URL}/projetos/2/desenvolvedores", json=add_dev)
        print(f"Desenvolvedor 3 adicionado ao projeto 2 (inviável)")

        response = requests.get(f"{BASE_URL}/projetos/2/viabilidade")
        viabilidade2 = response.json()
        print(
            f"Resultado:\n{json.dumps(viabilidade2, indent=2, ensure_ascii=False)}\n")

        # Resumo
        print("="*70)
        print("✅ TODOS OS TESTES FORAM EXECUTADOS COM SUCESSO!")
        print("="*70 + "\n")

    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor Flask")
        print("Certifique-se de que o servidor está rodando na porta 5000")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    testar_api()
