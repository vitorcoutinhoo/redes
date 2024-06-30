# Universidade Estadual de Santa Cruz
# Autores: Bruno Santos, Daniel Lago, Kauan Teles, Vítor Coutinho

# Codigo do servidor
# Responsável por mostrar a configuração da votação e armazenar a contagem de votos

import socket
from config import vote_config, voted_users, in_list


# Host e porta do servidor
HOST = "127.0.0.1"
PORT = 65432


# recebe a configuração da votação
config = vote_config()
votes = [0] * len(config["options"])


# interface com o usuário
def handle_client(conn, addr):
    # mostra o Título da votação
    conn.sendall(f"{config['title']}\n".encode())

    # pede identificação do usuário
    conn.sendall("Digite o seu identificador: ".encode())
    
    # recebe a identificação do usuário
    user_id = conn.recv(1024).decode().strip()
    if in_list(user_id): # verifica se o usuário já votou
        conn.sendall("Voto único por pessoa!\n".encode())
        return
    else: # se o usuário não votou, adiciona o usuário à lista de votantes
        voted_users(user_id)

        conn.sendall(f"{config['description']}\n".encode())
        for i, option in enumerate(config["options"]):
            conn.sendall(f"{i + 1}. {option['name']} - {option['description']}\n".encode())
        
        while True:
            conn.sendall("Digite o número do candidato: ".encode())
            vote = int(conn.recv(1024).decode().strip())

            if 1 <= vote <= len(config["options"]):
                votes[vote - 1] += 1
                conn.sendall("Voto computado com sucesso!\n".encode())
                break
            else:
                conn.sendall("Número desconhecido!\n".encode())
    
    conn.sendall("Obrigado por votar!\n".encode())
    conn.close()
            
def start_server():
    # cria o socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Servidor rodando em {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                handle_client(conn, addr)


if __name__ == "__main__":
    start_server()
