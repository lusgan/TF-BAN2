from datetime import datetime, timedelta
import datetime
import DAO

# Classes da Biblioteca
class Livro:
    def __init__(self, titulo, autores, isbn, editora,id_colecao, id_bibliotecario):
        self.titulo = titulo
        self.autores = autores  # lista de autores
        self.isbn = isbn
        self.editora = editora
        self.id_colecao = id_colecao #CORRIGIR PARA RECEBER O ID DA COLECAO
        self.id_bibliotecario = id_bibliotecario
        self.exemplares = []

    def to_json(self):
        json = {'Titulo': self.titulo, 'autores': self.autores, 'isbn': self.isbn, 'Editora': self.editora, 'Colecao': self.colecao, 'Exemplares': self.exemplares}
        return json

    def nome_dos_autores_string(self):
        nomes = ""
        if isinstance(self.autores, list):
            for autor in self.autores:
                nomes = nomes + f"{autor.nome},"
        else:
            nomes = self.autores.nome
        return nomes


class Colecao:
    def __init__(self, nome):
        self.nome = nome
        self.id = None  # O ID será atribuído após a inserção no banco


class Exemplar:
    def __init__(self, id, status, id_bibliotecario):
        self.id = id
        self.status = status
        self.id_bibliotecario = id_bibliotecario
        self.posse = None

    def to_json(self):
        json = {'num': self.num, 'status': self.status, 'posse': self.posse}
        return json


class Bibliotecario:
    def __init__(self, cpf, nome, rua, cidade, cep, telefone, endereco):
        self.cpf = cpf
        self.nome = nome
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.telefone = telefone
        self.endereco = endereco

    def to_json(self):
        json = {'CPF': self.cpf, 'Nome': self.nome, 'Rua': self.rua, 'Cidade': self.cidade, 'CEP': self.cep, 'Telefone': self.telefone, 'Endereco': self.endereco}
        return json


class Assistente:
    def __init__(self, cpf, nome, rua, cidade, cep, telefone, endereco, supervisores):
        self.cpf = cpf
        self.nome = nome
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.telefone = telefone
        self.endereco = endereco
        self.supervisores = supervisores

    def to_json(self):
        json = {'CPF': self.cpf, 'Nome': self.nome, 'Rua': self.rua, 'Cidade': self.cidade, 'CEP': self.cep, 'Telefone': self.telefone, 'Endereco': self.endereco, 'Supervisores': self.supervisores}
        return json


class Usuario:
    def __init__(self, cpf, nome, rua, cidade, cep, telefone, endereco, multa, id_categoria):
        self.cpf = cpf
        self.nome = nome
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.telefone = telefone
        self.endereco = endereco
        self.multa = multa
        self.id_categoria = id_categoria
        self.emprestimos = []

    def to_json(self):
        json = {'CPF': self.cpf, 'Nome': self.nome, 'Rua': self.rua, 'Cidade': self.cidade, 'CEP': self.cep, 'Telefone': self.telefone, 'Endereco': self.endereco, 'Multa': self.multa, 'Categoria': self.categoria, 'Emprestimos': self.emprestimos}
        return json


class Autor:
    def __init__(self, nome):
        self.nome = nome


class Emprestimo:
    def __init__(self, data_hoje, isbn, num_exemplar, CPF, qtd_dias):
        self.id_emprestimo = DAO.get_id_ultimo_emprestimo() + 1
        self.dataInicial = data_hoje.strftime('%d-%m-%Y')
        self.dataFinal = (data_hoje + timedelta(days=qtd_dias)).strftime('%d-%m-%Y')
        self.dia_que_foi_devolvido = None
        self.isbn = isbn
        self.num_exemplar = num_exemplar
        self.CPF = CPF
        self.multa = None
        self.renovacoes = 0

    def devolver(self, data):
        self.livro.emprestado = False
        self.dia_que_foi_devolvido = data
        if data > self.dataFinal:
            self.usuario.penalizar(data, self)

    def to_json(self):
        json = {'id': self.id_emprestimo, 'Inicio': self.dataInicial, 'Fim': self.dataFinal, 'Data de devolucao': self.dia_que_foi_devolvido, 'isbn': self.isbn, 'Exemplar': self.num_exemplar, 'CPF': self.CPF, 'Multa': self.multa, 'Renovacoes': self.renovacoes}
        return json


