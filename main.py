import os #OS é utilizado para acessar variáveis de ambiente

from dotenv import load_dotenv #Dotenv é utilizado para carregar variáveis de ambiente de um arquivo .env

load_dotenv()   # isso carrega MONGO_URI, NEO4J_URI etc antes de qualquer import

from cli.menu import menu # Importa o menu do CLI para que o usuário possa interagir com o sistema

if __name__ == "__main__": # Ponto de partida do programa
    menu() # Chama o menu iterativo