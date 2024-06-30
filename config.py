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


# Configuração da lista de votantes
def voted_users(user_id):
    """
    Adiciona um usuário à lista de votantes
    """
    i = 1
    with open("voted_users.csv", "a", encoding="utf-8") as f:
        f.write(i + ", " + user_id + "\n")
        i += 1


def in_list(user_id):
    """
    Verifica se um usuário está na lista de votantes
    """
    with open("voted_users.csv", "r", encoding="utf-8") as f:
        for line in f:
            if user_id in line:
                return True
        return False