def usuario_possui_atraso(CPF, data_hoje):
    usuario = DAO.get_usuario(CPF)
    emprestimos = usuario['Emprestimos']

    if not emprestimos:
        return False

    for emprestimo in emprestimos:
        data_fim_iso = emprestimo['Fim']
        data_fim = datetime.datetime.strptime(data_fim_iso, "%d-%m-%Y").date()

        if data_hoje > data_fim:
            return True

    return False


def emprestar_livro(emprestimo, data_hoje):
    exemplar = DAO.get_exemplar(emprestimo.isbn, emprestimo.num_exemplar)

    if not exemplar:
        print("Exemplar nao cadastrado.")
    else:
        usuario = DAO.get_usuario(emprestimo.CPF)

        limite_de_emprestimos = 4
        emprestimos = usuario[9]
        qtd_emprestimos = 0

        if emprestimos:
            qtd_emprestimos = len(emprestimos)

        if exemplar['status'] == 'Indisponivel':
            print("Exemplar indisponivel.\n")
        elif usuario_possui_atraso(emprestimo.CPF, data_hoje):
            print("Usuario possui livro com atraso.\n")
        elif usuario['Multa'] > 0:
            print("Usuario possui multa pendente.\n")
        elif qtd_emprestimos + 1 > limite_de_emprestimos:
            print("Usuario ja atingiu limite de emprestimos!\n")
        elif DAO.get_colecao(emprestimo.isbn).lower() == "reserva":
            print("Esse livro faz parte da colecao reserva, logo não pode ser emprestado.")
        else:
            DAO.atualizar_exemplar(emprestimo.isbn, emprestimo.num_exemplar, "Indisponivel", emprestimo.CPF)
            DAO.adicionar_emprestimo_usuario(emprestimo)


def devolver_livro(isbn, num_exemplar, data_devolucao):
    emprestimo = DAO.get_emprestimo(isbn, num_exemplar)
    multa = None
    renovacoes = emprestimo['Renovacoes']

    if data_devolucao > datetime.datetime.strptime(emprestimo['Fim'], "%d-%m-%Y").date():
        multa = 30

    Fim = emprestimo["Fim"]
    DAO.atualizar_emprestimo(isbn, num_exemplar, data_devolucao.strftime('%d-%m-%Y'), multa, renovacoes, Fim)
    DAO.atualizar_exemplar(isbn, num_exemplar, 'Disponivel', None)
    DAO.apagar_emprestimo_usuario(emprestimo['CPF'], emprestimo['id'], multa)
 



def renovar_emprestimo(isbn, num_exemplar, data_hoje):
    # Obtém os dados do empréstimo e usuário
    emprestimo = DAO.get_emprestimo(isbn, num_exemplar)
    multa = emprestimo['Multa']
    
    usuario = DAO.get_usuario(emprestimo['CPF'])
    categoria_id = usuario['Categoria']['id']
    
    tempo_em_dias = None
    
    # Define o tempo de renovação com base na categoria do usuário
    if categoria_id == 1:  # Estudante de graduação
        tempo_em_dias = 15
    elif categoria_id == 2:  # Estudante de pós-graduação
        tempo_em_dias = 30
    elif categoria_id == 3:  # Professor
        tempo_em_dias = 30
    elif categoria_id == 4:  # Professor de graduação
        tempo_em_dias = 90
    
    # Verifica se o livro está atrasado
    if data_hoje > datetime.datetime.strptime(emprestimo['Fim'], "%d-%m-%Y").date():
        print("Livro atrasado, não pode ser renovado.")
    
    # Verifica se o número máximo de renovações foi atingido
    elif emprestimo['Renovacoes'] == 3:
        print("Limite de renovações atingido.")
    
    # Verifica se o livro já foi devolvido
    elif emprestimo['Data de devolucao']:
        print("Livro já foi devolvido, não é possível renovar.")
    
    else:
        # Atualiza a quantidade de renovações e a data final
        renovacoes = emprestimo['Renovacoes'] + 1
        data_devolucao = None
        Fim = (data_hoje + timedelta(days=tempo_em_dias)).strftime("%d-%m-%Y")
        
        # Atualiza o empréstimo no banco de dados
        DAO.atualizar_emprestimo(isbn, num_exemplar, data_devolucao, multa, renovacoes, Fim)
        
        # Atualiza a informação de renovação do usuário
        DAO.atualizar_emprestimo_em_usuario(usuario['CPF'], emprestimo['id'], renovacoes, Fim)
