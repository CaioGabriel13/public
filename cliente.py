import socket as sock
import threading

host = "172.20.10.2"
porta = 1313

sock_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
sock_cliente.connect((host, porta))
print("Conectado ao servidor")

# Enviar o nome do usuário para o servidor
nome = input("Digite seu nome para entrar:\n")
sock_cliente.sendall(nome.encode())

# Função para receber mensagens do servidor
def receber_mensagens():
    while True:
        try:
            mensagem = sock_cliente.recv(1024).decode()
            if mensagem:
                print(mensagem)
            else:
                raise
        except:
            print("Você se desconectou!")
            sock_cliente.close()
            break

# Função para enviar mensagens ao servidor
def enviar_mensagens():
    while True:
        mensagem = input()
        if mensagem == "/sair":
            sock_cliente.sendall(mensagem.encode())
            print("Você saiu do chat.")
            sock_cliente.close()
            break
        else:
            sock_cliente.sendall(mensagem.encode())

# Criar threads para enviar e receber mensagens simultaneamente
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

thread_enviar = threading.Thread(target=enviar_mensagens)
thread_enviar.start()
