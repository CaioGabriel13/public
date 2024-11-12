import socket as sock
import threading

# Dicionário para armazenar conexões de clientes com seus respectivos nomes
clientes = {}

# Função para receber dados de um cliente específico
def receber_dados(sock_cliente, endereco):
    try:
        nome = sock_cliente.recv(1024).decode()
        if (nome in clientes):
            sock_cliente.sendall("Nome já existente".encode())
            sock_cliente.close()
            return    
        clientes[nome] = sock_cliente
        print(f"{nome}:{endereco} entrou no chat.")
        broadcast(f"{nome} entrou no chat.", sock_cliente)

        while True:
            mensagem = sock_cliente.recv(1024).decode()
            if mensagem == "/sair":
                print(f"{nome} saiu do chat.")
                broadcast(f"{nome} saiu do chat.", sock_cliente)
                sock_cliente.close()
                del clientes[nome]
                break
            elif mensagem.startswith("/"):
                # Tratamento de mensagem privada
                if (not ":" in mensagem):
                    enviar_privado(nome, "Comando inválido\n", nome)
                else:
                    destinatario, mensagem_privada = mensagem[1:].split(":", 1)
                    enviar_privado(destinatario.strip(), f"{nome} (privado): {mensagem_privada.strip()}", sock_cliente)
            else:
                broadcast(f"{nome}: {mensagem}", sock_cliente)

    except Exception as e:
        print(f"Erro com o cliente {endereco}: {e}")
        sock_cliente.close()
        if nome in clientes:
            del clientes[nome]

# Função para enviar mensagem para todos os clientes conectados
def broadcast(mensagem, origem):
    for cliente in clientes.values():
        if cliente != origem:
            try:
                cliente.sendall(mensagem.encode())
            except:
                cliente.close()
                remover_cliente(cliente)

# Função para enviar mensagem privada
def enviar_privado(nome_destinatario, mensagem, origem):
    if nome_destinatario in clientes and clientes[nome_destinatario] != origem:
        try:
            clientes[nome_destinatario].sendall(mensagem.encode())
        except:
            print(f"Erro ao enviar mensagem privada para {nome_destinatario}")
    else:
        origem.sendall(f"Usuário {nome_destinatario} não está conectado.".encode())

# Função para remover cliente da lista ao desconectar
def remover_cliente(cliente):
    for nome, conexao in list(clientes.items()):
        if conexao == cliente:
            del clientes[nome]
            break

# Configurações do servidor
host = "172.20.10.2"
porta = 1313
sock_servidor = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
sock_servidor.bind((host, porta))
sock_servidor.listen()

print(f"O servidor {host}:{porta} está aguardando conexões...")

# Aceitar novas conexões
while True:
    sock_conn, endereco = sock_servidor.accept()
    thread_cliente = threading.Thread(target=receber_dados, args=(sock_conn, endereco))
    thread_cliente.start()