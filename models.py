class Pessoa():
    def __init__(self):
        
    @classmethod
    def cliente(cls, nome, id_cliente):
        id_cliente = id_cliente
        
    @classmethod
    def funcionario(cls, id_funcionario):
        id_funcionario = id_funcionario
        
class Categoria():
    def __init__(self, categoria):
        self.categoria = categoria

class Produto():
    def __init__(self, nome, preco, categoria):
        self.nome = nome
        self.preco = preco
        self.categoria = categoria

class Estoque():
    def __init__(self, produto: Produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade