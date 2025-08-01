import tkinter as tk
from tkinter import messagebox
import hashlib

def telaLogin():
    SALT = "saltsenhaapp123"
    SENHA_HASH = "4dff86630ab30d3eaf115de0303db17a7de1334b12535a39b80a53603b9c9bba"  # senha: testeapp123

    def validar_login():
        input_senha = entry_senha.get()
        senha_hash = hashlib.sha256((input_senha + SALT).encode()).hexdigest()

        if senha_hash == SENHA_HASH:
            autenticado.set(True)
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Senha incorreta.")

    # Cria janela
    janela = tk.Tk()
    janela.title("Login")
    largura, altura = 400, 250

    # Centralizar na tela
    screen_largura = janela.winfo_screenwidth()
    screen_altura = janela.winfo_screenheight()
    x = int((screen_largura / 2) - (largura / 2))
    y = int((screen_altura / 2) - (altura / 2))
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

    janela.configure(bg="#f0f4f8")
    janela.resizable(False, False)

    autenticado = tk.BooleanVar(value=False)

    # Titulo
    tk.Label(janela, text="Bem-vindo!", font=("Segoe UI", 14, "bold"), bg="#f0f4f8").pack(pady=(20, 5))

    # Campo de seenha
    frame_senha = tk.Frame(janela, bg="#f0f4f8")
    frame_senha.pack(pady=(10, 5))

    tk.Label(frame_senha, text="Senha:", font=("Segoe UI", 11), bg="#f0f4f8").pack(anchor="w")
    entry_senha = tk.Entry(frame_senha, font=("Segoe UI", 11), show="*", width=30)
    entry_senha.pack()

    # Botao de login
    tk.Button(janela, text="Entrar", command=validar_login,
              bg="#4A90E2", fg="white", font=("Segoe UI", 11, "bold"),
              activebackground="#357ABD", activeforeground="white",
              relief="raised", bd=2, width=20, height=1).pack(pady=25)

    janela.mainloop()

    return autenticado.get()