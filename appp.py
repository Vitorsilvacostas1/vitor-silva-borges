import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect('agenda_db.sqlite')

# Função para criar a tabela de clientes
def create_table():
    conn = connect_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS Cliente (
        Numero INTEGER PRIMARY KEY,
        Nome TEXT NOT NULL,
        Endereco TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Função para adicionar um cliente
def add_cliente():
    try:
        numero = int(entry_numero.get())
        nome = entry_nome.get()
        endereco = entry_endereco.get()

        # Verificar se todos os campos estão preenchidos
        if not nome or not endereco:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        conn = connect_db()
        conn.execute('INSERT INTO Cliente (Numero, Nome, Endereco) VALUES (?, ?, ?)', (numero, nome, endereco))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
        clear_entries()
        load_clientes()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "O número do cliente deve ser único.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para carregar os clientes na tabela
def load_clientes():
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.execute('SELECT * FROM Cliente')
    for row in cursor:
        tree.insert('', 'end', values=row)
    conn.close()

# Função para consultar um cliente pelo número
def consult_cliente():
    try:
        numero = int(entry_numero.get())
        conn = connect_db()
        cursor = conn.execute('SELECT * FROM Cliente WHERE Numero = ?', (numero,))
        client = cursor.fetchone()
        conn.close()

        if client:
            # Preenche os campos com os dados do cliente encontrado
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, client[1])  # Nome
            entry_endereco.delete(0, tk.END)
            entry_endereco.insert(0, client[2])  # Endereço
        else:
            messagebox.showwarning("Atenção", "Cliente não encontrado.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para editar um cliente selecionado
def edit_cliente():
    try:
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um cliente para editar.")
            return

        item = tree.item(selected_item)
        numero = item['values'][0]  # Pega o número do cliente selecionado
        nome = entry_nome.get()
        endereco = entry_endereco.get()

        # Verificar se todos os campos estão preenchidos
        if not nome or not endereco:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        conn = connect_db()
        conn.execute('UPDATE Cliente SET Nome = ?, Endereco = ? WHERE Numero = ?', (nome, endereco, numero))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Cliente alterado com sucesso!")
        clear_entries()
        load_clientes()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para excluir um cliente selecionado
def delete_cliente():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Atenção", "Selecione um cliente para excluir.")
        return

    item = tree.item(selected_item)
    numero = item['values'][0]

    conn = connect_db()
    conn.execute('DELETE FROM Cliente WHERE Numero = ?', (numero,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
    load_clientes()

# Função para limpar os campos de entrada
def clear_entries():
    entry_numero.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)

# Configuração da interface do Tkinter
app = tk.Tk()
app.title("Gerenciamento de Clientes")

# Criação da tabela de clientes no banco de dados
create_table()

# Frame para entrada de dados
frame_entry = tk.Frame(app)
frame_entry.pack(pady=10)

label_numero = tk.Label(frame_entry, text="Número:")
label_numero.grid(row=0, column=0)
entry_numero = tk.Entry(frame_entry)
entry_numero.grid(row=0, column=1)

label_nome = tk.Label(frame_entry, text="Nome:")
label_nome.grid(row=1, column=0)
entry_nome = tk.Entry(frame_entry)
entry_nome.grid(row=1, column=1)

label_endereco = tk.Label(frame_entry, text="Endereço:")
label_endereco.grid(row=2, column=0)
entry_endereco = tk.Entry(frame_entry)
entry_endereco.grid(row=2, column=1)

# Botões para ações
btn_add = tk.Button(app, text="Adicionar", command=add_cliente)
btn_add.pack(pady=5)

btn_consult = tk.Button(app, text="Consultar", command=consult_cliente)
btn_consult.pack(pady=5)

btn_edit = tk.Button(app, text="Alterar", command=edit_cliente)
btn_edit.pack(pady=5)

btn_delete = tk.Button(app, text="Excluir", command=delete_cliente)
btn_delete.pack(pady=5)

# Tabela para exibir os clientes
columns = ('Numero', 'Nome', 'Endereco')
tree = ttk.Treeview(app, columns=columns, show='headings')
tree.heading('Numero', text='Número')
tree.heading('Nome', text='Nome')
tree.heading('Endereco', text='Endereço')
tree.pack(pady=10)

# Carregar clientes existentes
load_clientes()

# Iniciar a aplicação
app.mainloop()
