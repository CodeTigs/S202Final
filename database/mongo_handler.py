from pymongo import MongoClient
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

class MongoHandler:
    """
    Gerencia conexão e operações no MongoDB para histórico de preços.
    """
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "steam_market"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["price_history"]

    def close(self):
        """Fecha a conexão com MongoDB."""
        self.client.close()

    def insert_price(self, item_name: str, price: float, timestamp: datetime = None):
        """
        Insere um registro de preço no histórico.

        :param item_name: Nome do item
        :param price: Preço do item
        :param timestamp: Data e hora do registro (default: agora)
        """
        timestamp = timestamp or datetime.now()
        doc = {
            "item": item_name,
            "price": price,
            "timestamp": timestamp
        }
        self.collection.insert_one(doc)

    def get_history(self, item_name: str):
        """
        Retorna uma lista de registros de preço de um item, ordenados por timestamp ascendente.

        :param item_name: Nome do item
        :return: Lista de documentos
        """
        return list(self.collection.find({"item": item_name}).sort("timestamp", 1))

    def delete_history(self, item_name: str):
        """
        Remove todos os registros de preço de um item.

        :param item_name: Nome do item
        """
        self.collection.delete_many({"item": item_name})
