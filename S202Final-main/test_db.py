# test_db.py

"""
Script de teste para verificar conexões e operações básicas em MongoDB e Neo4j.
Execute: python test_db.py
"""
import os #OS é utilizado para acessar variáveis de ambiente
from dotenv import load_dotenv #Dotenv é utilizado para carregar variáveis de ambiente de um arquivo .env

# Carrega variáveis de ambiente do arquivo .env
# Renomeia dotenv.env para .env na raiz do projeto
load_dotenv() # isso carrega MONGO_URI, NEO4J_URI etc antes de qualquer import

# Parâmetros MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017") # URI do MongoDB
MONGO_DB = os.getenv("MONGO_DB", "steam_market") # Nome do banco de dados

# Parâmetros Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687") # URI do Neo4j
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j") # Usuário do Neo4j
NEO4J_PASS = os.getenv("NEO4J_PASS", "senha") # Senha do Neo4j

# Debug: imprimir variáveis de ambiente para verificação de carregamento
print(f">>> MONGO_URI = {MONGO_URI}")
print(f">>> MONGO_DB  = {MONGO_DB}")
print(f">>> NEO4J_URI= {NEO4J_URI}")
print(f">>> NEO4J_USER= {NEO4J_USER}")
print(f">>> NEO4J_PASS= {NEO4J_PASS}")

# Importa handlers após carregar e imprimir variáveis
# Handlers são responsáveis por interagir com os bancos de dados
from database.mongo_handler import MongoHandler # MongoHandler é responsável por interagir com o MongoDB
from database.neo4j_handler import Neo4jHandler # Neo4jHandler é responsável por interagir com o Neo4j


def test_mongo(): # Função para testar operações básicas no MongoDB
    print("\n=== Teste MongoDB ===")
    # Cria uma instância do MongoHandler com a URI e o nome do banco de dados
    mongo = MongoHandler(uri=MONGO_URI, db_name=MONGO_DB)
    test_item = "TestItem" # Nome do item de teste
    test_price = 1.23 # Preço de teste

    # Insere um registro de teste
    mongo.insert_price(test_item, test_price) # Insere o preço do item no MongoDB
    print(f"Inserido preço R$ {test_price:.2f} para '{test_item}'.")

    # Recupera histórico
    history = mongo.get_history(test_item) # Recupera o histórico de preços do item
    print("Histórico retornado:") 
    for record in history: # Percorre todos os registros e imprime cada um
        print(record)

    # Limpa registros de teste
    mongo.delete_history(test_item) # Remove todos os registros do item de teste
    print(f"Registros de '{test_item}' removidos.")
    mongo.close() # Fecha a conexão com o MongoDB


def test_neo4j(): # Função para testar operações básicas no Neo4j
    print("\n=== Teste Neo4j ===")
    # Cria uma instância do Neo4jHandler com a URI, usuário e senha
    neo4j = Neo4jHandler(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASS)
    test_item = "TestItem" # Nome do item de teste
    test_type = "TestType" # Tipo do item de teste
    test_rarity = "TestRarity" # Raridade do item de teste

    # Cria nó de teste
    neo4j.create_item(test_item, test_type, test_rarity) # Cria um nó no Neo4j com o nome, tipo e raridade do item
    print(f"Criado nó de item '{test_item}'.")

    # Recupera item
    item = neo4j.get_item(test_item) # Recupera o nó do item
    print("Item recuperado:", item)

    # Remove nó de teste
    neo4j.delete_item(test_item) # Remove o nó do item de teste
    print(f"Nó de '{test_item}' removido.")
    neo4j.close() # Fecha a conexão com o Neo4j


if __name__ == '__main__': # Executa os testes se o script for executado diretamente
    test_mongo() # Testa operações no MongoDB
    test_neo4j() # Testa operações no Neo4j
