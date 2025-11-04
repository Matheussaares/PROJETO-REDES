# Projeto Mini-Chat TCP com Python

Este projeto implementa um chat multiusuário em Python usando a biblioteca `socket`. O sistema segue o modelo cliente-servidor, utiliza o protocolo TCP e gerencia múltiplos clientes simultaneamente usando threads.

## 🚀 Guia de Execução (em Codespaces)

Para rodar este projeto, você precisará de 3 terminais:

1.  **Terminal 1 (Servidor):**
    * Abra o primeiro terminal.
    * Entre na pasta do projeto: `cd PROJETOREDES`
    * Inicie o servidor: `python server.py`
    * (Você verá a mensagem: `Servidor ouvindo em 127.0.0.1:65432`)

2.  **Terminal 2 (Cliente 1):**
    * Abra um segundo terminal.
    * Entre na pasta do projeto: `cd PROJETOREDES`
    * Inicie o cliente: `python client.py`
    * **IP:** Aperte `Enter` (para usar o padrão `127.0.0.1`).
    * **Apelido:** Escolha um apelido (ex: `matheus`).

3.  **Terminal 3 (Cliente 2):**
    * Abra um terceiro terminal.
    * Entre na pasta do projeto: `cd PROJETOREDES`
    * Inicie o cliente: `python client.py`
    * **IP:** Aperte `Enter`.
    * **Apelido:** Escolha outro apelido (ex: `daniel`).

Agora você pode enviar mensagens entre os terminais 2 e 3.

---

## 📖 Documento do Protocolo

O chat utiliza um protocolo simples baseado em texto para a comunicação.

### 1. Registro de Apelido
* **Cliente:** Ao conectar, a primeira mensagem enviada é o apelido desejado.
* **Servidor (Sucesso):** Responde `SYS: Conectado. Bem-vindo, <apelido>!`.
* **Servidor (Erro):** Responde `ERR: apelido_em_uso` e fecha a conexão.

### 2. Mensagens de Chat

* **Broadcast (Padrão):**
    * **Cliente envia:** `Olá a todos!`
    * **Servidor envia (para todos, exceto remetente):** `FROM <remetente> [all]: Olá a todos!`

* **Mensagem Direta (DM):**
    * **Cliente envia:** `@daniel você pode me ajudar?`
    * **Servidor envia (apenas para 'daniel'):** `FROM <remetente> [dm]: você pode me ajudar?`

### 3. Comandos Adicionais

* **`WHO`:**
    * **Cliente envia:** `WHO`
    * **Servidor responde (apenas para o cliente):** `SYS: Usuários conectados: matheus, daniel`

* **`QUIT`:**
    * **Cliente envia:** `QUIT`
    * O cliente se desconecta. O servidor avisa os outros: `SYS: <apelido> saiu do chat.`

### 4. Respostas do Servidor

* **Confirmações:** `SYS: Conectado...`, `SYS: User ... joined.`
* **Erros:** `ERR: apelido_em_uso`, `ERR: user_not_found`.
* **Mensagens:** `FROM <apelido> [all]: ...`, `FROM <apelido> [dm]: ...`.

---

## ✅ Casos de Teste Verificados

O sistema foi testado para os seguintes cenários:
* [X] Broadcast com múltiplos clientes.
* [X] Mensagem direta para usuário existente.
* [X] Mensagem direta para usuário inexistente (retorna `ERR: user_not_found`).
* [X] Tentativa de apelido duplicado (retorna `ERR: apelido_em_uso`).