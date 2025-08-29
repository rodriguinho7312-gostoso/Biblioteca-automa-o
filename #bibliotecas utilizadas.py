#bibliotecas utilizadas

import tkinter as tk
from tkinter import messagebox
import datetime as dt
import sqlite3 as sql
import smtplib as sm
from email.mime.text import MIMEText as mt
import customtkinter as ctk
# a biblioteca baixada foi customtkinter, mas pode ser substituido pelo tkinter 👍
#para instalar as bibliotecas utilize o pip install nomedabiblioteca




#sistema de ficha
janela = ctk.CTk()
janela.title('Sistema de ficha do aluno')
janela.geometry('1280x720')
ctk.set_appearance_mode('white')
ctk.set_default_color_theme('green')
ctk.CTkLabel(janela, text = "Cadastro", font = ("Time News Roman",32)).pack()
ctk.CTkLabel(janela, text = "Nome: ", font = ("Time News Roman",20)).pack()
nome = ctk.CTkEntry(janela, font = ("Time News Roman", 20))
nome.pack()
ctk.CTkLabel(janela, text = "Turma: ", font = ("Time News Roman",20)).pack()
turma = ctk.CTkEntry(janela, font = ("Time News Roman", 20))
turma.pack()
ctk.CTkLabel(janela, text = "idade: ", font = ("Time News Roman",20)).pack()
idade = ctk.CTkEntry(janela, font = ("Time News Roman", 20))
idade.pack()

ctk.CTkLabel(janela, text = "CPF: ", font = ("Time News Roman",20)).pack()
cpf = ctk.CTkEntry(janela, font = ("Time News Roman", 20))
cpf.pack()

banco = sql.connect('ficha_aluno.db')
cursor = banco.cursor()
banco.execute('''CREATE TABLE IF NOT EXISTS ALUNOS
              (id_aluno integer primary key,
              nome text not null,
              turma text not null,
              idade integer not null,
              cpf text not null);''')

def cadastro():
    global nome_aluno, turma_aluno, idade_aluno, cpf_aluno
    nome_aluno = nome.get()
    turma_aluno = turma.get()
    idade_aluno = idade.get()
    cpf_aluno = cpf.get()
    if not nome_aluno or not turma_aluno or not idade_aluno or not cpf_aluno:
        messagebox.showerror("Erro", "Preencha todos os campos")
        return

    if len(str(cpf_aluno)) != 11 or not cpf_aluno.isdigit():
        messagebox.showerror("Erro", "CPF inválido")
        return

    if len(idade_aluno)>2 or len(idade_aluno)<1 or idade_aluno.isalpha():
        messagebox.showerror("Erro", "Idade inválida")

        return

    banco.execute('''insert into ALUNOS (nome, turma, idade, cpf)
              values (?,?,?,?) ''',(nome_aluno, turma_aluno, int(idade_aluno), cpf_aluno))

    banco.commit()
    nome.delete(0, 'end')
    turma.delete(0, 'end')
    idade.delete(0, 'end')
    cpf.delete(0, 'end')


    messagebox.showinfo("Deu certo meu lindo", "Ficha salva ")
    janela.withdraw()
    abrir_janela2()
botao_salvar = ctk.CTkButton(janela, text="Salvar ficha do aluno", command=cadastro, width=200, height=40)
botao_salvar.pack(pady=20)


def abrir_janela2():
    janela2 = ctk.CTkToplevel()
    janela2.geometry("1280x720")
    janela2.title("Fichas dos alunos")
    janela2.configure(bg="white")

    ctk.CTkLabel(janela2, text="Alunos cadastrados", font=("Time News Roman", 28)).pack(pady=20)


    lista_alunos = ctk.CTkTextbox(janela2, width=800, height=500, font=("Time News Roman", 16))
    lista_alunos.pack(pady=20)

    cursor.execute("SELECT nome, turma, idade, cpf FROM ALUNOS")
    alunos = cursor.fetchall()

    if not alunos:
        lista_alunos.insert("end", "Nenhum aluno cadastrado ainda.")

    else:
        for aluno in alunos:
            nome, turma, idade, cpf = aluno
            lista_alunos.insert("end", f"Nome: {nome}\nTurma: {turma}\nIdade: {idade}\nCPF: {cpf}\n\n")
            btn = ctk.CTkButton (
                janela2,
                text=nome,
                command=lambda id_aluno=id_aluno: mostrar_ficha(id_aluno) )
            btn.pack(pady=5)

    lista_alunos.configure(state="disabled")
    abrir_janela3()

    def abrir_janela3():
        janela3 = ctk.CTkToplevel()
        janela3.geometry("1280x720")
        janela3.title("Ficha detalhada do aluno")
        janela3.configure(bg="white")

        ctk.CTkLabel(janela3, text="Ficha detalhada do aluno", font=("Time News Roman", 20)).pack()










janela.mainloop()

banco.close()
