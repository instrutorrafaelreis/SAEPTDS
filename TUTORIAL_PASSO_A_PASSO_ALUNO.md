# 📘 Tutorial Passo a Passo — Prova Prática SAEP (Python + FastAPI)
**Curso:** Técnico em Desenvolvimento de Sistemas  
**Tema:** Sistema de Gestão para Clínica Veterinária (Tutores, Pets e Agendamentos)  
**Objetivo:** Garantir de **80% a 100% da nota** escrevendo o menor e mais simples código possível, sem perder tempo com CSS ou JavaScript.

---

## 🎯 A Estratégia para Passar com Folga (37 Pontos no Total)

Na prova prática do SAEP você tem **3 horas** e **não tem internet**. A prova **não avalia beleza visual (CSS)**, ela avalia **funcionalidade**.

Por isso, nossa estratégia usa **4 atalhos inteligentes**:
1. **Zero JavaScript e Zero CSS:** Usaremos apenas `<form>` puro do HTML dentro do próprio FastAPI (`HTMLResponse`).
2. **Apenas 1 arquivo Python (`sistema/main.py`):** Você não precisa criar pastas de templates, arquivos `.js` ou `.css`.
3. **Apenas 3 tabelas (`tutor`, `pet`, `agendamento`):** Como o edital pede que o Tutor tenha CPF e Senha criptografados, usamos a própria tabela `tutor` para fazer o Login do sistema.
4. **Edição direto na tabela:** Em vez de criar uma tela nova só para editar o Tutor ou mudar a data do Agendamento, colocamos os campos `<input>` dentro da própria linha da tabela (`<tr>`).

### 📁 Estrutura de Arquivos que você deve entregar na pasta da prova:
```text
Pasta_Da_Entrega/
 ├── documentacao.txt       (Entrega 1: Requisitos Funcionais e Infraestrutura)
 ├── der.png ou der.pdf     (Entrega 2: Diagrama Entidade-Relacionamento)
 ├── saep_db.sql            (Entrega 3: Script SQL de criação e população)
 └── sistema/               (Entregas 4 a 8: Pasta obrigatória com nome "sistema")
      └── main.py           (Código-fonte completo do sistema)
```

---

## 📝 PASSO 1: Documentação de Software (Vale 3 Pontos)
> **Itens avaliados:**  
> - **1.1 (Peso 2):** Identificar no mínimo 4 requisitos funcionais.  
> - **1.2 (Peso 1):** Identificar os requisitos de infraestrutura (SGBD e Linguagem).

O caderno de prova permite entregar em formato **`.txt`**, `.docx` ou `.pdf`. Crie um arquivo chamado **`documentacao.txt`** (ou preencha o `documentacao.docx` fornecido pelo avaliador) com o seguinte conteúdo:

```text
1.1 REQUISITOS FUNCIONAIS DO SISTEMA (Mínimo 4)
- RF01: O sistema deve permitir o login de usuários validando as credenciais no banco de dados, exibindo mensagem de erro em caso de falha e criando sessão com tempo de expiração.
- RF02: O sistema deve exibir na tela principal o nome do usuário logado na sessão, links para os módulos "Tutor", "Pet" e "Agendamento", e opção para sair do sistema (logout).
- RF03: O sistema deve permitir cadastrar, listar, buscar por termo, editar e excluir tutores, salvando CPF e senha criptografados no banco de dados (LGPD).
- RF04: O sistema deve permitir cadastrar e listar pets associando obrigatoriamente cada pet a um tutor existente.
- RF05: O sistema deve permitir cadastrar agendamentos, atualizar a data de um agendamento e listar os agendamentos ordenados por data exibindo os dados do tutor e do pet.

1.2 LISTA DE REQUISITOS DE INFRAESTRUTURA
- Linguagem de Programação: Python 3 (com framework FastAPI)
- Sistema Gerenciador de Banco de Dados (SGBD): MySQL / SQLite3
- Servidor Web: Uvicorn
- Editor de Código / IDE: VS Code
```

---

## 🗂️ PASSO 2: Diagrama Entidade-Relacionamento - DER (Vale 1 Ponto)
> **Item avaliado:**  
> - **1.3 (Peso 1):** Gerar o Diagrama Entidade-Relacionamento conforme descrito no caderno.

Você pode desenhar rapidamente na ferramenta disponível no computador da prova (MySQL Workbench, brModelo, Draw.io ou LibreOffice Draw) e exportar como imagem ou PDF. O diagrama tem apenas **3 entidades**:

