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
        print(f'========== Categorias ==========')
        for i in categorias:            
                
                print(f'Categoaria: {i.categoria}')
#a = ControllerCategoria()
#a.cadastraCategoria('Roupa')
#a.removerCategoria('Bebidas')
#a.alterarCategoria('Frutas','novaFrutas')
#a.mostrarCategoria()

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
            print("O produto removido com sucesso.")
        else:
            print("O produto que deseja remover não existe")
    
        with open ('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + 
                                i.produto.categoria  + "|" + str(i.quantidade))
                arq.writelines('\n')

    def alterarProduto(self, nomeAlterar, novoNome, novoPreco, novaCategoria, novaQuantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        
        h = list(filter(lambda x: x.categoria == novaCategoria, y))
        if len(h) > 0:
            est = list(filter(lambda x: x.produto.nome == nomeAlterar, x))
            if len(est) > 0:
                est = list(filter(lambda x: x.produto.nome == novoNome, x))
                if len(est) == 0:
                    x = list(map(lambda x: Estoque(Produtos(novoNome, novoPreco, novaCategoria), novaQuantidade) if (x.produto.nome == nomeAlterar) else(x), x))
                    print('O produto foi alterado com sucesso.')
                else:
                    print('O produto já cadastrado.')                    
            else:
                print("O produto que deseja alterar não existe.")
            
            with open ('estoque.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + 
                                    i.produto.categoria  + "|" + str(i.quantidade))
                    arq.writelines('\n')
        else:
            print("A categoria informada não existe")

    def mostrarEstoque(self):
        estoque = DaoEstoque.ler()
        if len(estoque) == 0:
            print ('Estoque vazio')
        else:            
            print("========== Produtos ==========")
            for i in estoque:
                print(f"Nome: {i.produto.nome}\n"
                      f"Preço: {i.produto.preco}\n"
                      f"Categoria: {i.produto.categoria}\n"
                      f"Quantidade: {i.quantidade}")
                print("--------------------")
#a = ControllerEstoque()
#a.cadastrarProduto ('Camisa', '5', 'Roupa', 20)
#a.removerProduto ('Camisa')
#a.alterarProduto ('banana','bananaAlterar', '100','novaFrutas','30')
#a.mostrarEstoque()

class ControllerVenda:
    def cadastrarVenda(self, nomeProduto, vendedor, comprador, quantidadeVendida):         
        x = DaoEstoque.ler()
        temp = []
        existe = False
        quantidade = False
        for i in x:
            if existe == False:
                if i.produto.nome == nomeProduto:
                    existe = True
                    if i.quantidade >= quantidadeVendida:
                        quantidade = True
                        i.quantidade = int(i.quantidade) - int(quantidadeVendida)

                        vendido = Venda(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidadeVendida)
                                            
                        valorCompra = int(quantidadeVendida) * int(i.produto.preco)  

                        DaoVenda.salvar(vendido)

            temp.append(Estoque(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade))

        arq = open ('estoque.txt', 'w')
        arq.write("")

        for i in temp:
                with open ('estoque.txt', 'a') as arq:
                    arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + i.produto.categoria + "|" + str(i.quantidade))
                    arq.writelines("\n")  

        if existe == False:
            print("O produto não existe")
            return None
        elif not quantidade:
            print ("A quantidade vendida não contem em estoque")
            return None
        else:
            print ("Venda realizada com sucesso")
            return valorCompra

    def relatorioVendas(self):
        vendas = DaoVenda.ler()
        produtos = []

        for i in vendas:
            nome = i.itensVendido.nome
            quantidade = i.quantidadeVendida
            tamanho = list(filter(lambda x: x['produto'] == nome, produtos))
            if len(tamanho) >0:
                produtos = list(map(lambda x: {'produto': nome, 'quantidade': int(x['quantidade']) + int(quantidade)}
                if (x['produto'] == nome) else (x), produtos))
            else:
                produtos.append({'produto': nome, 'quantidade': int(quantidade)})

        ordenado = sorted(produtos, key=lambda k: k['quantidade'], reverse=True)

        print('Esses são os produtos mais vendidos')
        a = 1
        for i in ordenado:
            print(f'========== Produto [{a}] ==========')
            print(f"Produto: {i['produto']}\n"
                f"Quantidade: {i['quantidade']}\n")
            a += 1

    def mostrarVenda(self,dataInicio, dataTermino):
        vendas = DaoVenda.ler()
        dataInicio1 = datetime.strptime(dataInicio,'%d/%m/%Y')
        dataTermino1 = datetime.strptime(dataTermino,'%d/%m/%Y')
        
        vendasSelecionadas = list(filter(lambda x: datetime.strptime(x.data,'%d/%m/%Y') >= dataInicio1
                                and datetime.strptime(x.data,'%d/%m/%Y') <= dataTermino1, vendas))
        
        cont = 1
        total = 0
        for i in vendasSelecionadas:
            print(f'========== Venda [{cont}]==========')
            print(f'Nome: {i.itensVendido.nome}\n'
                f'Categoria: {i.itensVendido.categoria}\n'
                f'Data: {i.data}\n'
                f'Quantidade: {i.quantidadeVendida}\n'
                f'Cliente: {i.comprador}\n'
                f'Vendedor: {i.vendedor}\n')

            total += int(i.itensVendido.preco) * int(i.quantidadeVendida)
            cont += 1
        print (f'Total vendido: {total}')
