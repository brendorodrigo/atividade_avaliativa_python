class Projeto:
    def __init__ (self, ID, descricao, prazo, pontos):
        self.ID = ID
        self.descricao = descricao
        self.prazo = prazo
        self.pontos = pontos
        self.desenvolvedores = []
    
    @classmethod
    def cadastrar_projeto (cls, ID, descricao, prazo, pontos):
        projeto = cls(ID, descricao, prazo, pontos)
        return projeto

    def adicionar_desenvolvedor(self, dev):
        self.desenvolvedores.append(dev)
    
    def capacidade_total(self):
        capacidade_dia = sum(dev.pontos for dev in self.desenvolvedores)
        return capacidade_dia * self.prazo
    
    def verificar_viabilidade(self):
        capacidade = self.capacidade_total()

        if (capacidade >= self.pontos):
            print ("Projeto Viável")
        else:
            print ("Projeto Inviável")

class Desenvolvedor:
    def __init__(self, id, nome, senioridade, pontos, linguagem):
        self.id = id
        self.nome = nome
        self.senioridade = senioridade
        self.pontos = pontos
        self.linguagem = linguagem

    @classmethod
    def cadastrar_desenvolvedor (cls, id, nome, senioridade, pontos, linguagem):
        dev = cls(id, nome, senioridade, pontos, linguagem)
        return dev

dev1 = Desenvolvedor.cadastrar_desenvolvedor(1, "João", "Pleno", 5, "Python")
dev2 = Desenvolvedor.cadastrar_desenvolvedor(2, "Eva", "Sênior", 8, "Java")
projeto = Projeto.cadastrar_projeto(1, "Sistema de Biblioteca", 10, 100)
projeto.adicionar_desenvolvedor(dev1)
projeto.adicionar_desenvolvedor(dev2)
projeto.verificar_viabilidade()
