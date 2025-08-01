import tkinter as tk
from tkinter import ttk


def criarTreeview(frame, dados, colunas):
    tree = ttk.Treeview(frame, columns=colunas, show='headings')
    
    # Coluna Cabeçalho
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120)
        
    # Linha de dados uma a uma
    for linha in dados:
        tree.insert("","end", values=linha)
        
    # Organizar o Treeview para ocupar todo o espaço disponível no frame
    tree.pack(fill="both", expand=True)
    
    return tree
