from dotenv import load_dotenv
import os
from neo4j import GraphDatabase, basic_auth
load_dotenv()
URI      = os.getenv("NEO4J_URI")
USER     = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASS")

class Neo4jHandler:
    """
    Gerencia a conexão e operações CRUD para itens no Neo4j.
    """
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))

    def close(self):
        """Fecha a conexão com o banco Neo4j."""
        self.driver.close()

    def create_item(self, name: str, item_type: str, rarity: str):
        """Cria ou atualiza um nó Item com os atributos fornecidos."""
        with self.driver.session() as session:
            session.write_transaction(self._create_item_tx, name, item_type, rarity)

    @staticmethod
    def _create_item_tx(tx, name, item_type, rarity):
        query = (
            "MERGE (i:Item {name: $name}) "
            "SET i.type = $item_type, i.rarity = $rarity"
        )
        tx.run(query, name=name, item_type=item_type, rarity=rarity)

    def get_item(self, name: str) -> dict | None:
        """Retorna os atributos de um Item existente ou None se não existir."""
        with self.driver.session() as session:
            result = session.read_transaction(self._get_item_tx, name)
            return result

    @staticmethod
    def _get_item_tx(tx, name):
        query = (
            "MATCH (i:Item {name: $name}) "
            "RETURN i.name AS name, i.type AS type, i.rarity AS rarity"
        )
        record = tx.run(query, name=name).single()
        if record:
            return {"name": record["name"], "type": record["type"], "rarity": record["rarity"]}
        return None

    def delete_item(self, name: str):
        """Remove um nó Item pelo nome."""
        with self.driver.session() as session:
            session.write_transaction(self._delete_item_tx, name)

    @staticmethod
    def _delete_item_tx(tx, name):
        tx.run("MATCH (i:Item {name: $name}) DETACH DELETE i", name=name)
