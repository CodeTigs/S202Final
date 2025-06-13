from pymongo import MongoClient #Pymongo é utilizado para interagir com o MongoDB
from datetime import datetime #Datetime é utilizado para manipulação de datas e horas

from dotenv import load_dotenv #Dotenv é utilizado para carregar variáveis de ambiente de um arquivo .env
import os #OS é utilizado para acessar variáveis de ambiente

load_dotenv() # Carrega as variáveis de ambiente do arquivo .env
MONGO_URI = os.getenv("MONGO_URI") # recupera a URI do MongoDB do arquivo .env

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
        timestamp = timestamp or datetime.now() # Usa o timestamp atual se não for fornecido
        doc = {
            "item": item_name,
            "price": price,
            "timestamp": timestamp
        }
        self.collection.insert_one(doc) # Insere o documento no MongoDB

    def get_history(self, item_name: str):
        """
        Retorna uma lista de registros de preço de um item, ordenados por timestamp ascendente.

        :param item_name: Nome do item
        :return: Lista de documentos
        """
        return list(self.collection.find({"item": item_name}).sort("timestamp", 1)) # Ordena por timestamp ascendente

    def delete_history(self, item_name: str):
        """
        Remove todos os registros de preço de um item.

        :param item_name: Nome do item
        """
        self.collection.delete_many({"item": item_name}) # Remove todos os documentos com o nome do item especificado