```
+-----------------------+       1          N +-----------------------+       1          N +--------------------------+
|         TUTOR         |--------------------|          PET          |--------------------|       AGENDAMENTO        |
+-----------------------+                    +-----------------------+                    +--------------------------+
| PK  id (INT)          |                    | PK  id (INT)          |                    | PK  id (INT)             |
|     nome (VARCHAR)    |                    |     nome (VARCHAR)    |                    |     data_agendamento     |
|     telefone (VARCHAR)|                    |     especie (VARCHAR) |                    |     servico (VARCHAR)    |
|     cpf (VARCHAR)     |                    | FK  tutor_id (INT)    |                    | FK  pet_id (INT)         |
|     login (VARCHAR)   |                    +-----------------------+                    +--------------------------+
|     senha (VARCHAR)   |
+-----------------------+
```
* **Relacionamento 1:** Um `TUTOR` possui vários `PET`s (`1:N` — chave estrangeira `tutor_id` na tabela `pet`).
* **Relacionamento 2:** Um `PET` possui vários `AGENDAMENTO`s (`1:N` — chave estrangeira `pet_id` na tabela `agendamento`).

---

## 🗄️ PASSO 3: Script do Banco de Dados `saep_db.sql` (Vale 3 Pontos)
> **Itens avaliados:**  
> - **2.1 (Peso 2):** Criar as tabelas respeitando a chave estrangeira (`FOREIGN KEY`) de cada relacionamento.  
> - **2.2 (Peso 1):** Inserir pelo menos **3 registros em cada uma das tabelas**.

Crie o arquivo **`saep_db.sql`** na raiz da entrega.  
**Regra de ouro:** Sempre crie as tabelas na ordem **`tutor` -> `pet` -> `agendamento`** para que as chaves estrangeiras funcionem de primeira!

```sql
CREATE DATABASE IF NOT EXISTS saep_db;
USE saep_db;

-- 1. Tabela TUTOR
CREATE TABLE IF NOT EXISTS tutor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    cpf VARCHAR(64) NOT NULL,
    login VARCHAR(50) NOT NULL,
    senha VARCHAR(64) NOT NULL
);

-- 2. Tabela PET (Chave Estrangeira para tutor)
CREATE TABLE IF NOT EXISTS pet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    tutor_id INT NOT NULL,
    FOREIGN KEY (tutor_id) REFERENCES tutor(id) ON DELETE CASCADE
);

-- 3. Tabela AGENDAMENTO (Chave Estrangeira para pet)
CREATE TABLE IF NOT EXISTS agendamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_agendamento DATE NOT NULL,
    servico VARCHAR(100) NOT NULL,
    pet_id INT NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES pet(id) ON DELETE CASCADE
);

-- INSERÇÃO DE 3 REGISTROS EM CADA TABELA (Item 2.2)
-- Obs: O hash SHA-256 da senha abaixo corresponde a '123'
INSERT INTO tutor (nome, telefone, cpf, login, senha) VALUES
('Ana Silva', '11999990001', '2c624232cdd221771294dfbb310aca000a0df6ac8b66b696d90ef06fdefb64a3', 'ana', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'),
('Carlos Souza', '11999990002', '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b', 'carlos', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'),
('Mariana Costa', '11999990003', 'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35', 'mariana', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3');

INSERT INTO pet (nome, especie, tutor_id) VALUES
('Rex', 'Cachorro', 1),
('Mimi', 'Gato', 2),
('Thor', 'Cachorro', 3);

INSERT INTO agendamento (data_agendamento, servico, pet_id) VALUES
('2026-05-20', 'Consulta Geral', 1),
('2026-03-10', 'Vacinação', 2),
('2025-11-05', 'Banho e Tosa', 3);
```

---

## 💻 PASSO 4: Criando o Sistema em Python + FastAPI (Vale 29 Pontos)

Crie uma pasta chamada **`sistema`** e, dentro dela, crie o arquivo **`main.py`**.  
Vamos construir o `main.py` em **6 pequenos blocos** na ordem exata da prova.

---

### 🔹 Bloco 1: Importações, Criptografia LGPD e Banco de Dados
> **Por que esse bloco é importante?**  
> A função `criptografar()` tem **apenas 2 linhas** e usa `hashlib` (que já vem no Python). Só ela garante os **3 pontos do Item 5.4 (LGPD)**! Além disso, a função `inicializar_banco()` já cria e popula o banco automaticamente quando você roda o sistema.

