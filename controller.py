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
        
        estoque = DaoEstoque.ler()

        estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, "Sem categoria"), x.quantidade)
        if (x.produto.categoria == categoriaRemover) else(x), estoque))

        with open ('estoque.txt', 'w') as arq:
            for i in estoque:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + i.produto.categoria + "|" + str(i.quantidade))
                arq.writelines('\n')

    def alterarCategoria(self, categoriaAlterar, categoriaAlterada):
        x = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == categoriaAlterar, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda x: x.categoria == categoriaAlterada, x))
            if len(cat1) == 0:
                x = list(map(lambda x: Categoria(categoriaAlterada) if (x.categoria == categoriaAlterar) else(x),x ))
                print("A categoria foi alterada com sucesso.")

                with open('categoria.txt', 'w') as arq:
                    for i in x:
                        arq.writelines(i.categoria)
                        arq.writelines("\n")
        
                estoque = DaoEstoque.ler()

                estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, categoriaAlterada), x.quantidade)
                if (x.produto.categoria == categoriaAlterar) else(x), estoque))

                with open ('estoque.txt', 'w') as arq:
                    for i in estoque:
                        arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + i.produto.categoria + "|" + str(i.quantidade))
                        arq.writelines('\n')
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
# a = ControllerCategoria()
# a.cadastraCategoria('Verduras')
# a.removerCategoria('Roupa')
# a.alterarCategoria('Roupa','novaRoupa')
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
# a = ControllerEstoque()
# a.cadastrarProduto ('legumes01', '5', 'Legumes', 20)
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
a = ControllerVenda()
# a.cadastrarVenda('novo02','02','02',1)
#a.relatorioVendas()
#a.mostrarVenda("07/12/2022", "20/12/2022")

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
                x = list(map(lambda x: Fornecedor(novoNome, novoCnpj, novoTelefone, novaCategoria) if (x.nome == nomeAlterar) else(x), x))
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
#a.cadastarFornecedor('camiladel','12345678907001','21000009991','Equipamentos')
#a.alterarFornecedor('camila','camila', '12345678901234', '21000001111', 'equipamentosNovo')
#a.removerFornecedor('camiladel')
#a.mostrarFornecedor()

## DAQUI PRA CIMA ESTA OK ##
class ControllerCliente:
    def cadastarPessoa(self, nome, telefone, cpf, email, endereco):
        x = DaoPessoa.ler()
        
        listaCpf = list(filter(lambda x: x.cpf == cpf, x))
        if len(listaCpf) > 0:
            print('O Cpf já existe.')
        else:
            if len(cpf) == 11 and len(telefone) <= 11 and len(telefone) >= 10:
                DaoPessoa.salvar(Pessoa(nome, telefone, cpf, email, endereco))
                print('Cliente cadastrado com sucesso.')
            else:
                print('Digite um CPF ou telefone válido.')

    def alterarPessoa(self, nomeAlterar, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco):
        x = DaoPessoa.ler()

        est = list(filter(lambda x: x.nome == nomeAlterar, x))
        if len (est) > 0:
                x = list(map(lambda x: Pessoa(novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco) if
                (x.nome == nomeAlterar) else (x), x))
        else:
            print("Cliente que deseja alterar não existe.")
            return None

        with open ('clientes.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.telefone + "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print('Cliente alterado com sucesso.')

    def removerPessoa(self, nome):
        x = DaoPessoa.ler()

        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del x[i]
                    break
        else:
            print('O cliente que deseja remover não existe')
            return None        

        with open('clientes.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.telefone + "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')                
            print("Cliente removido com sucesso.")

    def mostrarPessoa(self):
        x = DaoPessoa.ler()

        if len (x) == 0:
            print("Categoria vazia.")

        print(f'========== Categorias ==========')
        for i in x:
                print(f'Nome: {i.nome}\n'
                    f'Telefone: {i.telefone}\n'
                    f'CPF: {i.cpf}\n'                    
                    f'Email: {i.email}\n'
                    f'Endereço: {i.endereco}')
a = ControllerCliente()
# a.cadastarPessoa('ClienteDel','21000000005','33322211105','email05@email.com','endereco05') - Ok
# a.cadastarPessoa('Cliente06','21000000006','33322211106','email06@email.com','endereco06')
# a.cadastarPessoa('Cliente07','21000000007','33322211107','email07@email.com','endereco07')
# a.cadastarPessoa('Cliente08','21000000008','33322211108','email08@email.com','endereco08')
# a.cadastarPessoa('Cliente09','21000000009','33322211109','email09@email.com','endereco09')
# a.cadastarPessoa('Cliente21','21000000021','33322211121','email21@email.com','endereco21')
# a.alterarPessoa('ClienteDel','nomeAleterado','21000000100','33322211100','email100@email.com','endereco100')
# a.removerPessoa('ClienteDel')
# a.mostrarPessoa() - Ok
### NÃO ESTA FUNCIONANDO altearPessoa e removerPesssoa. ### ERRO INEXPLICAVEL  ###

class ControllerFuncionario:
    def cadastarFuncionario(self, clt, nome, telefone, cpf, email, endereco):
        x = DaoFuncionario.ler()

        listaCpf = list(filter(lambda x: x.cpf == cpf, x))
        listaClt = list(filter(lambda x: x.clt == clt, x))

        if len(listaCpf) > 0:
            print('O CPF já existe.')
        elif len(listaClt) > 0:
            print('O clt já existe.')
        else:
            if len(clt) == 14 and len(telefone) <= 11 and len(telefone) >= 10:
                DaoFuncionario.salvar(Funcionario(clt, nome, telefone, cpf, email, endereco))
                print('Funcionario cadastrado com sucesso.')
            else:
                print('Digite um CNPJ ou Telefone válido.')

    def alterarFuncionario(self, nomeAlterar, novoClt, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco):
        x = DaoFuncionario.ler()

        est = list(filter(lambda x: x.nome == nomeAlterar, x)) 
        if len (est) > 0:
                x = list(map(lambda x: Funcionario(novoClt, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco) if (x.nome == nomeAlterar) else(x), x))
        else:
            print('O funcionario que deseja alterar não existe.')
            return None    

        with open ('funcionarios.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.clt  + '|' +  i.nome + '|' + i.telefone + '|' + i.cpf + '|' + i.email + '|' + i.endereco)
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
                arq.writelines(i.clt  + '|' +  i.nome + '|' + i.telefone + '|' + i.cpf + '|' + i.email + '|' + i.endereco)
                arq.writelines('\n')
            print('Funcionario removido com sucesso.')
   
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
# a = ControllerFuncionario() - Ok
# a.cadastarFuncionario('12345678900001', 'Func01', '21000009991', '12345678901', 'f01@g.com', 'end01') - Ok
# a.cadastarFuncionario('12345678900002', 'Func02', '21000009992', '12345678902', 'f02@g.com', 'end02') - Ok
# a.cadastarFuncionario('12345678900003', 'Func03', '21000009993', '12345678903', 'f03@g.com', 'end03') - Ok
# a.alterarFuncionario('Func02','12345678900005', 'Func05', '21000009995', '12345678905', 'f05@g.com', 'end05') - Ok
# a.removerFuncionario('Func01') - Ok
# a.mostrarFuncionario() - Ok