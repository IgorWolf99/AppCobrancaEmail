from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
from functools import wraps

import pandas as pd
import datetime as dt
from email.message import EmailMessage
import smtplib

email = "X"  # Coloque aqui o E-mail do remetente
senhaapp = "X"    # Senha criada na conta google para usar em aplicações


def VerificarTabelaCarregada(func):   # Decorador Utilizado para fazer a verificação em cada função
    @wraps(func)
    def wrapper(*args, **kwargs):
        tabela = next((a for a in args if isinstance(a, pd.DataFrame)), None)
        if tabela is None or tabela.empty:
            messagebox.showerror("Erro", "Nenhuma planilha foi carregada.")
            return
        return func(*args, **kwargs)
    return wrapper

def dataFormatada(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tabela = next((a for a in args if isinstance(a, pd.DataFrame)), None)
        if tabela is not None and not tabela.empty:
            if "Data limite pagamento" in tabela.columns:
                # Converte para datetime.date
                tabela["Data limite pagamento"] = pd.to_datetime(
                    tabela["Data limite pagamento"], dayfirst=True, errors="coerce"
                ).dt.date

                # Converte para string no formato desejado
                tabela["Data limite pagamento"] = tabela["Data limite pagamento"].apply(
                    lambda d: d.strftime('%d/%m/%Y') if pd.notnull(d) else ""
                )
        return func(*args, **kwargs)
    return wrapper


@VerificarTabelaCarregada
def validarColunas(df):
    colunas_necessarias = ["CPF", "Valor em aberto", "Data limite pagamento", "Status", "NF", "E-mail"]
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            messagebox.showerror("Erro", f" Coluna obrigatória não encontrada: {coluna} ")
            return False
    return True

@dataFormatada  
def pesquisarArquivo():
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo Excel ou CSV",
        filetypes=[
            ("Planilhas Excel", "*.xlsx *.xls"),
            ("Arquivos CSV", "*.csv")
        ]
    )
    if caminho_arquivo:
        extensao = os.path.splitext(caminho_arquivo)[-1].lower()
        if extensao in ['.xlsx', '.xls']:
            tabela = pd.read_excel(caminho_arquivo)
        elif extensao == '.csv':
            tabela = pd.read_csv(caminho_arquivo, sep=';')
        else:
            messagebox.showerror("Erro", "Formato de arquivo não suportado.")
            return None, None
        if validarColunas(tabela):
            return tabela.sort_values(by="NF"), caminho_arquivo

    return None, None

@dataFormatada  
@VerificarTabelaCarregada
def pagamentosVencidos(tabela):
    dt_hoje = dt.datetime.now().date()  
    
    tabela["Data limite pagamento"] = pd.to_datetime(tabela["Data limite pagamento"], dayfirst=True).dt.date
    pag_vencidos= tabela.loc[
    (tabela["Data limite pagamento"] < dt_hoje) & (tabela["Status"] == "Em aberto") ]
    
    pag_vencidos.loc[:, "Data limite pagamento"] = pag_vencidos["Data limite pagamento"].apply(lambda d: d.strftime('%d/%m/%Y'))
   
    return pag_vencidos.sort_values(by="NF")
  
@dataFormatada  
@VerificarTabelaCarregada    
def todosDados(tabela):
    return tabela.sort_values(by="NF")

@dataFormatada      
@VerificarTabelaCarregada
def nfsEmAberto(tabela):
    nfs_em_aberto = tabela.loc[tabela['Status'] == "Em aberto"]
    
    nfs_em_aberto = nfs_em_aberto.sort_values(by="NF")
    cont = len(nfs_em_aberto)
    
    print('def qtdNfsEmAberto(): \n', nfs_em_aberto)
    print("\033[32mValores encontrados: ", cont, "\033[0m")
    return nfs_em_aberto