```python
import hashlib
import sqlite3
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# ITEM 5.4 (Peso 3): Criptografia de Senha e CPF (LGPD)
def criptografar(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()

# Conexão com o banco de dados
def get_db():
    conn = sqlite3.connect("saep_db.sqlite")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Inicializa as tabelas e os 3 registros iniciais automaticamente
def inicializar_banco():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS tutor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            cpf TEXT NOT NULL,
            login TEXT NOT NULL,
            senha TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS pet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especie TEXT NOT NULL,
            tutor_id INTEGER NOT NULL,
            FOREIGN KEY (tutor_id) REFERENCES tutor(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS agendamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_agendamento TEXT NOT NULL,
            servico TEXT NOT NULL,
            pet_id INTEGER NOT NULL,
            FOREIGN KEY (pet_id) REFERENCES pet(id) ON DELETE CASCADE
        );
    """)
    if conn.execute("SELECT COUNT(*) FROM tutor").fetchone()[0] == 0:
        senha_padrao = criptografar("123")
        conn.executemany(
            "INSERT INTO tutor (nome, telefone, cpf, login, senha) VALUES (?, ?, ?, ?, ?)",
            [
                ("Ana Silva", "11999990001", criptografar("11111111111"), "ana", senha_padrao),
                ("Carlos Souza", "11999990002", criptografar("22222222222"), "carlos", senha_padrao),
                ("Mariana Costa", "11999990003", criptografar("33333333333"), "mariana", senha_padrao),
            ],
        )
        conn.executemany(
            "INSERT INTO pet (nome, especie, tutor_id) VALUES (?, ?, ?)",
            [("Rex", "Cachorro", 1), ("Mimi", "Gato", 2), ("Thor", "Cachorro", 3)],
        )
        conn.executemany(
            "INSERT INTO agendamento (data_agendamento, servico, pet_id) VALUES (?, ?, ?)",
            [
                ("2026-05-20", "Consulta Geral", 1),
                ("2026-03-10", "Vacinação", 2),
                ("2025-11-05", "Banho e Tosa", 3),
            ],
        )
        conn.commit()
    conn.close()

inicializar_banco()
```

---

### 🔹 Bloco 2: Funcionalidade de Login (Vale 6 Pontos)
> **Itens avaliados:**  
> - **3.1 (Peso 1):** Autenticar login e senha no banco e redirecionar para `/principal`.  
> - **3.2 (Peso 3):** Criar sessão com tempo de expiração (`max_age=1800` = 30 minutos).  
> - **3.3 (Peso 2):** Exibir mensagem de erro caso o login falhe.

Adicione abaixo do Bloco 1:

```python
@app.get("/", response_class=HTMLResponse)
def tela_login(erro: str = ""):
    msg_erro = f"<p style='color:red;'><b>{erro}</b></p>" if erro else ""
    return f"""
    <h2>Login - Clínica Veterinária</h2>
    {msg_erro}
    <form method="post" action="/login">
        Login: <input name="login" required> <br><br>
        Senha: <input type="password" name="senha" required> <br><br>
        <button type="submit">Entrar</button>
    </form>
    """

@app.post("/login")
def fazer_login(login: str = Form(), senha: str = Form()):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM tutor WHERE login = ? AND senha = ?",
        (login, criptografar(senha)),
    ).fetchone()
    conn.close()

    # Item 3.3 (Peso 2): Validação em caso de falha no login
    if not user:
        return RedirectResponse("/?erro=Login+ou+senha+invalidos!", status_code=303)

    # Item 3.1 (Peso 1) e Item 3.2 (Peso 3): Redireciona e cria sessão com expiração (1800 segundos)
    res = RedirectResponse("/principal", status_code=303)
    res.set_cookie(key="usuario_sessao", value=user["nome"], max_age=1800)
    return res

@app.get("/logout")
def logout():
    # Item 4.2 (Peso 1): Sair do sistema apagando a sessão
    res = RedirectResponse("/", status_code=303)
    res.delete_cookie("usuario_sessao")
    return res
```

---

### 🔹 Bloco 3: Funcionalidade Principal do Sistema (Vale 4 Pontos)
> **Itens avaliados:**  
> - **4.1 (Peso 2):** Recuperar o nome do usuário na sessão e exibir na tela principal.  
> - **4.2 (Peso 1):** Disponibilizar botão/link para sair do sistema (`/logout`).  
> - **4.3 (Peso 1):** Disponibilizar links para acessar **Tutor**, **Pet** e **Agendamento**.

