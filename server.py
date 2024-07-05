import socket
import json
import threading
from config import ConfiguracaoVotacao as config
from typing import Dict, Any, Union
import sys
import signal


# Host e porta do servidor
HOST = "127.0.0.1"
PORT = 65432


#Classe que sustenta a conexão socket com os diversos clientes. 
#Possibilita trocar mensagens em JSON com os clientes
class ClienteHandler:
    def __init__(self, conexao: socket.socket, endereco: Any):
        self.conexao = conexao
        self.endereco = endereco

    #Codifica e envia mensagem JSON para o cliente através de um dict do python
    def enviar_mensagem(self, mensagem:  Union[Dict[str, Any], str]):
        try:
            if isinstance(mensagem, dict):
                #Seta \n no final para a interface poder delimitar os dados trafegados pelo socket
                mensagem_str = json.dumps(mensagem) + '\n'
            else:
                mensagem_str = mensagem + '\n'
            self.conexao.sendall(mensagem_str.encode())
        except (socket.error, socket.timeout, ConnectionResetError, BrokenPipeError) as e:
            print(f"Erro ao enviar mensagem para {self.endereco}: {e}")
    #Recebe uma mensagem via socket e decodifca-a para formato Dict do python         
    def receber_mensagem(self) -> Dict[str, Any]:
        try:
            data = self.conexao.recv(1024)
            if not data:
                raise ConnectionResetError("Conexão fechada pelo cliente")
            return json.loads(data.decode())
        except (socket.error, socket.timeout, ConnectionResetError, json.JSONDecodeError) as e:
            print(f"Erro ao receber mensagem de {self.endereco}: {e}")
            raise Exception()
            

    def fechar_conexao(self):
        self.conexao.close()

#Responsavel por manter o procolo de aplicação da votação
class ProcessadorVotacao:
    def __init__(self, cliente_handler: ClienteHandler, config: config):
        self.cliente_handler = cliente_handler
        self.config = config

    #Envia titulo da votação para o cliente
    def enviar_titulo(self):
        self.cliente_handler.enviar_mensagem({"titulo": self.config.title})
       
    #Verifica se identificador submetido pelo cliente é valido
    def verificar_identificador(self, identificador: str) -> bool:
        if self.config.usuarioJaVotou(identificador):
            self.cliente_handler.enviar_mensagem({"erro_idUnico": "Voto único por pessoa!"})
            return False
        self.config.add_usuario_votando(identificador)
        return True
    #Envia os detalhes e opções de voto da votação
    def enviar_opcoes_votacao(self):
        self.cliente_handler.enviar_mensagem({"descricao": self.config.description})

        self.cliente_handler.enviar_mensagem({"opcoes": self.config.candidatos})

    #Verifica se o voto é valido e processa o voto, ou acusa erro
    def processar_voto(self, voto,identificador) -> bool:
        if self.config.registrar_voto(voto,identificador):
            self.cliente_handler.enviar_mensagem({"sucesso": "Voto computado com sucesso!"})
            return True
        else:
            self.cliente_handler.enviar_mensagem({"erro_voto": "Número desconhecido! Por favor, envie um número válido."})
            return False
    #Metodo que é executado em thread para que o servidor lide com multiplas conexões
    #Ele executa o protocolo de aplicação
    def tratar_cliente(self):
        try:
            self.enviar_titulo()
            
            #Espera receber um identificador válido
            while True:
                mensagem = self.cliente_handler.receber_mensagem()
                if "identificador" in mensagem:
                    identificador = mensagem["identificador"]
                    if self.verificar_identificador(identificador):
                        self.enviar_opcoes_votacao()
                        break
            #Espera receber uma opção de voto válida
            while True:
                mensagem = self.cliente_handler.receber_mensagem()
                if "voto" in mensagem:
                    voto = mensagem["voto"]
                    if self.processar_voto(voto,identificador):
                        break

            self.cliente_handler.enviar_mensagem({"sucesso": "Obrigado por votar!"})

            #PRinta no console o estado atual da votação
            print(self.config.estadoAtual())


        finally:
            #Fecha a conexão com o respectivo cliente
            self.cliente_handler.fechar_conexao()

#Responsavel de criar o servidor socket e manter a conexão ativa com os clientes
class ServidorVotacao:
    #Seta configurações de endereçamento do servidor socket
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.config = config()

    #Inicia o servidor socket, que passa a 'ouvir' nas configurações setadas
    def iniciar(self):
        
        #Seta sinal caso haja alguma interrupção de teclado
        def signal_handler(sig, frame):
            print('Encerrando o servidor...')
            if self.servidor_socket:
                self.servidor_socket.close()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        #Intancia um socket e espera por conexões de clientes (interfaces)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
            servidor_socket.bind((self.host, self.port))
            servidor_socket.listen()
            print(f"Servidor rodando em {self.host}:{self.port}")
            while True:
                try:
                    #Recebe conexão de cliente especifico e joga o tratamento para uma thread separada
                    #Dessa forma, o server pode lidar com multiplas conexões
                    conexao, endereco = servidor_socket.accept()
                    print(f" ------- Conexão estabelecida com {endereco} ------- ")
                    cliente_handler = ClienteHandler(conexao, endereco)
                    processador_votacao = ProcessadorVotacao(cliente_handler, self.config)
                    thread = threading.Thread(target=processador_votacao.tratar_cliente)
                    thread.start()
                except Exception as e:
                    print(f"Erro ao aceitar conexão: {e}")
                    servidor_socket.close()
                    break

if __name__ == "__main__":
    servidor = ServidorVotacao(HOST, PORT)
    servidor.iniciar()
