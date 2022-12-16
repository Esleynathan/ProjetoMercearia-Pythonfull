from models import *
from DAO import *
from datetime import datetime

class ControllerCategoria:
    def cadastraCategoria(self, novaCategoria):
        existe = False
        x = DaoCategoria.ler()
        for i in x:
            if i.categoria == novaCategoria:
                existe = True
        if not existe:
            DaoCategoria.salvar(novaCategoria)
            print("Categoria cadastrada com sucesso.")
        else:
            print("A Categoria que deseja cadastrar já existe.")
            
a = ControllerCategoria()
a.cadastraCategoria('Frios')

class ControllerPessoa:
    pass

class ControllerProduto:
    pass

class ControllerEstoque:
    pass