Adicione abaixo do Bloco 2:

```python
@app.get("/principal", response_class=HTMLResponse)
def tela_principal(request: Request):
    # Item 4.1 (Peso 2): Recupera o nome do usuário salvo na sessão
    usuario = request.cookies.get("usuario_sessao")
    if not usuario:
        return RedirectResponse("/?erro=Sessao+expirada!", status_code=303)

    return f"""
    <h2>Tela Principal - Clínica Veterinária</h2>
    <p>Bem-vindo(a), <b>{usuario}</b>! | <a href="/logout">Sair do Sistema</a></p>
    <hr>
    <h3>Menu (Item 4.3):</h3>
    <ul>
        <li><a href="/tutores">Tutor</a></li>
        <li><a href="/pets">Pet</a></li>
        <li><a href="/agendamentos">Agendamento</a></li>
    </ul>
    """
```

---

### 🔹 Bloco 4: Gerenciamento de Tutor (Vale 13 Pontos — O Mais Importante!)
> **Itens avaliados:**  
> - **5.1 (Peso 2):** Listar e excluir tutores cadastrados.  
> - **5.2 (Peso 3):** Buscar tutor por termo (`WHERE nome LIKE ?`).  
> - **5.3 (Peso 2):** Inserir novo tutor no banco e atualizar a lista.  
> - **5.4 (Peso 3):** Criptografar CPF e senha do tutor ao salvar.  
> - **5.5 (Peso 3):** Editar um tutor já existente no banco.

Adicione abaixo do Bloco 3:

```python
@app.get("/tutores", response_class=HTMLResponse)
def listar_tutores(busca: str = ""):
    conn = get_db()
    # Item 5.2 (Peso 3): Busca por termo
    if busca:
        tutores = conn.execute("SELECT * FROM tutor WHERE nome LIKE ?", (f"%{busca}%",)).fetchall()
    else:
        tutores = conn.execute("SELECT * FROM tutor").fetchall()
    conn.close()

    linhas = ""
    for t in tutores:
        # Item 5.1 (Listar/Excluir) + Item 5.5 (Editar direto na linha da tabela!)
        linhas += f"""
        <tr>
            <form method="post" action="/tutores/editar">
                <td>{t['id']}<input type="hidden" name="id" value="{t['id']}"></td>
                <td><input name="nome" value="{t['nome']}" required></td>
                <td><input name="telefone" value="{t['telefone']}" required></td>
                <td><input name="login" value="{t['login']}" required></td>
                <td><small>{t['cpf'][:12]}...</small></td>
                <td>
                    <button type="submit">Salvar Edição</button>
                    <a href="/tutores/excluir/{t['id']}">Excluir</a>
                </td>
            </form>
        </tr>
        """

    return f"""
    <p><a href="/principal">Voltar para Principal</a></p>
    <h2>Gerenciamento de Tutores</h2>

    <!-- Item 5.3: Cadastro de novo tutor -->
    <form method="post" action="/tutores/criar">
        Nome: <input name="nome" required>
        Telefone: <input name="telefone" required>
        CPF: <input name="cpf" required>
        Login: <input name="login" required>
        Senha: <input type="password" name="senha" required>
        <button type="submit">Cadastrar Tutor</button>
    </form>
    <hr>

    <!-- Item 5.2: Formulário de Busca -->
    <form method="get" action="/tutores">
        Buscar tutor: <input name="busca" value="{busca}">
        <button type="submit">Buscar</button>
        <a href="/tutores">Limpar</a>
    </form>
    <br>

    <table border="1" cellpadding="5">
        <tr><th>ID</th><th>Nome</th><th>Telefone</th><th>Login</th><th>CPF (Criptografado)</th><th>Ações</th></tr>
        {linhas}
    </table>
    """

@app.post("/tutores/criar")
def criar_tutor(
    nome: str = Form(),
    telefone: str = Form(),
    cpf: str = Form(),
    login: str = Form(),
    senha: str = Form(),
):
    conn = get_db()
    # Item 5.3 e 5.4: Insere tutor criptografando CPF e Senha
    conn.execute(
        "INSERT INTO tutor (nome, telefone, cpf, login, senha) VALUES (?, ?, ?, ?, ?)",
        (nome, telefone, criptografar(cpf), login, criptografar(senha)),
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/tutores", status_code=303)

@app.post("/tutores/editar")
def editar_tutor(id: int = Form(), nome: str = Form(), telefone: str = Form(), login: str = Form()):
    # Item 5.5 (Peso 3): Edita um tutor existente
    conn = get_db()
    conn.execute("UPDATE tutor SET nome = ?, telefone = ?, login = ? WHERE id = ?", (nome, telefone, login, id))
    conn.commit()
    conn.close()
    return RedirectResponse("/tutores", status_code=303)

@app.get("/tutores/excluir/{id}")
def excluir_tutor(id: int):
    # Item 5.1 (Peso 2): Exclui um tutor
    conn = get_db()
    conn.execute("DELETE FROM tutor WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/tutores", status_code=303)
```

