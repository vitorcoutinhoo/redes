import socket
import json
from typing import Dict, Any, Union

# Configurações do servidor
SERVER_IP = "127.0.0.1"
PORT = 65432

#Responsavel por efetuar conexão socket com o servidor, trocando mensagens JSON com ele de acordo
#Com o protocolo de aplicação estabelecido
class Cliente:
    #Seta as configuração de endereçamento para conexão
    def __init__(self, server_ip: str, port: int):
        self.server_ip = server_ip
        self.port = port
        self.conexao = None
        
        #Buffer para receber dados do servidor e possibilitar recuperá-los em json
        self.buffer = ""
    
    #Cria conexão socket com o servidor a partir das configurações iniciais
    def conectar(self):
        try:
            self.conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conexao.connect((self.server_ip, self.port))
        except (socket.error, ConnectionRefusedError) as e:
            print(f"Erro ao conectar ao servidor: {e}")
            raise

    #Envia mensagem em formato JSON para o servidor
    def enviar_mensagem(self, mensagem: Union[Dict[str, Any], str]):
        try:
            if isinstance(mensagem, dict):
                mensagem_str = json.dumps(mensagem)
            else:
                mensagem_str = mensagem
            self.conexao.sendall(mensagem_str.encode())
        except (socket.error, socket.timeout, ConnectionResetError, BrokenPipeError) as e:
            print(f"Erro ao enviar mensagem: {e}")
            self.fechar_conexao()

    #Recebe e decodifica mensagens em JSON para o servidor
    def receber_mensagem(self) -> Dict[str, Any]:
        try:
            while True:
                data = self.conexao.recv(1024).decode()
                self.buffer += data
                if '\n' in self.buffer:
                    mensagem_json = self.buffer[:self.buffer.index('\n')]
                    self.buffer = self.buffer[self.buffer.index('\n') + 1:]
                    return json.loads(mensagem_json.strip())
        except (socket.error, socket.timeout, ConnectionResetError, json.JSONDecodeError) as e:
            print(f"Erro ao receber mensagem: {e}")
            self.fechar_conexao()
            return {}

    #Fecha a conexão do socket com o servidor
    def fechar_conexao(self):
        if self.conexao:
            try:
                self.conexao.close()
            except socket.error as e:
                print(f"Erro ao fechar conexão: {e}")

