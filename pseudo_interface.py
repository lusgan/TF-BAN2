import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import biblioteca_camada_logica
import DAO
import datetime
from datetime import datetime,timedelta

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("400x500")
        
        # Cria o menu principal
        self.create_main_menu()
    
    def create_main_menu(self):
        self.clear_window()
        
        tk.Label(self.root, text="Menu Principal", font=("Arial", 16)).pack(pady=10)
        buttons = [
            ("Cadastrar Coleção", self.cadastrar_colecao),  # Adicionando o botão para Coleção
            ("Cadastrar Bibliotecário", self.cadastrar_bibliotecario),
            ("Cadastrar Assistente", self.cadastrar_assistente),
            ("Cadastrar Usuário", self.cadastrar_usuario),
            ("Cadastrar Livro", self.cadastrar_livro),
            ("Cadastrar Exemplar", self.cadastrar_exemplar),
            ("Realizar Empréstimo", self.realizar_emprestimo),
            ("Localizar Exemplar", self.localizar_exemplar),
            ("Devolução de Exemplar", self.devolucao_exemplar),
            ("Renovar Empréstimo", self.renovar_emprestimo),
            ("Comandos do Desenvolvedor", self.menu_do_desenvolvedor),
            ("Sair", self.root.destroy)
        ]
        
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command, width=30).pack(pady=5)

    
    def cadastrar_bibliotecario(self):
        self.clear_window()
        tk.Label(self.root, text="Cadastrar Bibliotecário", font=("Arial", 16)).pack(pady=10)
        
        fields = ["CPF", "Nome", "Rua", "Cidade", "CEP", "Telefone", "Endereço"]
        entries = {}
        
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field] = entry
        
        def submit():
            bibliotechman = biblioteca_camada_logica.Bibliotecario(
                entries["CPF"].get(), entries["Nome"].get(), entries["Rua"].get(), 
                entries["Cidade"].get(), entries["CEP"].get(), entries["Telefone"].get(), entries["Endereço"].get()
            )
            DAO.cadastrar_bibliotecario(bibliotechman)
            messagebox.showinfo("Sucesso", "Bibliotecário cadastrado com sucesso!")
            self.create_main_menu()
        
        tk.Button(self.root, text="Cadastrar", command=submit).pack(pady=20)
    
    def cadastrar_assistente(self):
        self.clear_window()
        tk.Label(self.root, text="Cadastrar Assistente", font=("Arial", 16)).pack(pady=10)
        
        fields = ["CPF", "Nome", "Rua", "Cidade", "CEP", "Telefone", "Endereço", "Supervisores (CPF separados por vírgula)"]
        entries = {}
        
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field] = entry
        
        def submit():
            supervisores = entries["Supervisores (CPF separados por vírgula)"].get().split(",")
            assistente = biblioteca_camada_logica.Assistente(
                entries["CPF"].get(), entries["Nome"].get(), entries["Rua"].get(),
                entries["Cidade"].get(), entries["CEP"].get(), entries["Telefone"].get(), entries["Endereço"].get(), supervisores
            )
            DAO.cadastrar_assistente(assistente)
            messagebox.showinfo("Sucesso", "Assistente cadastrado com sucesso!")
            self.create_main_menu()
        
        tk.Button(self.root, text="Cadastrar", command=submit).pack(pady=20)

    def cadastrar_usuario(self):
        self.clear_window()
        tk.Label(self.root, text="Cadastrar Usuário", font=("Arial", 16)).pack(pady=10)
        
        fields = ["Nome", "Rua", "Cidade", "CPF", "CEP", "Telefone", "Endereço"]
        entries = {}
        
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field] = entry
        
        tk.Label(self.root, text="Categoria").pack()
        categoria_var = tk.IntVar()
        categorias = [
            ("Aluno de graduação", 1),
            ("Aluno de pós-graduação", 2),
            ("Professor", 3),
            ("Professor de pós-graduação", 4)
        ]
        
        for text, value in categorias:
            tk.Radiobutton(self.root, text=text, variable=categoria_var, value=value).pack(anchor="w")
        
        def submit():
            
            categoria_id = categoria_var.get()
            usuario = biblioteca_camada_logica.Usuario(
                entries["Nome"].get(), entries["Rua"].get(), entries["Cidade"].get(), 
                entries["CPF"].get(), entries["CEP"].get(), entries["Telefone"].get(), 
                entries["Endereço"].get(), 0, categoria_id
            )
            DAO.cadastrar_usuario(usuario)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.create_main_menu()
        
        tk.Button(self.root, text="Cadastrar", command=submit).pack(pady=20)
    
    def cadastrar_livro(self):
        self.clear_window()
        tk.Label(self.root, text="Cadastrar Livro", font=("Arial", 16)).pack(pady=10)
        
        fields = ["Título", "Autores (separados por vírgula)", "isbn", "Editora", "id_coleção", "id_bibliotecario"]
        entries = {}
        
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field] = entry
        
        def submit():
            autores = entries["Autores (separados por vírgula)"].get().split(",")
            livro = biblioteca_camada_logica.Livro(
                entries["isbn"].get(), entries["Título"].get(), 
                entries["Editora"].get(), autores, entries["id_coleção"].get(), entries["id_bibliotecario"].get()
            )
            DAO.cadastrar_livro(livro)
            messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
            self.create_main_menu()
        
        tk.Button(self.root, text="Cadastrar", command=submit).pack(pady=20)
    
    def cadastrar_exemplar(self):
        self.clear_window()
        tk.Label(self.root, text="Cadastrar Exemplar", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self.root, text="isbn").pack()
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack()
        
        
        tk.Label(self.root, text="id_bibliotecario").pack()
        id_bibliotecario_entry = tk.Entry(self.root)
        id_bibliotecario_entry.pack()
        
        tk.Label(self.root, text="Status").pack()
        status_var = tk.StringVar(value="Disponível")
        tk.Radiobutton(self.root, text="Disponível", variable=status_var, value="Disponível").pack(anchor="w")
        tk.Radiobutton(self.root, text="Indisponível", variable=status_var, value="Indisponível").pack(anchor="w")
    
        
        def submit():
            if not DAO.verificar_isbn(isbn_entry.get()):
                messagebox.showwarning("Erro", "isbn não encontrado no banco de dados!")
                return
            
            
            exemplar = biblioteca_camada_logica.Exemplar(isbn_entry.get(), status_var.get(),int(id_bibliotecario_entry.get()))
            DAO.cadastrar_exemplar(exemplar)
            messagebox.showinfo("Sucesso", "Exemplar cadastrado com sucesso!")
            self.create_main_menu()
        
        tk.Button(self.root, text="Cadastrar", command=submit).pack(pady=20)
    
    
    
    def realizar_emprestimo(self):
        self.clear_window()
        tk.Label(self.root, text="Realizar Empréstimo", font=("Arial", 16)).pack(pady=10)
    
        # Campos de entrada para realizar o empréstimo
        tk.Label(self.root, text="isbn").pack()
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack()
    
        tk.Label(self.root, text="id do Exemplar").pack()
        exemplar_entry = tk.Entry(self.root)
        exemplar_entry.pack()
    
        tk.Label(self.root, text="CPF do Usuário").pack()
        cpf_entry = tk.Entry(self.root)
        cpf_entry.pack()
    
        tk.Label(self.root, text="Data hoje (DD-MM-YYYY)").pack()
        hoje_entry = tk.Entry(self.root)
        hoje_entry.pack()
    
        def submit():
            try:
                # Verificação dos dados do usuário e exemplar
                isbn = isbn_entry.get()
                id_exemplar = int(exemplar_entry.get())
                CPF = cpf_entry.get()
    
                usuario = DAO.get_usuario(CPF)
                if not usuario:
                    messagebox.showwarning("Erro", "Usuário não encontrado!")
                    return
    
                # Supondo que a tupla retornada tenha a categoria_id na posição 9
                categoria_id = usuario[9]  # Acessa o id da categoria da tupla
                qtd_dias = {
                    1: 15,  # Aluno de graduação
                    2: 30,  # Aluno de pós-graduação
                    3: 30,  # Professor
                    4: 90   # Professor de pós-graduação
                }.get(categoria_id, 15)  # Valor padrão é 15 se o id não for encontrado
    
              
                data_hoje_str = hoje_entry.get().strip()  
                data_hoje = datetime.strptime(data_hoje_str, "%d-%m-%Y").date()
                
                fim = data_hoje + timedelta(days=qtd_dias)  # Utilizando qtd_dias em vez de valor fixo 15
                usuario_id = usuario[0]
                

                emprestimo = biblioteca_camada_logica.Emprestimo(data_hoje, fim, id_exemplar, usuario_id)
                biblioteca_camada_logica.emprestar_livro(emprestimo, data_hoje)
    
                messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso!")
                self.create_main_menu()
    
            except ValueError as e:
                messagebox.showerror("Erro", f"{e}.")

            
        tk.Button(self.root, text="Realizar Empréstimo", command=submit).pack(pady=20)
    
    
    
    
    def localizar_exemplar(self):
        self.clear_window()
        tk.Label(self.root, text="Localizar Exemplar", font=("Arial", 16)).pack(pady=10)
        
        # Campos de entrada para localizar o exemplar
        tk.Label(self.root, text="isbn").pack()
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack()
        
        tk.Label(self.root, text="Número do Exemplar").pack()
        exemplar_entry = tk.Entry(self.root)
        exemplar_entry.pack()
        
        def buscar_exemplar():
            try:
                isbn = isbn_entry.get()
                numero = int(exemplar_entry.get())
                
                # Usa a função DAO.get_exemplar para localizar o exemplar
                exemplar = DAO.get_exemplar(isbn, numero)
                if exemplar:
                    messagebox.showinfo("Exemplar Encontrado", f"Exemplar: {exemplar}")
                else:
                    messagebox.showwarning("Não Encontrado", "Exemplar não encontrado!")
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um número válido para o exemplar.")
        
        tk.Button(self.root, text="Buscar Exemplar", command=buscar_exemplar).pack(pady=20)
        tk.Button(self.root, text="Voltar", command=self.create_main_menu).pack(pady=10)

    def devolucao_exemplar(self):
        self.clear_window()
        tk.Label(self.root, text="Devolução de Exemplar", font=("Arial", 16)).pack(pady=10)
        
        # Campos de entrada para devolução de exemplar
        tk.Label(self.root, text="isbn").pack()
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack()
        
        tk.Label(self.root, text="Número do Exemplar").pack()
        exemplar_entry = tk.Entry(self.root)
        exemplar_entry.pack()
        
        tk.Label(self.root, text="Data de Devolução (DD-MM-YYYY)").pack()
        data_devolucao_entry = tk.Entry(self.root)
        data_devolucao_entry.pack()
        
        def devolver():
            try:
                isbn = isbn_entry.get()
                num_exemplar = int(exemplar_entry.get())
                data_devolucao_str = data_devolucao_entry.get()
                data_devolucao = datetime.strptime(data_devolucao_str, "%d-%m-%Y").date()
                
                # Função para processar a devolução
                biblioteca_camada_logica.devolver_livro(num_exemplar, data_devolucao)
                messagebox.showinfo("Sucesso", "Devolução realizada com sucesso!")
                self.create_main_menu()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira dados válidos.")
        
        tk.Button(self.root, text="Devolver Exemplar", command=devolver).pack(pady=20)
        tk.Button(self.root, text="Voltar", command=self.create_main_menu).pack(pady=10)

    
    

    def renovar_emprestimo(self):
        self.clear_window()
        tk.Label(self.root, text="Renovar Empréstimo", font=("Arial", 16)).pack(pady=10)
        
        # Campos de entrada para renovação de empréstimo
        tk.Label(self.root, text="isbn").pack()
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack()
        
        tk.Label(self.root, text="Número do Exemplar").pack()
        exemplar_entry = tk.Entry(self.root)
        exemplar_entry.pack()
        
        tk.Label(self.root, text="Data de Hoje (DD-MM-YYYY)").pack()
        data_hoje_entry = tk.Entry(self.root)
        data_hoje_entry.pack()
        
        def renovar():
            try:
                isbn = isbn_entry.get()
                num_exemplar = int(exemplar_entry.get())
                data_hoje_str = data_hoje_entry.get()
                data_hoje = datetime.strptime(data_hoje_str, "%d-%m-%Y").date()
                
                # Verificar renovação
                emprestimo = DAO.get_emprestimo_nao_devolvido(num_exemplar)
                if not emprestimo:
                    messagebox.showwarning("Erro", "Empréstimo não encontrado!")
                    return
    
                # Verifica as condições para renovação
                if data_hoje > emprestimo[2]:
                    messagebox.showwarning("Erro", "Livro atrasado, não pode ser renovado.")
                    return
                if emprestimo[4] >= 3:
                    messagebox.showwarning("Erro", "Limite de renovações atingido.")
                    return
                if emprestimo[3]:
                    messagebox.showwarning("Erro", "Livro já foi devolvido, não é possível renovar.")
                    return
                
                # Processa a renovação
                biblioteca_camada_logica.renovar_emprestimo(isbn, num_exemplar, data_hoje)
                messagebox.showinfo("Sucesso", "Renovação realizada com sucesso!")
                self.create_main_menu()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira dados válidos.")
        
        tk.Button(self.root, text="Renovar Empréstimo", command=renovar).pack(pady=20)
        tk.Button(self.root, text="Voltar", command=self.create_main_menu).pack(pady=10)
    
    
    def cadastrar_colecao(self):
        self.clear_window()
        tk.Label(self.root, text="Cadastrar Coleção", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self.root, text="Nome da Coleção").pack()
        nome_entry = tk.Entry(self.root)
        nome_entry.pack()
        
        def submit():
            nome = nome_entry.get()
            if not nome:
                messagebox.showwarning("Erro", "O nome da coleção não pode estar vazio.")
                return
            
            colecao = biblioteca_camada_logica.Colecao(nome)
            id_colecao = DAO.cadastrar_colecao(colecao)
            colecao.id = id_colecao
            
            messagebox.showinfo("Sucesso", f"Coleção '{colecao.nome}' cadastrada com sucesso!")
            self.create_main_menu()
        
        tk.Button(self.root, text="Cadastrar", command=submit).pack(pady=20)

    
    def menu_do_desenvolvedor(self):
        self.clear_window()
        tk.Label(self.root, text="Comandos do Desenvolvedor", font=("Arial", 16)).pack(pady=10)
        
        buttons = [
            ("Visualizar Bibliotecários", self.visualizar_bibliotecarios),
            ("Visualizar Assistentes", self.visualizar_assistentes),
            ("Visualizar Usuários", self.visualizar_usuarios),
            ("Visualizar Livros", self.visualizar_livros),
            ("Visualizar Exemplares", self.visualizar_exemplares),
            ("Visualizar Empréstimos", self.visualizar_todos_emprestimos),
            ("Voltar", self.create_main_menu)
        ]
        
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command, width=30).pack(pady=5)

    def visualizar_bibliotecarios(self):
        data, columns = DAO.get_bibliotecarios()
        self.display_data("Bibliotecários", data, columns)

    def visualizar_assistentes(self):
        data, columns = DAO.get_assistentes()
        self.display_data("Assistentes", data, columns)
    
    def visualizar_usuarios(self):
        data, columns = DAO.get_usuarios()
        self.display_data("Usuários", data, columns)
    
    def visualizar_livros(self):
        data, columns = DAO.get_livros()
        self.display_data("Livros", data, columns)
    
    def visualizar_exemplares(self, isbn):
        data, columns = DAO.get_exemplares(isbn)
        self.display_data("Exemplares", data, columns)
    
    def visualizar_emprestimo(self, isbn, exemplar):
        data, columns = DAO.get_emprestimo(isbn, exemplar)
        if data:
            # Se houver dados, exibe a linha com as colunas correspondentes
            self.display_data("Empréstimo", [data], columns)
        else:
            # Se não houver dados, exibe uma mensagem indicando que não foi encontrado
            tk.Label(self.root, text="Empréstimo não encontrado", font=("Arial", 12)).pack(pady=10)
    
    def visualizar_todos_emprestimos(self):
        data, columns = DAO.get_todos_emprestimos()
        self.display_data("Todos os Empréstimos", data, columns)


    
    def display_data(self, title, data, columns):
        self.clear_window()
        
        tk.Label(self.root, text=title, font=("Arial", 16)).pack(pady=10)
        
        # Verifica se há dados a serem exibidos
        if not data:
            tk.Label(self.root, text="Nenhum dado disponível", font=("Arial", 12)).pack(pady=10)
            return
        
        # Cria o Treeview (tabela)
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        # Define as colunas e os cabeçalhos
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        # Insere cada item na tabela
        for item in data:
            tree.insert("", tk.END, values=item)  # Os valores são as tuplas retornadas pela consulta
        
        tree.pack(expand=True, fill="both", padx=10, pady=10)
    
        # Botão para voltar
        tk.Button(self.root, text="Voltar", command=self.menu_do_desenvolvedor).pack(pady=10)



    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Inicialização da interface gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
