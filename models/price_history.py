from datetime import datetime # Importa datetime para manipulação de datas e horas

class PriceHistory:
    """
    Representa um registro de preço de um item no mercado CS2 para ser armazenado no MongoDB.
    """
    #Construtor da classe
    def __init__(self, item_name: str, price: float, timestamp: datetime = None):
        self.item_name = item_name
        self.price = price
        self.timestamp = timestamp or datetime.now() # Usa o timestamp atual se não for fornecido

    def to_dict(self) -> dict:
        """
        Converte o objeto para dicionário, útil para operações com MongoDB.
        """
        return {
            "item": self.item_name,
            "price": self.price,
            "timestamp": self.timestamp
        }

    def __repr__(self): # Representação do objeto para facilitar o debug
        return f"<PriceHistory item={self.item_name!r}, price={self.price!r}, timestamp={self.timestamp!r}>"
