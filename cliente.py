import socket
import time
import random
import os

def enviar_texto(sock, msg):
    sock.sendall("TEXT".encode())  # Indica que é texto
    sock.sendall(msg.encode())
    resposta = sock.recv(1024).decode()
    print(f"[Cliente] Resposta do servidor: {resposta}")

def enviar_arquivo(sock, caminho):
    if not os.path.exists(caminho):
        print("[Cliente] Arquivo não encontrado!")
        return

    nome = os.path.basename(caminho)
    tamanho = os.path.getsize(caminho)

    print(f"[Cliente] Enviando arquivo {nome} ({tamanho} bytes)")

    # Informar ao servidor que é um arquivo
    sock.sendall("FILE".encode())
    time.sleep(0.1)

    # Enviar nome do arquivo
    sock.sendall(nome.encode())
    time.sleep(0.1)

    # Enviar tamanho do arquivo (20 bytes reservados)
    sock.sendall(str(tamanho).ljust(20).encode())

    # Enviar conteúdo
    with open(caminho, "rb") as f:
        while True:
            dados = f.read(4096)
            if not dados:
                break
            sock.sendall(dados)

    resposta = sock.recv(1024).decode()
    print(f"[Cliente] Resposta do servidor: {resposta}")


def cliente(nome):
    host = "127.0.0.1"
    port = 5000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"[{nome}] Conectado ao servidor.")

    # Enviar algumas mensagens de texto
    for i in range(2):
        msg = f"Mensagem {i+1} do {nome}"
        print(f"[{nome}] Enviando: {msg}")
        enviar_texto(client_socket, msg)
        time.sleep(random.uniform(1, 2))

    # Enviar imagem
    enviar_arquivo(client_socket, "teste.jpg")

    # Encerrar
    enviar_texto(client_socket, "FIM")
    client_socket.close()
    print(f"[{nome}] Conexão encerrada.")


if __name__ == "__main__":
    cliente("Andersu")
