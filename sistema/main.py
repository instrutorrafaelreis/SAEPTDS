import hashlib
import sqlite3
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()


# =====================================================================
# FUNÇÕES AUXILIARES: CRIPTOGRAFIA (LGPD - Item 5.4) E BANCO DE DADOS
# =====================================================================
def criptografar(texto: str) -> str:
    """Criptografa CPF e Senha usando SHA-256 (Biblioteca padrão do Python)."""
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def get_db():
    """Conecta ao banco local SQLite (zero configuração) e ativa Foreign Keys."""
    conn = sqlite3.connect("saep_db.sqlite")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar_banco():
    """Cria as tabelas e insere os 3 registros iniciais caso o banco esteja vazio (Itens 2.1 e 2.2)."""
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


# =====================================================================
# ATIVIDADE 3: FUNCIONALIDADE DE LOGIN (Itens 3.1, 3.2 e 3.3)
# =====================================================================
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
    <p><small>Dica de teste: Login <b>ana</b> | Senha <b>123</b></small></p>
    """


@app.post("/login")
def fazer_login(login: str = Form(), senha: str = Form()):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM tutor WHERE login = ? AND senha = ?",
        (login, criptografar(senha)),
    ).fetchone()
    conn.close()

    # Item 3.3: Validação caso haja falha de autenticação
    if not user:
        return RedirectResponse("/?erro=Login+ou+senha+invalidos!", status_code=303)

    # Item 3.1 e 3.2: Redireciona para o módulo principal e cria sessão com tempo de expiração (1800s = 30 min)
    res = RedirectResponse("/principal", status_code=303)
    res.set_cookie(key="usuario_sessao", value=user["nome"], max_age=1800)
    return res


@app.get("/logout")
def logout():
    # Item 4.2: Meio para sair do sistema
    res = RedirectResponse("/", status_code=303)
    res.delete_cookie("usuario_sessao")
    return res


# =====================================================================
# ATIVIDADE 4: FUNCIONALIDADE PRINCIPAL DO SISTEMA (Itens 4.1, 4.2, 4.3)
# =====================================================================
@app.get("/principal", response_class=HTMLResponse)
def tela_principal(request: Request):
    usuario = request.cookies.get("usuario_sessao")
    if not usuario:
        return RedirectResponse("/?erro=Sessao+expirada.+Faca+login+novamente.", status_code=303)

    return f"""
    <h2>Sistema Clínica Veterinária - Tela Principal</h2>
    <p>Usuário logado: <b>{usuario}</b> | <a href="/logout">Sair do Sistema</a></p>
    <hr>
    <h3>Menu de Funcionalidades (Item 4.3):</h3>
    <ul>
        <li><a href="/tutores">Gerenciar Tutores</a></li>
        <li><a href="/pets">Gerenciar Pets</a></li>
        <li><a href="/agendamentos">Gerenciar Agendamentos</a></li>
    </ul>
    """


# =====================================================================
# ATIVIDADE 5: GERENCIAMENTO DE TUTOR (Itens 5.1, 5.2, 5.3, 5.4 e 5.5)
# =====================================================================
@app.get("/tutores", response_class=HTMLResponse)
def listar_tutores(busca: str = ""):
    conn = get_db()
    # Item 5.2: Busca com termo
    if busca:
        tutores = conn.execute("SELECT * FROM tutor WHERE nome LIKE ?", (f"%{busca}%",)).fetchall()
    else:
        tutores = conn.execute("SELECT * FROM tutor").fetchall()
    conn.close()

    linhas = ""
    for t in tutores:
        # Item 5.1 (Listar e Excluir) e Item 5.5 (Editar tutor já existente diretamente na linha)
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

    <!-- Item 5.3 e 5.4: Inserir novo tutor (CPF e Senha serão criptografados) -->
    <h3>Novo Tutor</h3>
    <form method="post" action="/tutores/criar">
        Nome: <input name="nome" required>
        Telefone: <input name="telefone" required>
        CPF: <input name="cpf" required>
        Login: <input name="login" required>
        Senha: <input type="password" name="senha" required>
        <button type="submit">Cadastrar Tutor</button>
    </form>
    <hr>

    <!-- Item 5.2: Busca por termo -->
    <form method="get" action="/tutores">
        Buscar por nome: <input name="busca" value="{busca}">
        <button type="submit">Buscar</button>
        <a href="/tutores">Limpar</a>
    </form>
    <br>

    <!-- Item 5.1: Listagem -->
    <table border="1" cellpadding="5">
        <tr><th>ID</th><th>Nome</th><th>Telefone</th><th>Login</th><th>CPF (Hash LGPD)</th><th>Ações</th></tr>
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
    # Item 5.4: Criptografa CPF e Senha antes de persistir no banco
    conn.execute(
        "INSERT INTO tutor (nome, telefone, cpf, login, senha) VALUES (?, ?, ?, ?, ?)",
        (nome, telefone, criptografar(cpf), login, criptografar(senha)),
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/tutores", status_code=303)


@app.post("/tutores/editar")
def editar_tutor(
    id: int = Form(),
    nome: str = Form(),
    telefone: str = Form(),
    login: str = Form(),
):
    # Item 5.5: Atualiza dados do tutor existente
    conn = get_db()
    conn.execute(
        "UPDATE tutor SET nome = ?, telefone = ?, login = ? WHERE id = ?",
        (nome, telefone, login, id),
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/tutores", status_code=303)


@app.get("/tutores/excluir/{id}")
def excluir_tutor(id: int):
    # Item 5.1: Excluir registro de tutor
    conn = get_db()
    conn.execute("DELETE FROM tutor WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/tutores", status_code=303)


# =====================================================================
# ATIVIDADE 6: GERENCIAMENTO DE PETS (Item 6.1)
# =====================================================================
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

    <!-- Item 6.1: Inserir novo pet associando-o a um tutor no banco -->
    <h3>Novo Pet</h3>
    <form method="post" action="/pets/criar">
        Nome do Pet: <input name="nome" required>
        Espécie: <input name="especie" required>
        Tutor: <select name="tutor_id" required>{opcoes_tutor}</select>
        <button type="submit">Cadastrar Pet</button>
    </form>
    <hr>
    <table border="1" cellpadding="5">
        <tr><th>ID</th><th>Nome do Pet</th><th>Espécie</th><th>Tutor Associado</th></tr>
        {linhas}
    </table>
    """


