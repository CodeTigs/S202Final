from dotenv import load_dotenv #Dotenv é utilizado para carregar variáveis de ambiente de um arquivo .env
import os #OS é utilizado para acessar variáveis de ambiente
from neo4j import GraphDatabase, basic_auth # Importa as classes necessárias do driver Neo4j
load_dotenv() # Carrega as variáveis de ambiente do arquivo .env
URI      = os.getenv("NEO4J_URI") # recupera a URI do banco Neo4j do arquivo .env
USER     = os.getenv("NEO4J_USER") # recupera o usuário do banco Neo4j do arquivo .env
PASSWORD = os.getenv("NEO4J_PASS") # recupera a senha do banco Neo4j do arquivo .env

class Neo4jHandler:
    """
    Gerencia a conexão e operações CRUD para itens no Neo4j.
    """
    def __init__(self, uri: str, user: str, password: str):
        # Inicializa o driver Neo4j com as credenciais fornecidas.
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))

    def close(self):
        """Fecha a conexão com o banco Neo4j."""
        self.driver.close()

    def create_item(self, name: str, item_type: str, rarity: str):
        """Cria ou atualiza um nó Item com os atributos fornecidos."""
        with self.driver.session() as session: # Abre uma sessão no banco de dados
            # Usa uma transação para garantir que a operação seja atômica
            session.write_transaction(self._create_item_tx, name, item_type, rarity) # Chama a função que cria o item

    @staticmethod # Método estáticos são usados para operações que não dependem do estado da instância
    def _create_item_tx(tx, name, item_type, rarity): # Função que cria o item
        query = (
            "MERGE (i:Item {name: $name}) " # Uso de MERGE para garantir que o nó seja criado ou atualizado
            "SET i.type = $item_type, i.rarity = $rarity"
        )
        tx.run(query, name=name, item_type=item_type, rarity=rarity) #roda a query no banco de dados

    def get_item(self, name: str) -> dict | None:
        """Retorna os atributos de um Item existente ou None se não existir."""
        with self.driver.session() as session: # Abre uma sessão no banco de dados
            result = session.read_transaction(self._get_item_tx, name) #chama a função que busca o item
            return result #retorna o resultado da busca

    @staticmethod
    def _get_item_tx(tx, name): # Função que busca o item pelo nome
        query = (
            "MATCH (i:Item {name: $name}) "
            "RETURN i.name AS name, i.type AS type, i.rarity AS rarity"
        )
        record = tx.run(query, name=name).single() # Executa a query e obtém o primeiro registro
        # Se o registro existir, retorna um dicionário com os atributos do item
        if record:
            return {"name": record["name"], "type": record["type"], "rarity": record["rarity"]}
        return None # Se o registro não existir, retorna None

    def delete_item(self, name: str):
        """Remove um nó Item pelo nome."""
        with self.driver.session() as session: # Abre uma sessão no banco de dados
            session.write_transaction(self._delete_item_tx, name) # Chama a função que deleta o item

    @staticmethod
    def _delete_item_tx(tx, name): # Função que deleta o item pelo nome
        # Usa DETACH DELETE para remover o nó e todos os relacionamentos associados
        tx.run("MATCH (i:Item {name: $name}) DETACH DELETE i", name=name) #roda a query no banco de dados
