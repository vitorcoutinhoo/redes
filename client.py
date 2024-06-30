# Universidade Estadual de Santa Cruz
# Autores: Bruno Santos, Daniel Lago, Kauan Teles, Vítor Coutinho

# Codigo do cliente
# Responsável por mostrar a configuração da votação e enviar o voto ao servidor]

import socket

# Host e porta do servidor
HOST = "127.0.0.1"
PORT = 65432

def start_client():
    # cria o socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        


if __name__ == "__main__":
    start_client()