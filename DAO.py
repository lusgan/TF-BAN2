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
        insert into bibliotecario (cpf, nome, rua, cidade, cep, telefone, endereco)
        values (%s, %s, %s, %s, %s, %s, %s) returning id;
        """,
        (bibliotecario.cpf, bibliotecario.nome, bibliotecario.rua, bibliotecario.cidade, 
         bibliotecario.cep, bibliotecario.telefone, bibliotecario.endereco)
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
        insert into assistente (cpf, nome, rua, cidade, cep, telefone, endereco, id_bibliotecario)
        values (%s, %s, %s, %s, %s, %s, %s, %s) returning id;
        """,
        (assistente.cpf, assistente.nome, assistente.rua, assistente.cidade, assistente.cep, 
         assistente.telefone, assistente.endereco, assistente.id_bibliotecario)
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
        insert into livro (isbn, titulo, editora, autores, id_colecao, id_bibliotecario)
        values (%s, %s, %s, %s, %s, %s) returning isbn;
        """,
        (livro.isbn, livro.titulo, livro.editora, livro.autores, livro.id_colecao, livro.id_bibliotecario)
    )
    conn.commit()
    print("\nlivro cadastrado com isbn:", livro.isbn)


def get_livros():
    cursor.execute("select * from livro;")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return data, columns


# função para cadastrar exemplar
def cadastrar_exemplar(exemplar):
    cursor.execute(
        """
        insert into exemplar (isbn_livro, status, id_bibliotecario)
        values (%s, %s, %s) returning id;
        """,
        (exemplar.isbn, exemplar.status, exemplar.id_bibliotecario)
    )
    conn.commit()
    print("exemplar cadastrado para o livro com isbn:", exemplar.isbn)


def get_exemplares(isbn):
    cursor.execute("select * from exemplar where isbn_livro = %s;", (isbn,))
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return data, columns


def get_exemplar(id):
    cursor.execute(
        """
        select * from exemplar where id = %s;
        """, 
        (id,)
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
        insert into emprestimo (inicio, fim, devolucao, renovacoes, id_exemplar, id_usuario)
        values (%s, %s, %s, %s, %s, %s) returning id;
        """,
        (emprestimo.inicio, emprestimo.fim, emprestimo.devolucao, emprestimo.renovacoes, emprestimo.id_exemplar, emprestimo.id_usuario)
    )
    conn.commit()
    emprestimo_id = cursor.fetchone()[0]
    print("empréstimo adicionado com sucesso com id:", emprestimo_id)



# função para obter um usuário por cpf
def get_usuario(cpf):
    cursor.execute("select * from usuario where cpf = %s;", (cpf,))
    return cursor.fetchone()


def get_usuario_pelo_id(id):
    cursor.execute("select * from usuario where id = %s;", (id,))
    return cursor.fetchone()

def get_id_usuario(cpf):
    cursor.execute("select id from usuario where cpf = %s;",(cpf,))
    return cursor.fetchone()

def get_todos_emprestimos_usuario(id_usuario):
    cursor.execute(
        """
        select * from emprestimo where id_usuario = %s;
        """, 
        (id_usuario,)
    )
    data = cursor.fetchall()  # retorna uma única linha, ou none se não houver correspondência
    columns = [desc[0] for desc in cursor.description] if data else []  # obtém os nomes das colunas, se houver dados
    return data, columns


# função para atualizar empréstimo
def atualizar_emprestimo(id_emprestimo, devolucao, multa, renovacoes, fim):
    cursor.execute(
        """
        update emprestimo
        set devolucao = %s, multa = %s, renovacoes = %s, fim = %s
        where id = %s;
        """,
        (devolucao, multa, renovacoes, fim, id_emprestimo)
    )
    conn.commit()
    print("empréstimo atualizado com sucesso!")
    

def multar_usuario(multa, usuario_id):
    cursor.execute(
            """
            UPDATE usuario
            SET multa = %s
            WHERE id = %s;
            """, 
            (multa, usuario_id)  # Passa o valor 30 para multa e o id do usuário
        ) 
    conn.commit()

# função para obter coleção do livro
def get_colecao(isbn):
    cursor.execute(
        """
        select colecao.nome from colecao join livro ON colecao.id = livro.id_colecao and isbn= %s;
        """,
        (isbn,)
    )
    colecao = cursor.fetchone()
    return colecao[0] if colecao else None



def get_todos_emprestimos():
    cursor.execute("select * from emprestimo;")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return data, columns


        

def cadastrar_colecao(colecao):
    query = "INSERT INTO colecao (nome) VALUES (%s) RETURNING id;"
    cursor = conn.cursor()
    cursor.execute(query, (colecao.nome,))
    id_colecao = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return id_colecao


def get_emprestimo_nao_devolvido(id_exemplar):
    cursor.execute("select * from emprestimo where id_exemplar = %s and devolucao is NULL",(id_exemplar,))
    return cursor.fetchone()

    
