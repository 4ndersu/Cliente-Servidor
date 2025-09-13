import socket
import threading
import os

# Função que lida com cada cliente conectado
def atender_cliente(conn, addr):
    print(f"[Servidor] Conectado com {addr}")
    while True:
        try:
            # Primeiro, receber o tipo de mensagem
            tipo = conn.recv(4).decode()

            if not tipo:
                break

            if tipo == "TEXT":  # Mensagem normal de texto
                msg = conn.recv(1024).decode()
                if msg == "FIM":
                    break
                print(f"[Servidor] Texto de {addr}: {msg}")
                conn.sendall(f"Servidor recebeu: {msg}".encode())

            elif tipo == "FILE":  # Transferência de arquivo
                # Receber o nome do arquivo
                nome = conn.recv(1024).decode()
                print(f"[Servidor] Recebendo arquivo: {nome}")

                # Receber o tamanho do arquivo
                tamanho = int(conn.recv(20).decode().strip())
                print(f"[Servidor] Tamanho: {tamanho} bytes")

                # Criar pasta para salvar
                os.makedirs("recebidos", exist_ok=True)
                caminho = os.path.join("recebidos", nome)

                # Receber os bytes do arquivo
                with open(caminho, "wb") as f:
                    recebido = 0
                    while recebido < tamanho:
                        dados = conn.recv(4096)
                        if not dados:
                            break
                        f.write(dados)
                        recebido += len(dados)

                print(f"[Servidor] Arquivo {nome} salvo em {caminho}")
                conn.sendall(f"Arquivo {nome} recebido!".encode())

        except Exception as e:
            print(f"[Servidor] Erro: {e}")
            break

    print(f"[Servidor] Encerrando conexão com {addr}")
    conn.close()


# Servidor TCP
def servidor():
    host = "127.0.0.1"
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[Servidor] Aguardando conexões em {host}:{port}...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=atender_cliente, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    servidor()