---

### 🔹 Bloco 5: Gerenciamento de Pets (Vale 3 Pontos)
> **Item avaliado:**  
> - **6.1 (Peso 3):** Inserir um novo pet associando-o a um tutor no banco de dados (usando `<select name="tutor_id">`).

Adicione abaixo do Bloco 4:

```python
@app.get("/pets", response_class=HTMLResponse)
def listar_pets():
    conn = get_db()
    tutores = conn.execute("SELECT id, nome FROM tutor").fetchall()
    pets = conn.execute("""
        SELECT p.id, p.nome, p.especie, t.nome AS tutor_nome
        FROM pet p JOIN tutor t ON p.tutor_id = t.id
    """).fetchall()
    conn.close()

    opcoes_tutor = "".join([f"<option value='{t['id']}'>{t['nome']}</option>" for t in tutores])
    linhas = "".join([
        f"<tr><td>{p['id']}</td><td>{p['nome']}</td><td>{p['especie']}</td><td>{p['tutor_nome']}</td></tr>"
        for p in pets
    ])

    return f"""
    <p><a href="/principal">Voltar para Principal</a></p>
    <h2>Gerenciamento de Pets</h2>

    <!-- Item 6.1 (Peso 3): Cadastrar Pet escolhendo o Tutor -->
    <form method="post" action="/pets/criar">
        Nome do Pet: <input name="nome" required>
        Espécie: <input name="especie" required>
        Tutor: <select name="tutor_id" required>{opcoes_tutor}</select>
        <button type="submit">Cadastrar Pet</button>
    </form>
    <hr>
    <table border="1" cellpadding="5">
        <tr><th>ID</th><th>Nome do Pet</th><th>Espécie</th><th>Tutor</th></tr>
        {linhas}
    </table>
    """

@app.post("/pets/criar")
def criar_pet(nome: str = Form(), especie: str = Form(), tutor_id: int = Form()):
    conn = get_db()
    conn.execute("INSERT INTO pet (nome, especie, tutor_id) VALUES (?, ?, ?)", (nome, especie, tutor_id))
    conn.commit()
    conn.close()
    return RedirectResponse("/pets", status_code=303)
```

---

### 🔹 Bloco 6: Gerenciamento de Agendamentos (Vale 5 Pontos)
> **Itens avaliados:**  
> - **7.1 (Peso 3):** Listar os agendamentos ordenados por data trazendo os dados do tutor e do pet.  
>   - **Atenção ao tipo da sua prova no `ORDER BY`:**  
>     - **Prova 1 (Dia):** `ORDER BY strftime('%d', a.data_agendamento) ASC`  
>     - **Prova 2 (Mês):** `ORDER BY strftime('%m', a.data_agendamento) ASC`  
>     - **Prova 3 (Ano):** `ORDER BY strftime('%Y', a.data_agendamento) ASC`  
>     - **Data Completa:** `ORDER BY a.data_agendamento ASC`  
> - **7.2 (Peso 2):** Atualizar a data de um agendamento existente.

Adicione abaixo do Bloco 5:

