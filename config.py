

#Tem a responsabilidade de guardar dados a respeito da votação
class ConfiguracaoVotacao:
    def __init__(self):
        self.title = self.setTitle()
        self.description = self.setDescription()
        self.candidatos = self.setCandidatos()
        self.votos = [0 for n in self.candidatos]
        self.users = {}

    #Registra o voto de um usuario para um determinado candidato
    def registrar_voto(self, opcao, userid):
        if not isinstance(opcao,int):
            return False
        if 1 <= opcao <= len(self.candidatos):    
                self.votos[opcao - 1] += 1
                self.users[userid] = opcao
                return True
        else:
            return False

    #Seta o nome da votação
    def setTitle(self):
        title = str(input('Digite o nome da votação: '))
        return title
    #Seta a descrição da votação
    def setDescription(self):
        description = str(input('Escreva a descrição da votação: '))
        return description
    #Seta as opções de voto
    def setCandidatos(self):
        lista = []
        status = True
        print('-- A seguir, insira as opções de voto --')
        while status != '.':
            status = str(input("Digite o nome da opção de voto(Digite '.' para executar o server: "))
            if status == '.':
                break
            else:
                desc =str(input("Escreva descrição dessa opcao de voto: "))
                lista.append({"nome":status,"descricao":desc})
        return lista
    #Verifica se determinado usuario já fez a votação
    def usuarioJaVotou(self,userid):
        if userid in self.users.keys():
            return True
        else:
             return False
    #Adiciona o usuario na lista de usuario enquanto ele ainda esta votando
    def add_usuario_votando(self,userid):
        self.users[userid] = -1
    
    #Mostra o estado atual da votação, quantos votos tem os candidatos
    def estadoAtual(self):
        str = "\nESTADO ATUAL VOTACAO: \n"
        for i,candidato in enumerate(self.candidatos):
            str += f"Candidato {i+1} -- {candidato["nome"]} -----> {self.votos[i]}\n"
        return str