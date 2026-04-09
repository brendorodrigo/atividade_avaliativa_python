import requests
import json

# URL base da API
BASE_URL = "http://localhost:8000"

def pretty_print(title, data):
    """Imprime JSON de forma formatada"""
    print(f"\n{'='*60}")
    print(f"► {title}")
    print(f"{'='*60}")
    print(json.dumps(data, indent=2, ensure_ascii=False))

def testar_desenvolvedores():
    """Testa os endpoints de desenvolvedores"""
    print("\n\n" + "█"*60)
    print("█ TESTANDO ENDPOINTS DE DESENVOLVEDORES")
    print("█"*60)
    
    # Criar desenvolvedores
    devs_data = [
        {
            "nome": "João Silva",
            "senioridade": "Pleno",
            "pontos_por_dia": 5,
            "linguagem": "Python"
        },
        {
            "nome": "Maria Santos",
            "senioridade": "Senior",
            "pontos_por_dia": 8,
            "linguagem": "Python"
        },
        {
            "nome": "Pedro Costa",
            "senioridade": "Junior",
            "pontos_por_dia": 2,
            "linguagem": "JavaScript"
        }
    ]
    
    dev_ids = []
    
    for dev in devs_data:
        response = requests.post(f"{BASE_URL}/desenvolvedores", json=dev)
        pretty_print(f"POST /desenvolvedores", response.json())
        dev_ids.append(response.json()["id"])
    
    # Listar desenvolvedores
    response = requests.get(f"{BASE_URL}/desenvolvedores")
    pretty_print("GET /desenvolvedores", response.json())
    
    # Obter desenvolvedor específico
    response = requests.get(f"{BASE_URL}/desenvolvedores/{dev_ids[0]}")
    pretty_print(f"GET /desenvolvedores/{dev_ids[0]}", response.json())
    
    return dev_ids


def testar_projetos(dev_ids):
    """Testa os endpoints de projetos"""
    print("\n\n" + "█"*60)
    print("█ TESTANDO ENDPOINTS DE PROJETOS")
    print("█"*60)
    
    # Criar projetos
    projetos_data = [
        {
            "descricao": "Sistema de pagamentos",
            "prazo_dias": 30,
            "pontos_funcao": 200
        },
        {
            "descricao": "App mobile",
            "prazo_dias": 45,
            "pontos_funcao": 300
        },
        {
            "descricao": "Dashboard Analytics",
            "prazo_dias": 20,
            "pontos_funcao": 100
        }
    ]
    
    projeto_ids = []
    
    for proj in projetos_data:
        response = requests.post(f"{BASE_URL}/projetos", json=proj)
        pretty_print(f"POST /projetos", response.json())
        projeto_ids.append(response.json()["id"])
    
    # Listar projetos
    response = requests.get(f"{BASE_URL}/projetos")
    pretty_print("GET /projetos", response.json())
    
    # Obter projeto específico
    response = requests.get(f"{BASE_URL}/projetos/{projeto_ids[0]}")
    pretty_print(f"GET /projetos/{projeto_ids[0]}", response.json())
    
    return projeto_ids


def testar_alocacao(dev_ids, projeto_ids):
    """Testa alocação de desenvolvedores aos projetos"""
    print("\n\n" + "█"*60)
    print("█ TESTANDO ALOCAÇÃO DE DESENVOLVEDORES")
    print("█"*60)
    
    # Alocar desenvolvedores ao primeiro projeto
    for dev_id in dev_ids[:2]:  # Aloca 2 desenvolvedores
        response = requests.post(
            f"{BASE_URL}/projetos/{projeto_ids[0]}/desenvolvedores",
            json={"desenvolvedor_id": dev_id}
        )
        pretty_print(
            f"POST /projetos/{projeto_ids[0]}/desenvolvedores (dev_id={dev_id})",
            response.json()
        )
    
    # Obter desenvolvedores do projeto
    response = requests.get(f"{BASE_URL}/projetos/{projeto_ids[0]}/desenvolvedores")
    pretty_print(
        f"GET /projetos/{projeto_ids[0]}/desenvolvedores",
        response.json()
    )


def testar_viabilidade(projeto_ids):
    """Testa verificação de viabilidade dos projetos"""
    print("\n\n" + "█"*60)
    print("█ TESTANDO VIABILIDADE DOS PROJETOS")
    print("█"*60)
    
    for proj_id in projeto_ids:
        response = requests.get(f"{BASE_URL}/projetos/{proj_id}/viabilidade")
        resultado = response.json()
        
        if resultado["viavel"]:
            status_emoji = "✓ VIÁVEL"
        else:
            status_emoji = "✗ INVIÁVEL"
        
        pretty_print(f"{status_emoji} - Projeto {proj_id}", resultado)


def testar_health():
    """Testa o endpoint de saúde"""
    print("\n\n" + "█"*60)
    print("█ TESTANDO HEALTH CHECK")
    print("█"*60)
    
    response = requests.get(f"{BASE_URL}/health")
    pretty_print("GET /health", response.json())


def main():
    """Executa todos os testes"""
    try:
        print("\n\n")
        print("╔" + "═"*58 + "╗")
        print("║" + " "*58 + "║")
        print("║" + "  TESTE COMPLETO DA API".center(58) + "║")
        print("║" + "  Projeto e Desenvolvimento".center(58) + "║")
        print("║" + " "*58 + "║")
        print("╚" + "═"*58 + "╝")
        
        # Testar health
        testar_health()
        
        # Testar desenvolvedores
        dev_ids = testar_desenvolvedores()
        
        # Testar projetos
        projeto_ids = testar_projetos(dev_ids)
        
        # Testar alocação
        testar_alocacao(dev_ids, projeto_ids)
        
        # Testar viabilidade
        testar_viabilidade(projeto_ids)
        
        print("\n\n" + "═"*60)
        print("✓ TODOS OS TESTES COMPLETADOS COM SUCESSO!")
        print("═"*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não conseguiu conectar à API.")
        print("Certifique-se de que a API está rodando em http://localhost:8000")
        print("Execute: python main.py\n")
    except Exception as e:
        print(f"\n❌ ERRO: {e}\n")


if __name__ == "__main__":
    main()
