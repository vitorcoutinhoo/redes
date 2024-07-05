

#Tem a responsabilidade de guardar dados a respeito da votação
class ConfiguracaoVotacao:
    def __init__(self):
        self.title = "Eleição de Centro Acadêmico"
        self.description = "Vote no seu candidato favorito para o Centro Acadêmico de Ciência da Computação"
        self.candidatos = [{"nome":"Daniel","descricao":"Deseja trazer inovações para o curso"},{"nome":"Vitor","descricao":"Quer instalar novas máquinas potentes"}]
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
        str = "ESTADO ATUAL VOTACAO: \n"
        for i,candidato in enumerate(self.candidatos):
            str += f"Candidato {i+1} -- {candidato["nome"]} -----> {self.votos[i]}\n"
        return str