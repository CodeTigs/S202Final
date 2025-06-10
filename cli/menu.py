# cli/menu.py

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

from steam.steam_api import get_item_price
from database.mongo_handler import MongoHandler
from database.neo4j_handler import Neo4jHandler
from models.price_history import PriceHistory
from models.item import Item


def menu():
    """
    Menu principal de operações CRUD via console.
    """
    # Ler configurações do .env
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB = os.getenv("MONGO_DB", "steam_market")
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASS = os.getenv("NEO4J_PASS", "senha")

    # Instancia handlers com configurações dinâmicas
    mongo = MongoHandler(uri=MONGO_URI, db_name=MONGO_DB)
    neo4j = Neo4jHandler(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASS)

    try:
        while True:
            print("\n=== Steam Market CLI ===")
            print("1. Buscar item e salvar preço")
            print("2. Ver histórico de preços")
            print("3. Cadastrar item no Neo4j")
            print("4. Excluir histórico de preços")
            print("5. Excluir item do Neo4j")
            print("6. Sair")
            choice = input("Escolha uma opção: ")

            if choice == "1":
                name = input("Nome do item (market_hash_name): ")
                price, volume = get_item_price(name)
                if price is not None:
                    mongo.insert_price(name, price)
                    print(f"Preço R$ {price:.2f} salvo com sucesso! Volume: {volume}")
                else:
                    print("Não foi possível obter o preço do item.")

            elif choice == "2":
                name = input("Nome do item para histórico: ")
                history = mongo.get_history(name)
                if history:
                    for record in history:
                        print(f"{record['timestamp']}: R$ {record['price']}")
                else:
                    print("Nenhum registro de preço encontrado.")

            elif choice == "3":
                name = input("Nome do item: ")
                type_ = input("Tipo do item: ")
                rarity = input("Raridade do item: ")
                neo4j.create_item(name, type_, rarity)
                print("Item cadastrado/atualizado no Neo4j com sucesso!")

            elif choice == "4":
                name = input("Nome do item para excluir histórico: ")
                mongo.delete_history(name)
                print("Histórico de preços excluído com sucesso.")

            elif choice == "5":
                name = input("Nome do item para exclusão no Neo4j: ")
                neo4j.delete_item(name)
                print("Item excluído do Neo4j com sucesso.")

            elif choice == "6":
                print("Saindo...")
                break

            else:
                print("Opção inválida. Tente novamente.")

    finally:
        mongo.close()
        neo4j.close()


if __name__ == '__main__':
    menu()
