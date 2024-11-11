import psycopg2
from psycopg2.extras import RealDictCursor

# conecte-se ao postgresql
conn = psycopg2.connect(
    host="localhost",
    database="biblioteca",
    user="postgres",
    password="Biellucas1"
)
cursor = conn.cursor()

def cadastrar_bibliotecario(bibliotecario):
    cursor.execute(
        """
        insert into bibliotecario (nome, endereco, cidade, cep, telefone, cpf)
        values (%s, %s, %s, %s, %s, %s) returning id;
        """,
        (bibliotecario.nome, bibliotecario.endereco, bibliotecario.cidade, bibliotecario.cep, 
         bibliotecario.telefone, bibliotecario.cpf)
    )
    conn.commit()
    bibliotecario_id = cursor.fetchone()[0]
    print("\nbibliotecário cadastrado com id:", bibliotecario_id)
    

# função para obter bibliotecários
def get_bibliotecarios():
    cursor.execute("select * from bibliotecario;")
    data = cursor.fetchall()  # obtém os dados (tuplas)
    columns = [desc[0] for desc in cursor.description]  # obtém os nomes das colunas
    return data, columns  # retorna tanto os dados quanto as colunas


def cadastrar_assistente(assistente):
    cursor.execute(
        """
        insert into assistente (nome, endereco, cidade, cep, telefone, cpf, id_bibliotecario)
        values (%s, %s, %s, %s, %s, %s, %s) returning id;
        """,
        (assistente.nome, assistente.endereco, assistente.cidade, assistente.cep, 
         assistente.telefone, assistente.cpf, assistente.id_bibliotecario)
    )
    conn.commit()
    assistente_id = cursor.fetchone()[0]
    print("\nassistente cadastrado com id:", assistente_id)



def get_assistentes():
    cursor.execute("select * from assistente;")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # obtém os nomes das colunas
    return data, columns


def cadastrar_usuario(usuario):
    cursor.execute(
        """
        insert into usuario (nome, rua, cidade, cpf, cep, telefone, endereco, multa, id_categoria)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning id;
        """,
        (usuario.nome, usuario.rua, usuario.cidade, usuario.cpf, usuario.cep, usuario.telefone, usuario.endereco, usuario.multa, usuario.id_categoria)
    )
    conn.commit()
    usuario_id = cursor.fetchone()[0]
    print("\nusuário cadastrado com id:", usuario_id)



def get_usuarios():
    cursor.execute("select * from usuario;")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return data, columns

# função para cadastrar livro
def cadastrar_livro(livro):
    cursor.execute(
        """
        insert into livro (titulo, autores, isbn, editora, id_colecao, id_bibliotecario)
        values (%s, %s, %s, %s, %s, %s) returning isbn;
        """,
        (livro.titulo, livro.autores, livro.isbn, livro.editora, livro.id_colecao, livro.id_bibliotecario)
    )
    conn.commit()
    print("\nlivro cadastrado com isbn:", livro.isbn)


def get_livros():
    cursor.execute("select * from livro;")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return data, columns


# função para cadastrar exemplar
def cadastrar_exemplar(exemplar, isbn):
    cursor.execute(
        """
        insert into exemplar (isbn_livro, status, id_bibliotecario)
        values (%s, %s, %s) returning id;
        """,
        (isbn, exemplar.status, exemplar.id_bibliotecario)
    )
    conn.commit()
    print("exemplar cadastrado para o livro com isbn:", isbn)


def get_exemplares(isbn):
    cursor.execute("select * from exemplar where isbn_livro = %s;", (isbn,))
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return data, columns


def get_exemplar(isbn, id):
    cursor.execute(
        """
        select * from exemplar where isbn_livro = %s and id = %s;
        """, 
        (isbn, id)
    )
    data = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description] if data else []
    return data, columns

