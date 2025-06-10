# test_db.py

"""
Script de teste para verificar conexões e operações básicas em MongoDB e Neo4j.
Execute: python test_db.py
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
# Renomeie dotenv.env para .env na raiz do projeto
load_dotenv()

# Parâmetros MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "steam_market")

# Parâmetros Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "senha")

# Debug: imprimir variáveis de ambiente para verificação de carregamento
print(f">>> MONGO_URI = {MONGO_URI}")
print(f">>> MONGO_DB  = {MONGO_DB}")
print(f">>> NEO4J_URI= {NEO4J_URI}")
print(f">>> NEO4J_USER= {NEO4J_USER}")
print(f">>> NEO4J_PASS= {NEO4J_PASS}")

# Importa handlers após carregar e imprimir variáveis
from database.mongo_handler import MongoHandler
from database.neo4j_handler import Neo4jHandler


def test_mongo():
    print("\n=== Teste MongoDB ===")
    mongo = MongoHandler(uri=MONGO_URI, db_name=MONGO_DB)
    test_item = "TestItem"
    test_price = 1.23

    # Insere um registro de teste
    mongo.insert_price(test_item, test_price)
    print(f"Inserido preço R$ {test_price:.2f} para '{test_item}'.")

    # Recupera histórico
    history = mongo.get_history(test_item)
    print("Histórico retornado:")
    for record in history:
        print(record)

    # Limpa registros de teste
    mongo.delete_history(test_item)
    print(f"Registros de '{test_item}' removidos.")
    mongo.close()


def test_neo4j():
    print("\n=== Teste Neo4j ===")
    neo4j = Neo4jHandler(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASS)
    test_item = "TestItem"
    test_type = "TestType"
    test_rarity = "TestRarity"

    # Cria nó de teste
    neo4j.create_item(test_item, test_type, test_rarity)
    print(f"Criado nó de item '{test_item}'.")

    # Recupera item
    item = neo4j.get_item(test_item)
    print("Item recuperado:", item)

    # Remove nó de teste
    neo4j.delete_item(test_item)
    print(f"Nó de '{test_item}' removido.")
    neo4j.close()


if __name__ == '__main__':
    test_mongo()
    test_neo4j()