#a = ControllerVenda()
#a.cadastrarVenda('novoEstoque','erika','adailza',1)
#a.relatorioVendas()
#a.mostrarVenda("07/12/2022", "20/12/2022")

## DAQUI PRA CIMA ESTA OK ##

class ControllerFornecedor:
    def cadastarFornecedor(self, nome, cnpj, telefone, categoria):
        x = DaoFornecedor.ler()
        listaCnpj = list(filter(lambda x: x.cnpj == cnpj, x))
        listaTelefone = list(filter(lambda x: x.telefone == telefone, x))
        if len(listaCnpj) > 0:
            print('O CNPJ já existe.')
        elif len(listaTelefone) > 0:
            print('O telefone já existe.')
        else:
            if len(cnpj) == 14 and len(telefone) <= 11 and len(telefone) >= 10:
                DaoFornecedor.salvar(Fornecedor(nome, cnpj, telefone, categoria))
                print('Fornecedor cadastrado com sucesso.')
            else:
                print('Digite um CNPJ ou telefone válido.')
    
    def alterarFornecedor(self, nomeAlterar, novoNome, novoCnpj, novoTelefone, novaCategoria):
        x = DaoFornecedor.ler()

        est = list(filter(lambda x: x.nome == nomeAlterar, x)) 
                   
        if len(est) > 0:
            est = list(filter(lambda x: x.cnpj == novoCnpj, x))
            if len (est) == 0:
                x = list(map(lambda x: Fornecedor(novoNome, novoCnpj, novoTelefone, novaCategoria) if (x.nome != nomeAlterar) else(x), x))
                print('========')
            else:
                print('O CNPJ já existe')
        else:
            print('O fornecedor que deseja alterar não existe.')
    

        with open ('fornecedores.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + '|' + i.cnpj + '|' + i.telefone + '|' + str(i.categoria))
                arq.writelines('\n')
            print('Fornecedor alterado com sucesso.')

    def removerFornecedor(self, nome):
        x = DaoFornecedor.ler()
        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del x[i]
                    break
        else:
            print('O fornecedor que deseja remover não existe')
            return None

        with open ('fornecedores.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.cnpj + "|" + i.telefone + "|" + str(i.categoria))
                arq.writelines('\n')
            print('Fornecedor removido com sucesso')

    def mostrarFornecedor(self):
        fornecedores = DaoFornecedor.ler()
        if len(fornecedores) > 0:
            print ("Lista de fornecedores vazia")
        
        for i in fornecedores:
            print("========== Fornecedores ==========")
            print(f'Categoria fornecida: {i.categoria}\n'
                    f'Nome: {i.nome}\n'
                    f'Telefone: {i.telefone}\n'
                    f'CNPJ: {i.cnpj}\n')

#a = ControllerFornecedor()
#a.cadastarFornecedor('camila','12345678907474','21000003030','Equipamentos') - Ok
#a.alterarFornecedor('camila','camila', '12345678901234', '21000001111', 'equipamentosNovo')
#Mesmo erro de cima a.removerFornecedor('camila')
#a.mostrarFornecedor()

class ControllerCliente:
    def cadastarCliente(self, nome, cpf, telefone, email, endereco):
        x = DaoPessoa.ler()
        print(x)

        listaCpf = list(filter(lambda x: x.cpf == cpf, x))     

        print(listaCpf)
        if len(listaCpf) > 0:
            print('O Cpf já existe.')
        else:
            if len(cpf) == 11 and len(telefone) <= 11 and len(telefone) >= 10:
                DaoPessoa.salvar(Pessoa(nome, cpf, telefone, email, endereco))
                print('Cliente cadastrado com sucesso.')
            else:
                print('Digite um CPF ou telefone válido.')

    def removerCliente(self, nome):
        x = DaoPessoa.ler()

        cat = list(filter(lambda x: x.nome == nome, x))
        if len(cat) <= 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del x[i]
                    break

            with open('clientes.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.nome + "|" + i.telefone + "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                    arq.writelines('\n')                
            print("Cliente removido com sucesso.")

    def alterarCliente(self, nomeAlterar, nomeAlterada):
        x = DaoPessoa.ler()
        cat = list(filter(lambda x: x.categoria == nomeAlterar, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda x: x.nome == nomeAlterada, x))
            if len(cat1) == 0:
                x = list(map(lambda x: Pessoa(nomeAlterada) if (x.nome == nomeAlterar) else(x),x ))
                print("Cliente foi alterado com sucesso.")

            else:
                print("Cliente para qual deseja alterar já existe.")
        else:
            print("Cliente que deseja alterar não existe.")

        with open ('clientes.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.telefone + "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print('Cliente alterado com sucesso.')

    def mostrarCliente(self):
        clientes = DaoPessoa.ler()

        if len (clientes) == 0:
            print("Categoria vazia.")

        print(f'========== Categorias ==========')
        for i in clientes:
                print(f'Nome: {i.nome}\n'
                    f'Telefone: {i.telefone}\n'
                    f'Endereço: {i.endereco}\n'
                    f'Email: {i.email}\n'
                    f'CPF: {i.cpf}\n')
#a = ControllerCliente()
#a.cadastarCliente('Cliente02','33322211102','21999990002','email02@email.com','endereco02')
#a.removerCliente('Cliente01')

class ControllerFuncionario:
    def cadastarFuncionario(self, clt, nome, cpf, telefone, endereco):
        x = DaoFuncionario.ler()

        listaCpf = list(filter(lambda x: x.cpf == cpf, x))
        listaClt = list(filter(lambda x: x.clt == clt, x))

        if len(listaCpf) > 0:
            print('O CPF já existe.')
        elif len(listaClt) > 0:
            print('O clt já existe.')
        else:
            if len(cpf) == 14 and len(telefone) <= 11 and len(telefone) >= 10:
                DaoFuncionario.salvar(Funcionario(clt, nome, cpf, telefone, endereco))
                print('Funcionario cadastrado com sucesso.')
            else:
                print('Digite um CPF ou Telefone válido.')
            
    def alterarFuncionario(self, nomeAlterar, novoClt, novoNome, novoTelefone, novoEmail, novoEndereco):
        x = DaoFuncionario.ler()

        est = list(filter(lambda x: x.nome == nomeAlterar, x)) 
        if len (est) == 0:
                x = list(map(lambda x: Funcionario(nomeAlterar, novoClt, novoNome, novoTelefone, novoEmail, novoEndereco) if (x.nome == nomeAlterar) else(x), x))
        else:
            print('O funcionario que deseja alterar não existe.')
    

        with open ('funcionarios.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.clt  + '|' +  i.nome + '|' + i.telefone + '|' + i.cpf + '|' + i.endereco)
                arq.writelines('\n')
            print('Funcionario alterado com sucesso.')

    def removerFuncionario(self, nome):
        x = DaoFuncionario.ler()
        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del x[i]
                    break
        else:
            print('O funcionario que deseja remover não existe')
            return None

        with open ('funcionarios.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.clt  + '|' +  i.nome + '|' + i.telefone + '|' + i.cpf + '|' + i.endereco)
                arq.writelines('\n')
            print('Funcionario alterado com sucesso.')
   
    def mostrarFuncionario(self):
        funcionario = DaoFuncionario.ler()

        if len (funcionario) == 0:
            print("Categoria vazia.")

        print(f'========== Funcionarios ==========')
        for i in funcionario:
                print(f'CLT: {i.clt}\n'
                    f'Nome: {i.nome}\n'
                    f'CPF: {i.cpf}\n'
                    f'Telefone: {i.telefone}\n'
                    f'Endereço: {i.endereco}\n')
                    