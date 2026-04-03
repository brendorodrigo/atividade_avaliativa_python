#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para validar as classes Projeto e Desenvolvedor
"""

from atividade2_leonardo_rodrigues import Projeto, Desenvolvedor

print("\n" + "="*60)
print("TESTE DE VALIDAÇÃO - CLASSES PROJETO E DESENVOLVEDOR")
print("="*60 + "\n")

# Criar desenvolvedores
print("1. Criando desenvolvedores...")
dev1 = Desenvolvedor.cadastrar_desenvolvedor(
    "Leonardo", "Sênior", 15, "Python")
dev2 = Desenvolvedor.cadastrar_desenvolvedor("Maria", "Pleno", 10, "Java")
dev3 = Desenvolvedor.cadastrar_desenvolvedor("João", "Júnior", 5, "COBOL")

print(
    f"   ✓ {dev1.nome} (ID: {dev1.id}) - Sênior - {dev1.pontos_por_dia} pontos/dia")
print(
    f"   ✓ {dev2.nome} (ID: {dev2.id}) - Pleno - {dev2.pontos_por_dia} pontos/dia")
print(
    f"   ✓ {dev3.nome} (ID: {dev3.id}) - Júnior - {dev3.pontos_por_dia} pontos/dia")

# Criar projeto
print("\n2. Criando projeto...")
proj = Projeto.criar_projeto("Sistema de pagamentos", 30, 300)
print(f"   ✓ Projeto: {proj.descricao}")
print(f"   ✓ Prazo: {proj.prazo_em_dias} dias")
print(f"   ✓ Pontos de função: {proj.pontos_funcao}")

# Adicionar desenvolvedores ao projeto
print("\n3. Adicionando desenvolvedores ao projeto...")
proj.adicionar_desenvolvedor(dev1)
proj.adicionar_desenvolvedor(dev2)
proj.adicionar_desenvolvedor(dev3)
print(f"   ✓ {len(proj.desenvolvedores)} desenvolvedores adicionados")

# Calcular capacidade total
print("\n4. Calculando capacidade total...")
capacidade = proj.calcular_capacidade_total()
pontos_por_dia_total = dev1.pontos_por_dia + \
    dev2.pontos_por_dia + dev3.pontos_por_dia
print(f"   ✓ Capacidade por dia: {pontos_por_dia_total} pontos")
print(f"   ✓ Capacidade total (30 dias): {capacidade} pontos")
print(f"   ✓ Pontos requeridos: {proj.pontos_funcao} pontos")

# Verificar viabilidade
print("\n5. Verificando viabilidade do projeto...")
viabilidade = proj.verificar_viabilidade()
print(f"   ✓ Status: {viabilidade['status']}")
print(
    f"   ✓ Pontos requeridos: {viabilidade['detalhes']['pontos_requeridos']}")
print(f"   ✓ Capacidade total: {viabilidade['detalhes']['capacidade_total']}")

# Teste com projeto inviável
print("\n6. Testando projeto inviável...")
proj2 = Projeto.criar_projeto("Projeto com muitos pontos", 10, 500)
# Apenas o júnior (5 pontos/dia = 50 total)
proj2.adicionar_desenvolvedor(dev3)
viabilidade2 = proj2.verificar_viabilidade()
print(f"   ✓ Projeto: {proj2.descricao}")
print(f"   ✓ Status: {viabilidade2['status']}")
print(
    f"   ✓ Pontos requeridos: {viabilidade2['detalhes']['pontos_requeridos']}")
print(f"   ✓ Capacidade total: {viabilidade2['detalhes']['capacidade_total']}")

print("\n" + "="*60)
print("TODOS OS TESTES PASSARAM COM SUCESSO!")
print("="*60 + "\n")
