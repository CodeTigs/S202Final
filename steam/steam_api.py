# steam/steam_api.py

import requests #requests é utilizado para fazer requisições HTTP
from typing import Tuple, Optional #Tuple e Optional são utilizados para definir tipos de retorno
#Tuple é usado para retornar múltiplos valores de uma função
#Optional é usado para indicar que um valor pode ser None
from urllib.parse import quote_plus #quote_plus é utilizado para codificar a string do nome do item para ser usada na URL


def get_item_price(
    item_name: str, # nome do item no formato market_hash (ex: "AK-47 | Redline (Field-Tested)")
    appid: int = 730, # ID do aplicativo Steam (default: 730 para CS2)
    currency: int = 7, # Código de moeda (default: 7 para BRL)
    timeout: int = 10 # Tempo máximo de espera pela resposta em segundos (default: 10)
) -> Tuple[Optional[float], Optional[int]]: # Tupla com preço (float) e volume (int), ambos opcionais
    """
    Consulta o preço mais baixo (lowest_price) ou médio (median_price) e o volume de um item no mercado Steam.

    :param item_name: market_hash_name do item (texto legível)
    :param appid: ID do aplicativo Steam (default: 730 para CS2)
    :param currency: código de moeda (default: 7 para BRL)
    :param timeout: tempo máximo de espera pela resposta em segundos
    :return: Tupla (price, volume) ou (None, None) se falhar
    """
    url = "https://steamcommunity.com/market/priceoverview/" # URL da API Steam para obter preços
    params = { # Dicionário com os parâmetros da requisição
        'appid': appid,
        'currency': currency,
        'market_hash_name': item_name
    }

    try: # Tenta fazer a requisição para a API Steam
        response = requests.get(url, params=params, timeout=timeout) # Faz a requisição GET para a API Steam
        response.raise_for_status() # Verifica se a resposta foi bem-sucedida (código 200)
        data = response.json() # Converte a resposta JSON em um dicionário Python
    except (requests.RequestException, ValueError): # Captura erros de requisição ou de conversão JSON
        return None, None # Se ocorrer erro na requisição ou na conversão JSON, retorna None
    # Se a resposta não contiver os dados esperados, retorna None

    # Tenta usar lowest_price, se não disponível usa median_price
    raw_price = data.get('lowest_price') or data.get('median_price') # Obtém o preço mais baixo ou o preço médio do item
    raw_volume = data.get('volume') # Obtém o volume do item

    if not data.get('success', False) or not raw_price: # Verifica se a resposta foi bem-sucedida e se há preço disponível
        return None, None # Se a resposta não for bem-sucedida ou não houver preço, retorna None

    # Remove símbolo e formata: 'R$ 286,78' -> '286.78'
    price_str = (
        raw_price
        .replace('R$', '') # Remove o símbolo de Real
        .replace(' ', '') # Remove espaços em branco
        .replace('.', '') # Remove pontos (separador de milhar)
        .replace(',', '.') # Substitui vírgula por ponto (separador decimal)
    )
    try: # Tenta converter a string de preço para float
        price = float(price_str) # Converte a string de preço para float
    except ValueError: # Se falhar na conversão, captura o erro
        return None, None # Se falhar na conversão, retorna None

    # Converte volume em int
    try: # Tenta converter o volume para int
        volume = int(raw_volume) if raw_volume is not None else None # Tenta converter volume para int, se não for None
    except (TypeError, ValueError): # Se falhar na conversão, define volume como None
        volume = None

    return price, volume


if __name__ == '__main__': # Executa o teste se o script for executado diretamente
    print('=== Teste Steam API ===')
    nome = input('Digite market_hash_name: ') # O usuário deve inserir o nome do item corretamente
    preco, vol = get_item_price(nome) #Recupera o preço e volume do item
    if preco is not None: # Verifica se o preço foi obtido com sucesso
        print(f"Item: {nome}\nPreço: R$ {preco:.2f}\nVolume: {vol}") # Exibe o preço formatado e o volume
    else:
        print(f"Falha ao obter dados para '{nome}'") # Exibe mensagem de erro se não conseguir obter os dados
