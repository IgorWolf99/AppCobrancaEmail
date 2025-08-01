from tkinter import *
import funcoes as func
import os
import pandas as pd
from tabela_view import criarTreeview
from login import telaLogin

if telaLogin():
    print("Login aceito. Abrindo sistema...")
    
    # region Funções dos botões

    def atualizaTabela(df):
        global tree
        for widget in frame_tabela.winfo_children():
            widget.destroy()

        colunas = list(df.columns)
        tree = criarTreeview(frame_tabela, [], colunas)
        for linha in df.values.tolist():
            tree.insert("", "end", values=linha)

    def btnPesquisar():
        global tabela, nome_arquivo
        dados, caminho = func.pesquisarArquivo()
        if dados is not None:
            tabela = dados
            nome_arquivo = os.path.basename(caminho)
            nome_arquivo_var.set(f"Arquivo aberto: {nome_arquivo}")
            qtd_result.set(f"Resultados: {len(dados)}")
            atualizaTabela(dados)

    def nfsVencidas():
        dados = func.pagamentosVencidos(tabela)
        func.abrirJanelaEmailVencidos(janela, dados, tabela)
        qtd_result.set(f"Resultados: {len(dados)}")
        atualizaTabela(dados)

    def btnTodosItens():
        dados = func.todosDados(tabela)
        qtd_result.set(f"Resultados: {len(dados)}")
        atualizaTabela(dados)

    def btnQtdNfsPagas():
        dados = func.qtdNfsPagas(tabela)
        qtd_result.set(f"Resultados: {len(dados)}")
        atualizaTabela(dados)

    def atualizarNfsEmAberto():
        dados = func.nfsEmAberto(tabela)
        qtd_result.set(f"Resultados: {len(dados)}")
        atualizaTabela(dados)

    def btnSair():
        janela.destroy()

    def criarBotao(texto, comando):
        return Button(
            frame_botoes,
            text=texto,
            command=comando,
            width=50,
            height=1,
            bg="#4A90E2",
            fg="white",
            activebackground="#357ABD",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="raised",
            bd=2,
            cursor="hand2"
        )

    # endregion

    # region Janela e container principal
    janela = Tk()
    janela.title("Sistema de Automação de Cobranças")
    janela.geometry("900x800")

    container = Frame(janela, borderwidth=5, relief="groove")
    container.pack(padx=20, pady=20, fill="both", expand=True)

    for i in range(10):
        container.grid_columnconfigure(i, weight=1)

    tabela = pd.DataFrame()
    # endregion

    # region Título
    titulo = Label(container, text="SISTEMA AUTOMAÇÃO DE COBRANÇAS",
                font=("Arial Black", 14, "bold"))
    titulo.grid(column=0, row=0, columnspan=10, sticky='nsew', pady=10)
    # endregion

    # region Botão de seleção de arquivo
    btn_pesquisar = Button(container, text="📂 Procurar Arquivo Excel",
                        command=btnPesquisar,
                        bg="#4A90E2",
                        fg="white",
                        activebackground="#357ABD",
                        font=("Segoe UI", 10, "bold"),
                        width=50)
    btn_pesquisar.grid(column=0, row=1, columnspan=10, pady=10, sticky='n')
    # endregion

    # region Ações disponíveis
    frame_acoes_area = Frame(container, borderwidth=2,
                            relief="groove", padx=15, pady=10, bg="#f0f4f7")
    frame_acoes_area.grid(column=0, row=4, columnspan=10,
                        sticky='ew', pady=(10, 0), padx=5)

    lbl_acoes = Label(frame_acoes_area, text="AÇÕES DISPONÍVEIS",
                    font=("Segoe UI", 11, "bold"), bg="#f0f4f7")
    lbl_acoes.pack()

    frame_botoes = Frame(frame_acoes_area, bg="#f0f4f7")
    frame_botoes.pack(anchor='center')

    criarBotao("Todas NFs", btnTodosItens).pack(pady=5)
    criarBotao("Cobrar NFs Vencidas", nfsVencidas).pack(pady=5)
    criarBotao("NFs em aberto", atualizarNfsEmAberto).pack(pady=5)
    criarBotao("NFs Pagas", btnQtdNfsPagas).pack(pady=5)
    criarBotao("Sair da Aplicação", btnSair).pack(pady=5)
    # endregion

    # region Resultados
    Label(container, text="RESULTADOS",
        font=("Segoe UI", 11, "bold"), bg="#f0f4f7").grid(
        column=0, row=7, columnspan=10, sticky='n', pady=(20, 0))

    nome_arquivo_var = StringVar()
    nome_arquivo_var.set("Arquivo aberto: (nenhum)")
    lbl_excel2 = Label(container, textvariable=nome_arquivo_var,
                    font=("Segoe UI", 11))
    lbl_excel2.grid(column=0, row=8, columnspan=10, pady=(10, 10), sticky='n')

    qtd_result = StringVar()
    qtd_result.set("Resultados: (nenhum)")
    lbl_result = Label(container, textvariable=qtd_result,
                    font=("Segoe UI", 11))
    lbl_result.grid(column=0, row=8, pady=(10, 10), sticky='n')

    # endregion

    # region Tabela
    frame_tabela = Frame(container)
    frame_tabela.grid(column=0, row=10, rowspan=5, padx=10,
                    columnspan=10, sticky='nsew')

    colunas = list(tabela.columns)
    tree = criarTreeview(frame_tabela, [], colunas)
    # endregion

    janela.mainloop()

else:
    print("Login inválido. Encerrando.")


