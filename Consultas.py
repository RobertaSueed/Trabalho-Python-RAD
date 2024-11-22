import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import sqlite3

# Conexão ao banco de dados
conexao = sqlite3.connect("consultas.db")
cursor = conexao.cursor()

# Criar tabela de pacientes, se ainda não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    telefone TEXT,
    data_nascimento TEXT,
    cep TEXT,
    estado TEXT,
    cidade TEXT,
    bairro TEXT,
    cpf TEXT,
    email TEXT,
    senha TEXT
)
''')

# Função para cadastrar o paciente
def cadastrar_paciente(nome, telefone, data_nascimento, cep, estado, cidade, bairro, cpf, email, senha):
    try:
        cursor.execute('''
        INSERT INTO pacientes (nome, telefone, data_nascimento, cep, estado, cidade, bairro, cpf, email, senha)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, telefone, data_nascimento, cep, estado, cidade, bairro, cpf, email, senha))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

# Função para abrir janela de cadastro
def abrir_janela_cadastrar():
    janela_cadastrar = Toplevel()
    janela_cadastrar.geometry('400x800')
    janela_cadastrar.title('Cadastrar Paciente')

    # Criar as labels e entries para os campos de cadastro
    labels_text = ["Nome", "Telefone", "Data de Nascimento (DD/MM/AAAA)", "CEP", "Estado", "Cidade", "Bairro", "CPF", "Email", "Senha", "Confirmar Senha"]
    entries = {}
    
    for i, label_text in enumerate(labels_text):
        tk.Label(janela_cadastrar, text=label_text, font=('Arial', 12, "bold")).pack(pady=5)
        entry = tk.Entry(janela_cadastrar, font=('Arial', 12, "bold"), show="*" if 'Senha' in label_text else "")
        entry.pack(pady=1)
        entries[label_text] = entry

    # Função do botão de cadastrar
    def on_cadastrar():
        dados = {label: entries[label].get() for label in labels_text}

        # Validação dos campos
        if all(dados.values()):
            if dados["Senha"] == dados["Confirmar Senha"]:
                cadastrar_paciente(*[dados[label] for label in labels_text[:-1]])  # Não envia "Confirmar Senha"
                janela_cadastrar.destroy()  # Fechar a janela após cadastro
            else:
                messagebox.showwarning("Erro", "As senhas não coincidem!")
        else:
            messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos.")

    # Botão de cadastrar
    btn_cadastrar = tk.Button(janela_cadastrar, text="Cadastrar", font=('Arial', 12, "bold"), bg="green", command=on_cadastrar)
    btn_cadastrar.pack(side="top", padx=20, pady=10)

# Função para verificar as credenciais
def verificar_login(cpf, senha):
    try:
        cursor.execute('''SELECT * FROM pacientes WHERE cpf = ? AND senha = ?''', (cpf, senha))
        paciente = cursor.fetchone()
        if paciente:
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            abrir_janela_marcacao()  # Abre a janela de marcação de agendamento  
        else:
            messagebox.showerror("Erro", "CPF ou senha incorretos!")
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao verificar login: {e}")

# Função para mostrar o formulário de login
def mostrar_login():
    janela_login = Toplevel()
    janela_login.geometry('200x200')
    janela_login.title('Login do Paciente')

  # Criar as labels e entries para os campos de login

    tk.Label(janela_login, text="CPF", font=('Arial', 12, "bold")).grid(row=0, column=1, padx=5, pady=5)
    cpf_entry = tk.Entry(janela_login, font=('Arial', 12))
    cpf_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(janela_login, text="Senha", font=('Arial', 12, "bold")).grid(row=2, column=1, padx=5, pady=5)
    senha_entry = tk.Entry(janela_login, font=('Arial', 12), show="*")
    senha_entry.grid(row=3, column=1, padx=5, pady=5)


    # Função do botão de login
    def on_login():
        cpf = cpf_entry.get()
        senha = senha_entry.get()

        if cpf and senha:
            verificar_login(cpf, senha)
            janela_login.destroy()  # Fecha a janela de login
            #abrir_janela_marcacao()  # Abre a janela de marcação de agendamento   
        else:
            messagebox.showwarning("Campos vazios", "Por favor, preencha o CPF e a senha.")

    # Botão de enviar
    btn_enviar = tk.Button(janela_login, text="Enviar", font=('Arial', 12, "bold"), bg="green", command=on_login)
    btn_enviar.grid(row=5, columnspan=2, pady=10)
     