```python
@app.get("/agendamentos", response_class=HTMLResponse)
def listar_agendamentos():
    conn = get_db()
    pets = conn.execute("SELECT id, nome FROM pet").fetchall()

    # Item 7.1 (Peso 3): Lista agendamentos com dados do pet e do tutor ordenados por data
    agendamentos = conn.execute("""
        SELECT a.id, a.data_agendamento, a.servico,
               p.nome AS pet_nome, p.especie AS pet_especie,
               t.nome AS tutor_nome, t.telefone AS tutor_telefone
        FROM agendamento a
        JOIN pet p ON a.pet_id = p.id
        JOIN tutor t ON p.tutor_id = t.id
        ORDER BY a.data_agendamento ASC
    """).fetchall()
    conn.close()

    opcoes_pet = "".join([f"<option value='{p['id']}'>{p['nome']}</option>" for p in pets])
    linhas = ""
    for a in agendamentos:
        # Item 7.2 (Peso 2): Permite atualizar a data do agendamento direto na linha
        linhas += f"""
        <tr>
            <td>{a['id']}</td>
            <td>
                <form method="post" action="/agendamentos/atualizar" style="margin:0;">
                    <input type="hidden" name="id" value="{a['id']}">
                    <input type="date" name="data_agendamento" value="{a['data_agendamento']}" required>
                    <button type="submit">Atualizar Data</button>
                </form>
            </td>
            <td>{a['servico']}</td>
            <td>{a['pet_nome']} ({a['pet_especie']})</td>
            <td>{a['tutor_nome']} - Tel: {a['tutor_telefone']}</td>
        </tr>
        """

    return f"""
    <p><a href="/principal">Voltar para Principal</a></p>
    <h2>Gerenciamento de Agendamentos</h2>

    <form method="post" action="/agendamentos/criar">
        Data: <input type="date" name="data_agendamento" required>
        Serviço: <input name="servico" required>
        Pet: <select name="pet_id" required>{opcoes_pet}</select>
        <button type="submit">Agendar</button>
    </form>
    <hr>
    <table border="1" cellpadding="5">
        <tr><th>ID</th><th>Data</th><th>Serviço</th><th>Pet</th><th>Tutor</th></tr>
        {linhas}
    </table>
    """

@app.post("/agendamentos/criar")
def criar_agendamento(data_agendamento: str = Form(), servico: str = Form(), pet_id: int = Form()):
    conn = get_db()
    conn.execute(
        "INSERT INTO agendamento (data_agendamento, servico, pet_id) VALUES (?, ?, ?)",
        (data_agendamento, servico, pet_id),
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/agendamentos", status_code=303)

@app.post("/agendamentos/atualizar")
def atualizar_data_agendamento(id: int = Form(), data_agendamento: str = Form()):
    # Item 7.2 (Peso 2): Atualiza a data no banco de dados
    conn = get_db()
    conn.execute("UPDATE agendamento SET data_agendamento = ? WHERE id = ?", (data_agendamento, id))
    conn.commit()
    conn.close()
    return RedirectResponse("/agendamentos", status_code=303)
```

---

## ▶️ PASSO 5: Como Rodar e Testar o Sistema

1. Abra o terminal na pasta `sistema`:
   ```bash
   cd sistema
   uvicorn main:app --reload
   ```
2. Abra o navegador em: **`http://127.0.0.1:8000`**
3. Faça o teste completo como o avaliador fará:
   * [x] Digite uma senha errada para ver a mensagem vermelha de erro (**Item 3.3**).
   * [x] Entre com login **`ana`** e senha **`123`** (**Itens 3.1 e 3.2**).
   * [x] Veja o nome `Ana Silva` no topo e os 3 links do menu (**Itens 4.1, 4.2 e 4.3**).
   * [x] Clique em **Tutor**: busque por `Ana` (**Item 5.2**), cadastre um novo tutor (**Itens 5.3 e 5.4**), altere o telefone de um tutor e clique em `Salvar Edição` (**Item 5.5**), e teste o botão `Excluir` (**Item 5.1**).
   * [x] Clique em **Pet**: cadastre um novo pet selecionando o tutor na caixinha `<select>` (**Item 6.1**).
   * [x] Clique em **Agendamento**: veja a lista ordenada por data (**Item 7.1**) e mude a data de um agendamento clicando em `Atualizar Data` (**Item 7.2**).

---

## 📊 Resumo da Pontuação (Onde estão os pontos mais fáceis)

| Bloco / Entrega | Tempo p/ Fazer | Pontos Ganhos | Acumulado (%) |
| :--- | :---: | :---: | :---: |
| 1. `documentacao.txt` + `DER` | 15 min | **4 pts** | 10,8% |
| 2. `saep_db.sql` (3 tabelas + 3 inserts) | 15 min | **3 pts** | 18,9% |
| 3. Login + Sessão (`max_age`) + Erro | 15 min | **6 pts** | 35,1% |
| 4. Tela Principal (Nome + Menu + Logout) | 10 min | **4 pts** | 45,9% |
| 5. CRUD de Tutor + Busca + `hashlib` | 30 min | **13 pts** | **81,1% (Meta atingida!)** |
| 6. Cadastro de Pet com `<select>` | 10 min | **3 pts** | 89,2% |
| 7. Agendamentos (Listar ordenado + Mudar data) | 15 min | **5 pts** | **100% (37/37 pts)** |