# função para verificar isbn
def verificar_isbn(isbn):
    cursor.execute("select 1 from livro where isbn = %s;", (isbn,))
    return cursor.fetchone() is not None

# função para atualizar status de exemplar
def atualizar_exemplar(id_exemplar, novo_status):
    cursor.execute(
        """
        update exemplar
        set status = %s
        where id = %s;
        """,
        (novo_status, id_exemplar)
    )
    conn.commit()
    print("status do exemplar atualizado.")

# função para adicionar empréstimo
def adicionar_emprestimo_usuario(emprestimo):
    cursor.execute(
        """
        insert into emprestimo (data_emp, data_dev, renovacoes, id_exemplar, id_usuario)
        values (%s, %s, %s, %s, %s) returning id;
        """,
        (emprestimo.data_emp, emprestimo.data_dev, emprestimo.renovacoes, emprestimo.id_exemplar, emprestimo.id_usuario)
    )
    conn.commit()
    emprestimo_id = cursor.fetchone()[0]
    print("empréstimo adicionado com sucesso com id:", emprestimo_id)

# função para obter o id do último empréstimo
def get_id_ultimo_emprestimo():
    cursor.execute("select id from emprestimo order by id desc limit 1;")
    ultimo_emprestimo = cursor.fetchone()
    if ultimo_emprestimo:
        return ultimo_emprestimo[0]
    return 0

# função para obter um usuário por cpf
def get_usuario(cpf):
    cursor.execute("select * from usuario where cpf = %s;", (cpf,))
    return cursor.fetchone()


def get_emprestimo(isbn, exemplar):
    cursor.execute(
        """
        select * from emprestimo where isbn_livro = %s and id_exemplar = %s;
        """, 
        (isbn, exemplar)
    )
    data = cursor.fetchone()  # retorna uma única linha, ou none se não houver correspondência
    columns = [desc[0] for desc in cursor.description] if data else []  # obtém os nomes das colunas, se houver dados
    return data, columns


# função para atualizar empréstimo
def atualizar_emprestimo(id_emprestimo, data_devolucao, multa, renovacoes):
    cursor.execute(
        """
        update emprestimo
        set data_dev = %s, multa = %s, renovacoes = %s
        where id = %s;
        """,
        (data_devolucao, multa, renovacoes, id_emprestimo)
    )
    conn.commit()
    print("empréstimo atualizado com sucesso!")

# função para obter coleção do livro
def get_colecao(isbn):
    cursor.execute(
        """
        select id_colecao from livro where isbn = %s;
        """,
        (isbn,)
    )
    colecao = cursor.fetchone()
    return colecao[0] if colecao else None

# função para apagar empréstimo do usuário
def apagar_emprestimo_usuario(cpf, emprestimo_id, multa):
    cursor.execute(
        """
        delete from emprestimo
        where id = %s and id_usuario = (select id from usuario where cpf = %s);
        """,
        (emprestimo_id, cpf)
    )
    conn.commit()
    print("empréstimo apagado com sucesso!")


def get_todos_emprestimos():
    cursor.execute("select * from emprestimo;")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return data, columns


# função para atualizar o empréstimo no usuário
def atualizar_emprestimo_em_usuario(cpf, id_emprestimo, renovacoes, fim):
    cursor.execute(
        """
        update usuario
        set renovacoes = %s, fim = %s
        where cpf = %s and exists (
            select 1 from emprestimo where id = %s and id_usuario = usuario.id
        );
        """, 
        (renovacoes, fim, cpf, id_emprestimo)
    )
    conn.commit()
    print("empréstimo do usuário atualizado com sucesso!")
    
    

def cadastrar_colecao(colecao):
    query = "INSERT INTO colecao (nome) VALUES (%s) RETURNING id;"
    # Supondo que o banco de dados esteja configurado e que você tenha uma conexão aberta
    cursor = conn.cursor()
    cursor.execute(query, (colecao.nome,))
    id_colecao = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return id_colecao
