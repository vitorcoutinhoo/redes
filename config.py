# Universidade Estadual de Santa Cruz
# Autores: Bruno Santos, Daniel Lago, Kauan Teles, Vítor Coutinho

# Codigo da configuração da votação
# Responsável por configurar a votação


# Configuração da votação
def vote_config():
    """
    Retorna a configuração da votação: título, descrição e candidatos
    """
    return {
        "title": "Eleição de Centro Acadêmico",
        "description": "Vote no seu candidato favorito para o Centro Acadêmico de Ciência da Computação",
        "options": [
            {"name": "Candidato 1", "description": "Descrição do candidato 1"},
            {"name": "Candidato 2", "description": "Descrição do candidato 2"},
            {"name": "Candidato 3", "description": "Descrição do candidato 3"},
        ],
    }


def create_arqv(arqv):
    """
    Cria o arquivo de votantes
    """
    with open(arqv, "w", encoding="utf-8"):
        pass
    
def voted_users(arqv, user_id):
    """
    Adiciona o usuário à lista de votantes
    """
    with open(arqv, "a", encoding="utf-8") as f:
        f.write(user_id + "\n")

def in_list(arqv, user_id):
    """
    Verifica se o usuário já votou
    """
    with open(arqv, "r", encoding="utf-8") as f:
        if user_id in f.read():
            return True
        return False
