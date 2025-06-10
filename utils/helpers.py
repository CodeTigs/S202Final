from urllib.parse import quote_plus
from datetime import datetime
import os


def sanitize_item_name(item_name: str) -> str:
    """
    Sanitiza o nome do item para uso em parâmetros de URL (percent-encoding).

    :param item_name: Nome bruto do item
    :return: Nome codificado para URL
    """
    return quote_plus(item_name)


def format_price(price: float) -> str:
    """
    Formata um valor float como string de preço em Real.

    :param price: Valor em float
    :return: Preço formatado, ex: 'R$ 10,50'
    """
    return f"R$ {price:,.2f}".replace(".", ",")


def clear_console():
    """
    Limpa a tela do console.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def format_timestamp(ts: datetime) -> str:
    """
    Formata um timestamp datetime para string legível.

    :param ts: datetime
    :return: String formatada, ex: '2025-06-10 18:00:00'
    """
    return ts.strftime('%Y-%m-%d %H:%M:%S')
