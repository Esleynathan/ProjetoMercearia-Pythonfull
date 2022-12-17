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

    def removerCategoria(self, categoriaRemover):
        x = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == categoriaRemover, x))

        if len(cat) <= 0:
            print("A categoria que deseja remover não existe.")
        else:
            for i in range(len(x)):
                if x[i].categoria == categoriaRemover:
                    del x[i]
                    break
            print("Categoria removida com sucesso.")
            #TO DO: COLOCAR SEM CATEGORIA NO ESTOQUE - QUANDO REMOVER CATEGORIA COLOCAR SEM CATEGORIA NOS PRODUTOS QUE TEM AQUELA CATEGORIA
            with open('categoria.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines("\n")

    def alterarCategoria(self, categoriaAlterar, categoriaAlterada):
        x = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == categoriaAlterar, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda x: x.categoria == categoriaAlterada, x))
            if len(cat1) == 0:
                x = list(map(lambda x: Categoria(categoriaAlterada) if (x.categoria == categoriaAlterar) else(x),x ))
                print("A categoria foi alterada com sucesso.")
 #TO DO: ALTERAR CATEGORIA TAMBEM DO ESTOQUE
            else:
                print("A categoria para qual deseja alterar já existe.")
        else:
            print("A categoria que deseja alterar não existe.")

        with open ('categoria.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')

    def mostrarCategoria(self):
        categorias = DaoCategoria.ler()
        if len (categorias) == 0:
            print("Categoria vazia.")
            return 0
        for i in categorias:
                print(f'Categoaria: {i.categoria}')

class ControllerEstoque:
    def cadastrarProduto(self, nome, preco, categoria, quantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()

        h = list(filter(lambda x: x.categoria == categoria, y))
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len(h) > 0:
            if len(est) == 0:
                produto = Produtos(nome, preco, categoria)
                DaoEstoque.salvar(produto, quantidade)
                print("Produto cadastrado com sucesso")
            else:
                print("O Produto já existe em estoque")
        else:
            print('Categoria inexistente.')

    def removerProduto(self, nome):
        x = DaoEstoque.ler()
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len (est) > 0:
            for i in range(len(x)):
                if x[i].produto.nome == nome:
                    del x[i]
                    break
                    print("O produto removido ccom sucesso.")
        else:
            print("O produto que deseja remover não existe")
    
        with open ('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + 
                                i.produto.categoria  + "|" + str(i.quantidade))
                arq.writelines('\n')

class ControllerPessoa:
    pass

class ControllerProduto:
    pass

