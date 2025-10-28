%%writefile server.py

import socket
import threading

# Configurações do Servidor
# Vamos usar '0.0.0.0' para aceitar conexões de qualquer interface
# (O ngrok vai se conectar a esta porta)
HOST = '0.0.0.0'
PORT = 65432        # Porta interna no Colab

# Listas para armazenar clientes e seus apelidos
clients = []
nicknames = []

# Função para transmitir mensagens para todos os clientes (Broadcast)
def broadcast(message, _client_socket=None):
    for client in clients:
        try:
            client.send(message)
        except:
            remove_client(client)

# Função para remover um cliente
def remove_client(client_socket):
    if client_socket in clients:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        client_socket.close()
        nickname = nicknames[index]
        nicknames.remove(nickname)
        broadcast(f'SYS: {nickname} saiu do chat.'.encode('utf-8'))

# Função para lidar com cada cliente individualmente (em sua própria thread)
def handle_client(client_socket):
    try:
        nickname = client_socket.recv(1024).decode('utf-8')
        
        if nickname in nicknames:
            client_socket.send('ERR: apelido_em_uso'.encode('utf-8'))
            client_socket.close()
            return 

        nicknames.append(nickname)
        clients.append(client_socket)
        
        client_socket.send(f'SYS: Conectado. Bem-vindo, {nickname}!'.encode('utf-8'))
        broadcast(f'SYS: User {nickname} joined.'.encode('utf-8'), client_socket)
        
    except Exception as e:
        print(f"Erro no registro do apelido: {e}")
        remove_client(client_socket)
        return

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message:
                raise ConnectionResetError
            
            # Lógica de Mensagens (Implemente DM e WHO aqui)
            if message.upper() == 'WHO':
                lista_usuarios = ", ".join(nicknames)
                client_socket.send(f'SYS: Usuários conectados: {lista_usuarios}'.encode('utf-8'))
                
            elif message.upper() == 'QUIT':
                raise ConnectionResetError
                
            else:
                broadcast(f'FROM {nickname} [all]: {message}'.encode('utf-8'))

        except (ConnectionResetError, BrokenPipeError):
            print(f"Cliente {nickname} desconectou.")
            remove_client(client_socket)
            break
        except Exception as e:
            print(f"Erro ao lidar com {nickname}: {e}")
            remove_client(client_socket)
            break

# Função principal do servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    
    print(f"Servidor ouvindo em {HOST}:{PORT} (dentro do Colab)")
    
    while True:
        client_socket, address = server.accept()
        print(f"Nova conexão de {address}")
        
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()