@dataFormatada  
@VerificarTabelaCarregada
def qtdNfsPagas(tabela):
    nfs_em_aberto = tabela.loc[tabela['Status'] == "Pago"]
    
    nfs_em_aberto = nfs_em_aberto.sort_values(by="NF")
    cont = len(nfs_em_aberto)
    
    print('def qtdNfsEmAberto(): \n', nfs_em_aberto)
    print("\033[32mValores encontrados: ", cont, "\033[0m")
    return nfs_em_aberto
    
@VerificarTabelaCarregada        
def cobrarDevedores(tabela, destinatario, dataLimite, nf, valor):
    
    email_remetente = email
    senha_app = senhaapp  # Senha criada na conta google 
    email_destinatario = destinatario  

    # Criar mensagem
    msg = EmailMessage()
    msg['Subject'] = f'Cobrança de Nota Fiscal em Aberto – NF {nf} -- TESTE APLICAÇÃO'
    msg['From'] = email_remetente
    msg['To'] = email_destinatario                 
    msg.set_content(f'''     
    Prezado(a) Senhor(a),
    Conforme nossos registros, identificamos que a Nota Fiscal {nf}, encontra-se vencida até a presente data. Solicitamos, gentilmente,
    a verificação dessa pendência e, se procedente, a regularização do pagamento no menor prazo possível.
    Detalhes da Nota Fiscal:
    Número da NF: {nf}
    Valor: R$ {valor}
    Data de Vencimento: {dataLimite}

    Caso o pagamento já tenha sido efetuado, por favor, desconsidere esta mensagem. Em caso de dúvidas ou divergências, estamos
    à disposição para esclarecimentos.

    Agradecemos pela atenção e colaboração.

    Atenciosamente,
    [NOME DO FUNCIONÁRIO]
    [NOME DA EMPRESA]
    [Telefone / E-mail de contato, se quiser incluir]
        ''')

    print("\nEnviando Email....")
    # Conectar ao servidor Gmail e enviar
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(email_remetente, senha_app)
        smtp.send_message(msg)
        
    # Log mensagem
    print(f'''
    \033[92m+-----------------------------------------+
    {dt.datetime.now().strftime("%H:%M:%S")}: ✅ Email enviado com sucesso! 
    Enviado para: {email_destinatario}             
    +-----------------------------------------+\033[0m
    ''')
 
@dataFormatada     
@VerificarTabelaCarregada   
def abrirJanelaEmailVencidos(janela, dadosDataFrame, tabela):
    nova_janela = Toplevel(janela)
    nova_janela.title("Notas Fiscais Vencidas")
    nova_janela.geometry("700x400")

    Label(nova_janela, text="Notas Fiscais Vencidas", font=("Arial", 12, "bold")).pack(pady=10)
    
    def confirmarEmail():
        resposta = messagebox.askyesno("CONFIRMAÇÃO","Deseja enviar os e-mails de cobrança?",    parent=nova_janela)
        if resposta:
            for item in tree.get_children():
                valores = tree.item(item)["values"]    
                
                valorNF = valores[1]
                data = valores[2]
                nf = valores[4]
                destinatario = valores[5]
                
                cobrarDevedores(tabela, destinatario, data, nf, valorNF)
                
                print(f"DADO: {item} - valor: {valorNF} - data: {data} - nf: {nf} - destinatario: {destinatario}")
        
        if resposta:        
            print("E-mails enviados!")
            messagebox.showinfo("Concluido","E-mails enviados")
            
                        
    Button(nova_janela, text="Enviar Emails",command=confirmarEmail).pack(pady=5)           
    
    #region Tabela na nova janela
    
    frame_tabela = Frame(nova_janela)
    frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

    colunas = list(dadosDataFrame.columns)
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
                
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for linha in dadosDataFrame.values.tolist():
        tree.insert("", "end", values=linha)

    tree.pack(fill="both", expand=True)
    #endregion
 
    
    
   
    
   
    
    
    
    
   
    
    
