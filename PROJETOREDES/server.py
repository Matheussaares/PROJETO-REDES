# server.py

import socket
import threading

# Configurações do Servidor
HOST = '127.0.0.1'  # Endereço local (localhost)
PORT = 65432        # Porta para ouvir

clients = []
nicknames = []

def broadcast(message, _client_socket=None):
    """ Envia uma mensagem para todos os clientes conectados """
    for client in clients:
        # CORREÇÃO BUG 2 (Alteração 1): Não enviar a mensagem de volta para o remetente
        if client != _client_socket: 
            try:
                client.send(message)
            except:
                remove_client(client)

def remove_client(client_socket):
    """ Remove um cliente da lista e avisa os outros """
    if client_socket in clients:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        client_socket.close()
        nickname = nicknames[index]
        nicknames.remove(nickname)
        # Para mensagens do sistema (como 'saiu do chat'), _client_socket=None, 
        # então todos recebem, o que está correto.
        broadcast(f'SYS: {nickname} saiu do chat.'.encode('utf-8'))
        print(f"Cliente {nickname} desconectado.")

def handle_client(client_socket):
    """ Lida com a conexão de um cliente individual """
    try:
        # [REQUISITO: 10] 1. Registro de Apelido
        nickname = client_socket.recv(1024).decode('utf-8')
        
        # [REQUISITO: 31, 41] Verificar se o apelido é duplicado
        if nickname in nicknames:
            client_socket.send('ERR: apelido_em_uso'.encode('utf-8'))
            client_socket.close()
            return

        nicknames.append(nickname)
        clients.append(client_socket)
        
        # [REQUISITO: 20, 21] Enviar confirmação ao cliente
        client_socket.send(f'SYS: Conectado. Bem-vindo, {nickname}!'.encode('utf-8'))
        
        # Avisar a todos sobre o novo usuário
        # Aqui passamos o client_socket para que o novo usuário não receba "User joao joined."
        broadcast(f'SYS: User {nickname} joined.'.encode('utf-8'), client_socket)
        print(f"Cliente {nickname} conectado.")
        
    except Exception as e:
        print(f"Erro no registro do apelido: {e}")
        remove_client(client_socket)
        return

    # 2. Loop de Mensagens
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message:
                raise ConnectionResetError

            # [REQUISITO: 16] Lógica de Comandos
            
            # [REQUISITO: 17] Comando WHO
            if message.upper() == 'WHO':
                lista_usuarios = ", ".join(nicknames)
                client_socket.send(f'SYS: Usuários conectados: {lista_usuarios}'.encode('utf-8'))
                continue # <-- Correção Bug 1
                
            # [REQUISITO: 18] Comando QUIT
            elif message.upper() == 'QUIT':
                raise ConnectionResetError # Força a desconexão limpa
                
            # [REQUISITO: 14] Lógica de Mensagem Direta (DM)
            elif message.startswith('@'):
                try:
                    dest_nick = message.split(' ')[0][1:] # Pega "joao" de "@joao ..."
                    dm_content = " ".join(message.split(' ')[1:])
                    
                    if dest_nick in nicknames:
                        dest_index = nicknames.index(dest_nick)
                        dest_socket = clients[dest_index]
                        
                        # [REQUISITO: 15] Envia a DM formatada
                        dest_socket.send(f'FROM {nickname} [dm]: {dm_content}'.encode('utf-8'))
                    else:
                        # [REQUISITO: 23, 40] Erro se usuário não for encontrado
                        client_socket.send(f'ERR: user_not_found'.encode('utf-8'))
                except:
                    client_socket.send('ERR: Formato de DM inválido. Use @apelido mensagem'.encode('utf-8'))
                
                continue # <-- Correção Bug 1

            # [REQUISITO: 11, 12] Lógica Broadcast (Padrão)
            else:
                # CORREÇÃO BUG 2 (Alteração 2): Passa o client_socket para o broadcast
                broadcast(f'FROM {nickname} [all]: {message}'.encode('utf-8'), client_socket)

        except (ConnectionResetError, BrokenPipeError):
            # [REQUISITO: 30] Tratar desconexões
            remove_client(client_socket)
            break # Sai do loop while True e encerra a thread
        except Exception as e:
            print(f"Erro ao lidar com {nickname}: {e}")
            remove_client(client_socket)
            break

# Função principal do servidor
def start_server():
    # [REQUISITO: 7, 27] Cria o socket do servidor (TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    
    print(f"Servidor ouvindo em {HOST}:{PORT}")
    
    while True:
        client_socket, address = server.accept()
        print(f"Nova conexão de {address}")
        
        # [REQUISITO: 28] Inicia uma nova thread para lidar com este cliente
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()