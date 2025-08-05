# 🧾 App de Automação de Cobranças com Envio por E-mail

Este é um aplicativo de automação de cobranças a partir de planilhas Excel, desenvolvido especialmente para pequenos negócios e autônomos.

   Com uma interface gráfica simples e intuitiva criada em Tkinter, o sistema permite:

  - Visualizar e filtrar notas fiscais em aberto;

  - Enviar e-mails de cobrança de forma prática e automatizada;

  - Reduzir o tempo gasto com tarefas manuais de cobrança.

A ideia surgiu ao conversar com meu irmão, que possui um pequeno negócio e enfrentava dificuldades para gerenciar e cobrar diversas notas fiscais vencidas. Com isso, desenvolvi esta solução para automatizar o processo de cobrança e otimizar o tempo produtivo, tornando a gestão financeira mais ágil e eficiente.


---

## ✨ Funcionalidades

- 📂 Importação de planilhas (Excel `.xlsx`, `.xls` ou `.csv`)
- 🔍 Visualização e filtragem de dados:
  - Notas fiscais vencidas
  - Pagas
  - Em aberto
  - Todas as notas
- 📧 Envio de e-mails automáticos para clientes com NFs vencidas
- 🔐 Tela de login protegida com senha (criptografada via SHA-256 + salt)
- 🖥 Interface amigável e centralizada na tela
- 📊 Visualização dos dados em tabela

##  Imagens

<img width="967" height="886" alt="image" src="https://github.com/user-attachments/assets/a945a4ed-f346-4d1d-9f84-375387eba8d8" />


<img width="1226" height="843" alt="image" src="https://github.com/user-attachments/assets/ec127222-9552-4914-8e34-961e4525dcb6" />


<img width="909" height="603" alt="image" src="https://github.com/user-attachments/assets/e8548907-bb64-48c5-8a83-0414e274e93f" />



## 🧠 Futuras melhorias

- Salvar histórico de cobranças
- Exportar resultados em PDF
- Tela de configurações (e-mail do remetente, assunto, corpo da mensagem)
  
  Atualmente o sistema possui uma mensagem de email fixo, pretendo implementar no futuro uma opção de email personalizavel.

---

## 🛠 Requisitos

- Python 3.10 ou superior
- Bibliotecas utilizadas:
  - `tkinter`
  - `pandas`
  - `openpyxl`
  - `smtplib`
  - `email`
  - `hashlib`

Instale as dependências com:

```bash
pip install pandas openpyxl
```

---

## ▶️ Como usar

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/SeuUsuario/AppCobrancaEmail.git
   cd AppCobrancaEmail
   ```

2. **Rode o sistema**:
   ```bash
   python main.py
   ```

3. Altere as informações de e-mail e senha do Gmail utilizando as credenciais da conta que deseja usar.

  A senha necessária aqui é a senha de aplicativo do Gmail.

  Para gerá-la, siga os passos abaixo:

    3.1. Ative a verificação em duas etapas na sua conta Google.

    3.2. Após ativá-la, acesse as configurações de segurança do Google e crie uma senha de aplicativo (senhas de app).

    3.3. Utilize essa senha gerada no lugar da senha comum da sua conta.

Essa configuração é necessária para que o aplicativo consiga enviar e-mails diretamente a partir da sua conta Gmail.
<img width="702" height="91" alt="image" src="https://github.com/user-attachments/assets/0910a042-d51b-4d63-93dd-fc978d97528c" />


4. **Digite a senha de acesso** (armazenada via hash no arquivo `login.py`)

      Como o sistema possui apenas um usuario, decidi por apenas uma senha padrão para entrar.(Claro que quando for implementar irei utilizar outra)
      Senha: testeapp123


6. **Selecione o arquivo Excel ou CSV** com os dados da cobrança
    - Utilize um dos arquivos excel que estão na pasta.
    - Caso deseje utilizar um própio, certifique-se que ele possui as colunas: NF, Valor em aberto, Data limite pagamento, Status, CPF e E-mail
    - Pretendo futuramente criar uma solução para que o sistema identifique automaticamente as colunas
      
7. **Escolha uma ação (ex: NFs vencidas)** e envie os e-mails!

---

## 🔐 Segurança

Mesmo sendo para uso de um único usuário no próprio computador, decidi aplicar uma camada básica de segurança.
A autenticação é feita por senha, protegida via **hash SHA-256 com salt fixo**. Não é necessário banco de dados.

---

## 📁 Estrutura

```
AppCobrancaEmail/
├── main.py               # Arquivo principal (interface e lógica)
├── login.py              # Tela de login + verificação de senha
├── funcoes.py            # Funções de filtro e envio de e-mails
├── tabela_view.py        # Criação da tabela (Treeview)
├── README.md             # Documentação do projeto
├── [arquivos .xlsx/csv]  # Suas planilhas
```

---

## 📦 Gerar executável

Você pode transformar o app em `.exe` com:
```bash
pip install pyinstaller 
```

```bash
pyinstaller --noconfirm --onefile --windowed --icon=icone.ico main.py
```

---

## 💡 Observações

- Certifique-se de que o e-mail do remetente está com **senha de app** ativada (no caso de Gmail).
- O envio de e-mails é feito via `smtplib`, porta 587 (TLS).

