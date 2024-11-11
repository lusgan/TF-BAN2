import psycopg2
from psycopg2.extras import RealDictCursor

# Conecte-se ao PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="biblioteca",
    user="postgres",
    password="Biellucas1"
)
cursor = conn.cursor()

# Função para cadastrar bibliotecário
def cadastrar_bibliotecario(bibliotecario):
    cursor.execute(
        """
        INSERT INTO Bibliotecario (nome, endereco, cidade, cep, telefone)
        VALUES (%s, %s, %s, %s, %s) RETURNING ID;
        """,
        (bibliotecario.nome, bibliotecario.endereco, bibliotecario.cidade, bibliotecario.cep, bibliotecario.telefone)
    )
    conn.commit()
    bibliotecario_id = cursor.fetchone()[0]
    print("\nBibliotecário cadastrado com ID:", bibliotecario_id)

# Função para obter bibliotecários
def get_bibliotecarios():
    cursor.execute("SELECT * FROM Bibliotecario;")
    return cursor.fetchall()

# Função para cadastrar assistente
def cadastrar_assistente(assistente):
    cursor.execute(
        """
        INSERT INTO Assistente (nome, endereco, cidade, cep, telefone, id_bibliotecario)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING ID;
        """,
        (assistente.nome, assistente.endereco, assistente.cidade, assistente.cep, assistente.telefone, assistente.id_bibliotecario)
    )
    conn.commit()
    assistente_id = cursor.fetchone()[0]
    print("\nAssistente cadastrado com ID:", assistente_id)

# Função para obter assistentes
def get_assistentes():
    cursor.execute("SELECT * FROM Assistente;")
    return cursor.fetchall()

# Função para cadastrar usuário
def cadastrar_usuario(usuario):
    cursor.execute(
        """
        INSERT INTO Usuario (nome, cpf, endereco, telefone)
        VALUES (%s, %s, %s, %s) RETURNING ID;
        """,
        (usuario.nome, usuario.cpf, usuario.endereco, usuario.telefone)
    )
    conn.commit()
    usuario_id = cursor.fetchone()[0]
    print("\nUsuario cadastrado com ID:", usuario_id)

# Função para obter usuários
def get_usuarios():
    cursor.execute("SELECT * FROM Usuario;")
    return cursor.fetchall()

# Função para cadastrar livro
def cadastrar_livro(livro):
    cursor.execute(
        """
        INSERT INTO Livro (ISBN, titulo, editora, id_colecao, id_bibliotecario)
        VALUES (%s, %s, %s, %s, %s) RETURNING ISBN;
        """,
        (livro.isbn, livro.titulo, livro.editora, livro.id_colecao, livro.id_bibliotecario)
    )
    conn.commit()
    print("\nLivro cadastrado com ISBN:", livro.isbn)

# Função para obter livros
def get_livros():
    cursor.execute("SELECT * FROM Livro;")
    return cursor.fetchall()

# Função para cadastrar exemplar
def cadastrar_exemplar(exemplar, ISBN):
    cursor.execute(
        """
        INSERT INTO Exemplar (isbn_livro, status, id_bibliotecario)
        VALUES (%s, %s, %s) RETURNING id;
        """,
        (ISBN, exemplar.status, exemplar.id_bibliotecario)
    )
    conn.commit()
    print("Exemplar cadastrado para o livro com ISBN:", ISBN)

# Função para obter exemplares
def get_exemplares(ISBN):
    cursor.execute("SELECT * FROM Exemplar WHERE isbn_livro = %s;", (ISBN,))
    return cursor.fetchall()

# Função para obter um exemplar específico
def get_exemplar(ISBN, numero):
    cursor.execute(
        """
        SELECT * FROM Exemplar WHERE isbn_livro = %s AND num = %s;
        """, 
        (ISBN, numero)
    )
    return cursor.fetchone()