# Função para abrir janela de agendamento
def abrir_janela_marcacao():    
    janela_marcacao = Toplevel()
    janela_marcacao.geometry('400x400')
    janela_marcacao.title('Marcação de Consultas e Exames')

    # Criar os campos para marcar consulta ou exame
    tk.Label(janela_marcacao, text="Selecione o tipo de agendamento", font=('Arial', 12, "bold")).pack(pady=10)

    # Combobox para selecionar o tipo de agendamento (Consulta ou Exame)
    tipos = ["Consulta", "Exame"]
    tipo_agendamento = ttk.Combobox(janela_marcacao, values=tipos, font=('Arial', 12))
    tipo_agendamento.pack(pady=10)

    # Combobox para selecionar a especialidade
    especialidades = ["Pediatria", "Cardiologista", "Dermatologista", "Ortopedia", "Clinica Médica", "Oftalmologia", "Ultrassonografia", "Endocrinologia", "Gatroenterologia/Endoscopia",  "Ginecologista", "Urologista"]
    tipo_area = ttk.Combobox(janela_marcacao, values=especialidades, font=('Arial', 12))
    tipo_area.pack(pady=10)

    # Campo para selecionar a data
    tk.Label(janela_marcacao, text="Data do Agendamento (DD/MM/AAAA)", font=('Arial', 12, "bold")).pack(pady=10)
    data_agendamento = tk.Entry(janela_marcacao, font=('Arial', 12))
    data_agendamento.pack(pady=10)

    # Campo para selecionar o horário
    tk.Label(janela_marcacao, text="Horário do Agendamento (00:00)", font=('Arial', 12, "bold")).pack(pady=10)
    horario_agendamento = tk.Entry(janela_marcacao, font=('Arial', 12))
    horario_agendamento.pack(pady=10)


    # Função do botão para marcar agendamento
    def on_marcar_agendamento():
        tipo = tipo_agendamento.get()
        area = tipo_area.get()
        data = data_agendamento.get()
        horario = horario_agendamento.get()

        if tipo and data:
            messagebox.showinfo("Sucesso", f"Agendamento de {tipo} marcado para {data} no horário das {horario}!")
            janela_marcacao.destroy()
        else:
            messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos.")

    # Botão para marcar o agendamento
    btn_marcar = tk.Button(janela_marcacao, text="Marcar Agendamento", font=('Arial', 12, "bold"), bg="green", command=on_marcar_agendamento)
    btn_marcar.pack(pady=10)


# Criando a janela principal
janela = tk.Tk()
janela.title("Gerenciador de Consultas Médicas")
janela.configure(bg="#F0F0F0")
janela.geometry("300x400")

# Configuração da imagem de fundo
image = tk.PhotoImage(file="img_c.png")
label_image = tk.Label(janela, image=image)
label_image.place(x=0, y=0, relwidth=1, relheight=1)  # A imagem ocupa todo o fundo da janela

# Criando o botão de cadastro
btn_cadastrar = tk.Button(janela, text="Cadastrar Paciente", font=('Arial', 12, "bold"), command=abrir_janela_cadastrar)
btn_cadastrar.place(relx=0.5, rely=0.4, anchor="center")  # Posiciona o botão no centro da janela

# Criando os botões de Login
btn_login = tk.Button(janela, text="Login", font=('Arial', 12, "bold"), command=mostrar_login)
btn_login.place(relx=0.5, rely=0.5, anchor="center")  # Posiciona o botão no centro da janela

#Teste
#btn_login = tk.Button(janela, text="Login", font=('Arial', 12), command=mostrar_login)
#btn_login.grid(row=1, column=1, padx=20, pady=20)

# Loop principal
janela.mainloop()