@app.post("/pets/criar")
def criar_pet(nome: str = Form(), especie: str = Form(), tutor_id: int = Form()):
    conn = get_db()
    conn.execute(
        "INSERT INTO pet (nome, especie, tutor_id) VALUES (?, ?, ?)",
        (nome, especie, tutor_id),
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/pets", status_code=303)


# =====================================================================
# ATIVIDADE 7: GERENCIAMENTO DE AGENDAMENTOS (Itens 7.1 e 7.2)
# =====================================================================
@app.get("/agendamentos", response_class=HTMLResponse)
def listar_agendamentos():
    conn = get_db()
    pets = conn.execute("SELECT id, nome FROM pet").fetchall()

    # Item 7.1: Listar agendamentos ordenado por data, trazendo dados do tutor e do pet
    # DICA DE PROVA:
    # - Ordenação padrão por data: ORDER BY a.data_agendamento ASC
    # - Prova 1 (por dia):  ORDER BY strftime('%d', a.data_agendamento) ASC  (ou DAY(a.data_agendamento) no MySQL)
    # - Prova 2 (por mês):  ORDER BY strftime('%m', a.data_agendamento) ASC  (ou MONTH(a.data_agendamento) no MySQL)
    # - Prova 3 (por ano):  ORDER BY strftime('%Y', a.data_agendamento) ASC  (ou YEAR(a.data_agendamento) no MySQL)
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
        # Item 7.2: Atualizar a data de um agendamento existente
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

    <h3>Novo Agendamento</h3>
    <form method="post" action="/agendamentos/criar">
        Data: <input type="date" name="data_agendamento" required>
        Serviço: <input name="servico" required>
        Pet: <select name="pet_id" required>{opcoes_pet}</select>
        <button type="submit">Agendar</button>
    </form>
    <hr>
    <table border="1" cellpadding="5">
        <tr><th>ID</th><th>Data (Ordenada)</th><th>Serviço</th><th>Dados do Pet</th><th>Dados do Tutor</th></tr>
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
    # Item 7.2: Atualiza a data de um agendamento
    conn = get_db()
    conn.execute(
        "UPDATE agendamento SET data_agendamento = ? WHERE id = ?",
        (data_agendamento, id),
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/agendamentos", status_code=303)
