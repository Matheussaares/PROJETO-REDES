# client.py

import socket
import threading

# [REQUISITO: 29] Interação 100% via terminal
def receive_messages(client_socket):
    """ Ouve por mensagens do servidor em uma thread separada """
    while True:
        try:
            # [REQUISITO: 24] Recebe mensagens formatadas (de sistema, erro, ou usuários)
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("Servidor fechou a conexão.")
                client_socket.close()
                break
                
            print(message) 
            
        except (ConnectionResetError, BrokenPipeError):
            print("Desconectado do servidor.")
            client_socket.close()
            break
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            client_socket.close()
            break

def start_client():
    # Para o teste local, o IP será sempre 127.0.0.1
    HOST = input("Digite o IP do servidor (default: 127.0.0.1): ") or '127.0.0.1'
    PORT = 65432

    # [REQUISITO: 27] Cria o socket do cliente (TCP)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((HOST, PORT))
    except Exception as e:
        print(f"Não foi possível conectar ao servidor: {e}")
        return

    # [REQUISITO: 10] Loop para registrar o apelido
    while True:
        nickname = input("Escolha seu apelido: ")
        if " " in nickname or not nickname:
            print("Apelido não pode conter espaços ou ser vazio.")
        else:
            client.send(nickname.encode('utf-8'))
            
            # Aguarda a resposta do servidor (confirmação ou erro)
            response = client.recv(1024).decode('utf-8')
            print(response)
            
            # [REQUISITO: 23] Lida com erro de apelido
            if response.startswith('ERR: apelido_em_uso'):
                continue # Pede o apelido novamente
            elif response.startswith('SYS: Conectado'):
                break # Apelido aceito, sai do loop
            else:
                client.close()
                return

    # [REQUISITO: 28] Inicia uma thread para receber mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True 
    receive_thread.start()

    # Thread principal para enviar mensagens
    try:
        while True:
            message = input()
            client.send(message.encode('utf-8'))
            
            # [REQUISITO: 18] Se o usuário digitar QUIT, encerra
            if message.upper() == 'QUIT':
                print("Encerrando conexão...")
                client.close()
                break
                
    except (KeyboardInterrupt, EOFError):
        print("\nDesconectando...")
        client.send('QUIT'.encode('utf-8'))
        client.close()
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        client.close()

if __name__ == "__main__":
    start_client()