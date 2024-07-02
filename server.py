# Universidade Estadual de Santa Cruz
# Autores: Bruno Santos, Daniel Lago, Kauan Teles, Vítor Coutinho

# Codigo do servidor
# Responsável por mostrar a configuração da votação e armazenar a contagem de votos

import socket
from config import vote_config, voted_users, in_list, create_arqv


# Host e porta do servidor
HOST = "127.0.0.1"
PORT = 65432

VOTELIST = "voted_users.csv"
create_arqv(VOTELIST)

# recebe a configuração da votação
config = vote_config()
votes = [0] * len(config["options"])


# Interface com o usuário
def handle_client(conn, addr):
    
    # Mostra o título da votação
    conn.sendall(f"{config['title']}\n".encode())

    # Pede identificação do usuário
    conn.sendall("Digite o seu identificador: ".encode())

    # Recebe a identificação do usuário
    user_id = conn.recv(1024).decode().strip()
    if in_list(VOTELIST, user_id):  # Verifica se o usuário já votou
        conn.sendall("Voto único por pessoa!\n".encode())
        conn.close()
        return
    else:  # Se o usuário não votou, adiciona o usuário à lista de votantes
        voted_users(VOTELIST, user_id)

        conn.sendall(f"{config['description']}\n".encode())
        
        # Envia todas as opções de voto em uma única mensagem, separadas por '|'
        options_msg = "|".join([f"{i + 1}. {option['name']} - {option['description']}" for i, option in enumerate(config["options"])])
        conn.sendall(options_msg.encode())

        # Envia uma string vazia para indicar o fim da lista de opções
        conn.sendall("\n".encode())

        # Recebe o voto do usuário
        vote = conn.recv(1024).decode().strip()
        vote = int(vote)

        if 1 <= vote <= len(config["options"]):
            votes[vote - 1] += 1
            conn.sendall("Voto computado com sucesso!\n".encode())
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
