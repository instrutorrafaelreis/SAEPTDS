# 📘 Tutorial Passo a Passo — Prova Prática SAEP (Python + FastAPI)

🌐 **Acesse o Tutorial Interativo Online (GitHub Pages):**  
👉 **[https://instrutorrafaelreis.github.io/SAEPTDS/](https://instrutorrafaelreis.github.io/SAEPTDS/)**

---

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
 ├── der.svg ou der.pdf     (Entrega 2: Diagrama Entidade-Relacionamento)
 ├── saep_db.sql            (Entrega 3: Script SQL de criação e população)
 └── sistema/               (Entregas 4 a 8: Pasta obrigatória com nome "sistema")
      └── main.py           (Código-fonte completo do sistema)
```

---

## 📝 PASSO 1: Documentação de Software (Vale 3 Pontos)
> **Itens avaliados:**  
> - **1.1 (Peso 2):** Identificar no mínimo 4 requisitos funcionais.  
> - **1.2 (Peso 1):** Identificar os requisitos de infraestrutura (SGBD e Linguagem).

O caderno de prova permite entregar em formato **`.txt`**, `.docx` ou `.pdf`. Crie um arquivo chamado **`documentacao.txt`** com o seguinte conteúdo:

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

![Diagrama Entidade Relacionamento](./der.svg)

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

Crie uma pasta chamada **`sistema`** e, dentro dela, crie o arquivo **`main.py`** conforme os 6 blocos detalhados no [Tutorial Completo](./TUTORIAL_PASSO_A_PASSO_ALUNO.md) ou no arquivo pronto [`sistema/main.py`](./sistema/main.py).

---

## ▶️ PASSO 5: Como Rodar e Testar o Sistema

```bash
cd sistema
uvicorn main:app --reload
```
Acesse no navegador: **`http://127.0.0.1:8000`** (Login: `ana` | Senha: `123`).

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