# Função para verificar ISBN
def verificar_isbn(isbn):
    cursor.execute("SELECT 1 FROM Livro WHERE ISBN = %s;", (isbn,))
    return cursor.fetchone() is not None

# Função para atualizar status de exemplar
def atualizar_exemplar(id_exemplar, novo_status):
    cursor.execute(
        """
        UPDATE Exemplar
        SET status = %s
        WHERE id = %s;
        """,
        (novo_status, id_exemplar)
    )
    conn.commit()
    print("Status do exemplar atualizado.")

# Função para adicionar empréstimo
def adicionar_emprestimo_usuario(emprestimo):
    cursor.execute(
        """
        INSERT INTO Emprestimo (data_emp, data_dev, renovacoes, id_exemplar, id_usuario)
        VALUES (%s, %s, %s, %s, %s) RETURNING ID;
        """,
        (emprestimo.data_emp, emprestimo.data_dev, emprestimo.renovacoes, emprestimo.id_exemplar, emprestimo.id_usuario)
    )
    conn.commit()
    emprestimo_id = cursor.fetchone()[0]
    print("Empréstimo adicionado com sucesso com ID:", emprestimo_id)

# Função para obter o ID do último empréstimo
def get_id_ultimo_emprestimo():
    cursor.execute("SELECT ID FROM Emprestimo ORDER BY ID DESC LIMIT 1;")
    ultimo_emprestimo = cursor.fetchone()
    if ultimo_emprestimo:
        return ultimo_emprestimo[0]
    return 0

# Função para obter um usuário por CPF
def get_usuario(CPF):
    cursor.execute("SELECT * FROM Usuario WHERE CPF = %s;", (CPF,))
    return cursor.fetchone()

# Função para obter empréstimos
def get_emprestimo(ISBN, exemplar):
    cursor.execute(
        """
        SELECT * FROM Emprestimo WHERE isbn_livro = %s AND id_exemplar = %s;
        """, 
        (ISBN, exemplar)
    )
    return cursor.fetchone()

# Função para atualizar empréstimo
def atualizar_emprestimo(id_emprestimo, data_devolucao, multa, renovacoes):
    cursor.execute(
        """
        UPDATE Emprestimo
        SET data_dev = %s, multa = %s, renovacoes = %s
        WHERE ID = %s;
        """,
        (data_devolucao, multa, renovacoes, id_emprestimo)
    )
    conn.commit()
    print("Empréstimo atualizado com sucesso!")

# Função para obter coleção do livro
def get_colecao(ISBN):
    cursor.execute(
        """
        SELECT id_colecao FROM Livro WHERE ISBN = %s;
        """,
        (ISBN,)
    )
    colecao = cursor.fetchone()
    return colecao[0] if colecao else None

# Função para apagar empréstimo do usuário
def apagar_emprestimo_usuario(CPF, emprestimo_id, multa):
    cursor.execute(
        """
        DELETE FROM Emprestimo
        WHERE id = %s AND id_usuario = (SELECT id FROM Usuario WHERE CPF = %s);
        """,
        (emprestimo_id, CPF)
    )
    conn.commit()
    print("Empréstimo apagado com sucesso!")

# Função para obter todos os empréstimos
def get_todos_emprestimos():
    cursor.execute("SELECT * FROM Emprestimo;")
    return cursor.fetchall()

# Função para atualizar o empréstimo no usuário
def atualizar_emprestimo_em_usuario(CPF, id_emprestimo, renovacoes, Fim):
    cursor.execute(
        """
        UPDATE Usuario
        SET renovacoes = %s, Fim = %s
        WHERE CPF = %s AND EXISTS (
            SELECT 1 FROM Emprestimo WHERE id = %s AND id_usuario = Usuario.id
        );
        """, 
        (renovacoes, Fim, CPF, id_emprestimo)
    )
    conn.commit()
    print("Empréstimo do usuário atualizado com sucesso!")
