from datetime import datetime, timedelta
import datetime
import DAO

# Classes da Biblioteca

class Colecao:
    def __init__(self, nome):
        self.id = None
        self.nome = nome


class Bibliotecario:
    def __init__(self, cpf, nome, rua, cidade, cep, telefone, endereco):
        self.id = None
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

class Livro:
    def __init__(self, isbn, titulo, editora, autores, id_colecao, id_bibliotecario):
        self.isbn = isbn
        self.titulo = titulo
        self.editora = editora
        self.autores = autores  # lista de autores
        self.id_colecao = id_colecao #CORRIGIR PARA RECEBER O ID DA COLECAO
        self.id_bibliotecario = id_bibliotecario
    
    
    def nome_dos_autores_string(self):
        nomes = ""
        if isinstance(self.autores, list):
            for autor in self.autores:
                nomes = nomes + f"{autor.nome},"
        else:
            nomes = self.autores.nome
        return nomes


class Exemplar:
    def __init__(self, isbn, status, id_bibliotecario):
        self.id = None
        self.isbn = isbn
        self.status = status
        self.id_bibliotecario = id_bibliotecario


class Usuario:
    def __init__(self, nome, rua, cidade, cpf, cep, telefone, endereco, multa, id_categoria):
        self.id = None
        self.nome = nome
        self.rua = rua
        self.cidade = cidade
        self.cpf =cpf
        self.cep = cep
        self.telefone = telefone
        self.endereco = endereco
        self.multa = multa
        self.id_categoria = id_categoria
        
    

class Emprestimo:
    def __init__(self, inicio, fim, id_exemplar, id_usuario):
        self.id = None
        self.inicio = inicio
        self.fim = fim
        self.devolucao = None
        self.renovacoes = 0
        self.id_exemplar = id_exemplar
        self.id_usuario = id_usuario
        
        
class Reserva:
    
    def __init__(self, data_res, id_livro, id_usuario):
        self.id = None
        self.data_res = data_res
        self.id_livro = id_livro
        self.id_usuario = id_usuario
        

class Assistente:
    def __init__(self, cpf, nome, rua, cidade, cep, telefone, endereco, id_bibliotecario):
        self.id = None
        self.cpf = cpf
        self.nome = nome
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.telefone = telefone
        self.endereco = endereco
        self.id_bibliotecario = id_bibliotecario




class Autor:
    def __init__(self, nome):
        self.nome = nome



def usuario_possui_atraso(CPF, data_hoje):
    
    id_usuario = DAO.get_id_usuario(CPF)
    emprestimos, _ = DAO.get_todos_emprestimos_usuario(id_usuario)

    if not emprestimos:
        return False

    for emprestimo in emprestimos:
        data_fim = emprestimo[2] #emprestimo["fim"]
        

        if data_hoje > data_fim:
            return True

    return False


def emprestar_livro(emprestimo, data_hoje):
    exemplar, _ = DAO.get_exemplar(emprestimo.id_exemplar)

    if not exemplar:
        print("Exemplar nao cadastrado.")
    else:
        
        usuario = DAO.get_usuario_pelo_id(emprestimo.id_usuario)
        
        limite_de_emprestimos = 4
        qtd_emprestimos = 0
        
        emprestimos, _ = DAO.get_todos_emprestimos_usuario(emprestimo.id_usuario)
        if emprestimos:
            qtd_emprestimos = len(emprestimos)
        

        if exemplar[2] == 'Indisponivel':
            print("Exemplar indisponivel.\n")
            
        elif usuario_possui_atraso(usuario[4], data_hoje):
            print("Usuario possui livro com atraso.\n")
            
        elif usuario[8] > 0:
            print("Usuario possui multa pendente.\n")
            
        elif qtd_emprestimos + 1 > limite_de_emprestimos:
            print("Usuario ja atingiu limite de emprestimos!\n")
            
        elif DAO.get_colecao(exemplar[1])[0].lower() == "reserva":
            print("Esse livro faz parte da colecao reserva, logo não pode ser emprestado.")
        else:
            DAO.atualizar_exemplar(emprestimo.id_exemplar, "Indisponivel")
            DAO.adicionar_emprestimo_usuario(emprestimo)
            


def devolver_livro(num_exemplar, data_devolucao):
    emprestimo = DAO.get_emprestimo_nao_devolvido(num_exemplar)
    multa = None
    renovacoes = emprestimo[4]

    if data_devolucao > emprestimo[2]:
        multa = 30

    Fim = emprestimo[2]
    DAO.atualizar_emprestimo(emprestimo[0], data_devolucao.strftime('%d-%m-%Y'), multa, renovacoes, Fim)
    DAO.atualizar_exemplar(num_exemplar, 'Disponivel')
    DAO.multar_usuario(multa, emprestimo[6])
    
 



def renovar_emprestimo(isbn, num_exemplar, data_hoje):
    # Obtém os dados do empréstimo e usuário
    emprestimo = DAO.get_emprestimo_nao_devolvido(num_exemplar)
    multa = emprestimo[7]
    
    usuario = DAO.get_usuario_pelo_id(emprestimo[6])
    categoria_id = usuario[9]
    
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
    if data_hoje > emprestimo[2]:
        print("Livro atrasado, não pode ser renovado.")
    
    # Verifica se o número máximo de renovações foi atingido
    elif emprestimo[4] == 3:
        print("Limite de renovações atingido.")
    
    # Verifica se o livro já foi devolvido
    elif emprestimo[3]:
        print("Livro já foi devolvido, não é possível renovar.")
    
    else:
        # Atualiza a quantidade de renovações e a data final
        renovacoes = emprestimo[4] + 1
        data_devolucao = None
        Fim = (data_hoje + timedelta(days=tempo_em_dias)).strftime("%d-%m-%Y")
        
        # Atualiza o empréstimo no banco de dados
        DAO.atualizar_emprestimo(emprestimo[0], data_devolucao, multa, renovacoes, Fim)
        
    
