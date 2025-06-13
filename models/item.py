class Item:
    """
    Representa um item do mercado CS2 para ser armazenado no Neo4j.
    """
    #Construtor da classe
    def __init__(self, name: str, item_type: str, rarity: str):
        self.name = name
        self.item_type = item_type
        self.rarity = rarity

    def __repr__(self):
        return f"<Item name={self.name!r}, type={self.item_type!r}, rarity={self.rarity!r}>"

    def to_dict(self) -> dict:
        """Converte o objeto para dicionário, útil em operações com Neo4j."""
        return {
            "name": self.name,
            "type": self.item_type,
            "rarity": self.rarity
        }
