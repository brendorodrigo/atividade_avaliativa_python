1.Classes e Objetos em Python (3,5 pontos)
Crie uma classe chamada Livro com as seguintes características:
Requisitos:
Atributos:
titulo
autor
quantidade
Métodos:
exibir_dados() → exibe todas as informações do livro
disponibilidade() → retorna "Disponível" se quantidade > 0, senão "Indisponível"
O programa deve:
Criar dois objetos da classe Livro
Exibir os dados dos livros
Mostrar a disponibilidade de cada livro
Exemplo de saída esperada:
Livro: Python Básico
Autor: Ana Silva
Quantidade: 3
Status: Disponível

Livro: Estruturas de Dados
Autor: Carlos Souza
Quantidade: 0
Status: Indisponível











2. Flask + HTTP + POO  (3,5 pontos)
Crie uma aplicação Flask que representa uma API simples de produtos.
Requisitos:
Criar uma classe chamada Produto com os atributos:
nome
preco
estoque

Criar um método:
disponivel() → retorna "Em estoque" se estoque > 0, senão "Esgotado"

Criar uma aplicação Flask com uma rota (ex: /produto)
A rota deve:
Criar um objeto Produto
Retornar os dados em formato JSON
Exibir nome, preço e situação do produto

Exemplo de retorno esperado (HTTP Response):
{
  "nome": "Notebook",
  "preco": 3500,
  "estoque": 2,
  "situacao": "Em estoque"
}
