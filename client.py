# Universidade Estadual de Santa Cruz
# Autores: Bruno Santos, Daniel Lago, Kauan Teles, Vítor Coutinho

# Codigo do cliente
# Responsável por mostrar a configuração da votação e enviar o voto ao servidor

import socket

# Host e porta do servidor
HOST = "127.0.0.1"
PORT = 65432


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        # Recebe e exibe o título da votação
        print(s.recv(1024).decode())
        
        # Envia o identificador do usuário
        user_id = input("Digite o seu identificador: ")
        s.sendall(user_id.encode())
        
        # Verifica se o usuário já votou
        response = s.recv(1024).decode()
        if "Voto único por pessoa!" in response:
            print(response)
            return
        
        # Recebe e exibe a descrição da votação
        print(s.recv(1024).decode())
        
        # Recebe e exibe todas as opções de voto
        options_msg = s.recv(1024).decode()
        options = options_msg.split('|')
        for option in options:
            print(option)
        
        vote = input("Digite o número da opção desejada: ")
        s.sendall(vote.encode())
        
        response = s.recv(1024).decode()
        print(response)
        
        # Agradecimento final
        print(s.recv(1024).decode())

if __name__ == "__main__":
    start_client()
