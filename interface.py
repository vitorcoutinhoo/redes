
from client import Cliente
from typing import Dict, Any, Union
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring

# Configurações do servidor
SERVER_IP = "127.0.0.1"
PORT = 65432


class InterfaceVotacao:
    def __init__(self):
        
        self.cliente_votacao = Cliente(SERVER_IP, PORT)
        self.user = ""
        try:
            self.cliente_votacao.conectar()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor: {e}")
            return

        # Inicializacao do menu
        self.Menu()

    def Menu(self):
        #Configurações inicias da interface
        self.root = Tk()
        self.root.geometry("600x400")
        self.centralizar_janela(600, 400)
        self.root.resizable(False, False)

        # Receber o título da votação
        try:
            mensagem = self.cliente_votacao.receber_mensagem()
            self.root.title(f"Votação Online - {mensagem.get('titulo')}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao receber título da votação: {e}")
            self.root.destroy()
            return

        # Solicitar identificador
        self.enviar_identificador()

        self.root.mainloop()

    #Centraliza a interface no meio da tela
    def centralizar_janela(self, largura, altura):
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    
    #CAptura o identificador do usuario e efetua os devidos tratamentos
    def enviar_identificador(self):
        while True:
            identificador = askstring("Identificação", "Digite o seu identificador:")
            if identificador:
                try:
                    self.cliente_votacao.enviar_mensagem({"identificador": identificador})
                    mensagem = self.cliente_votacao.receber_mensagem()
                    
                    if "erro_idUnico" in mensagem:
                        #Erro acusado pelo servidor quando identificador já fez um voto
                        messagebox.showerror("Erro", mensagem["erro_idUnico"])
                    else:
                        #Recebe a descricao e opções de voto do servidor
                        self.user = identificador
                        descricao = mensagem.get("descricao", "")
                        mensagem = self.cliente_votacao.receber_mensagem()
                        opcoes = mensagem.get("opcoes", [])
                        self.exibir_opcoes_votacao(descricao, opcoes)
                        self.root.lift()
                        break
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao enviar identificador: {e}")
                    self.root.destroy()
                    return
            else:
                messagebox.showerror("Erro", "Identificador não pode ser vazio.")


    #Exibe a descrição da votação na interface e cria botões com base nas opções de votação disponivel
    def exibir_opcoes_votacao(self, descricao: str, opcoes: list):
        Label(self.root, text=descricao, font=('Calibri', 14), wraplength=550).pack(pady=20)

        #Instancia botões que ao serem clicados, enviam voto para o servidor.
        for i, opcao in enumerate(opcoes):
            frame = Frame(self.root, padx=10, pady=10)
            frame.pack(fill=X, padx=20, pady=5)
            btn = Button(frame, text=f"{opcao['nome']} - {opcao['descricao']}",
                         command=lambda id=i+1: self.confirmar_voto(id), font=('Calibri', 12),
                         relief=RAISED, bd=3, wraplength=500)
            btn.pack(fill=X)

    
    #Confirma a opção de voto e envia opção de voto para o servidor
    def confirmar_voto(self, voto: int):
        confirmacao = messagebox.askyesno("Confirmação de Voto", f"Você ({self.user}) deseja votar na opção {voto}?")
        if confirmacao:
            try:
                self.cliente_votacao.enviar_mensagem({"voto": voto})
                mensagem = self.cliente_votacao.receber_mensagem()
                
                #Caso o voto é registrado com sucesso
                if "sucesso" in mensagem:
                    messagebox.showinfo("Votação", mensagem["sucesso"])
                    self.cliente_votacao.fechar_conexao()
                    self.root.destroy()
                
                #Caso haja algum erro com o voto
                elif "erro" in mensagem:
                    messagebox.showerror("Erro", mensagem["erro_voto"])
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao enviar voto: {e}")
                self.root.destroy()

# Execução do programa
if __name__ == "__main__":
    app = InterfaceVotacao()
