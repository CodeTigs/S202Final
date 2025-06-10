# steam/steam_api.py

import requests
from typing import Tuple, Optional
from urllib.parse import quote_plus


def get_item_price(
    item_name: str,
    appid: int = 730,
    currency: int = 7,
    timeout: int = 10
) -> Tuple[Optional[float], Optional[int]]:
    """
    Consulta o preço mais baixo (lowest_price) ou médio (median_price) e o volume de um item no mercado Steam.

    :param item_name: market_hash_name do item (texto legível)
    :param appid: ID do aplicativo Steam (default: 730 para CS2)
    :param currency: código de moeda (default: 7 para BRL)
    :param timeout: tempo máximo de espera pela resposta em segundos
    :return: Tupla (price, volume) ou (None, None) se falhar
    """
    url = "https://steamcommunity.com/market/priceoverview/"
    params = {
        'appid': appid,
        'currency': currency,
        'market_hash_name': item_name
    }

    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return None, None

    # Tenta usar lowest_price, se não disponível usa median_price
    raw_price = data.get('lowest_price') or data.get('median_price')
    raw_volume = data.get('volume')

    if not data.get('success', False) or not raw_price:
        return None, None

    # Remove símbolo e formata: 'R$ 286,78' -> '286.78'
    price_str = (
        raw_price
        .replace('R$', '')
        .replace(' ', '')
        .replace('.', '')
        .replace(',', '.')
    )
    try:
        price = float(price_str)
    except ValueError:
        return None, None

    # Converte volume em int
    try:
        volume = int(raw_volume) if raw_volume is not None else None
    except (TypeError, ValueError):
        volume = None

    return price, volume


if __name__ == '__main__':
    print('=== Teste Steam API ===')
    nome = input('Digite market_hash_name: ')
    preco, vol = get_item_price(nome)
    if preco is not None:
        print(f"Item: {nome}\nPreço: R$ {preco:.2f}\nVolume: {vol}")
    else:
        print(f"Falha ao obter dados para '{nome}'")
