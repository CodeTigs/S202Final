from steam_api import get_item_price # Importa a função get_item_price do módulo steam_api

if __name__ == "__main__":
    # Modo de teste rápido da Steam API
    print("=== Teste Steam API ===")
    item_name = input("Digite o market_hash_name do item: ")
    price, volume = get_item_price(item_name) # Obtém o preço e volume do item
    if price is not None: #se houver um preço para o item
        print(f"Item: {item_name}\nPreço: R$ {price:.2f}\nVolume: {volume}")
    else:
        print(f"Não foi possível obter dados para '{item_name}'.")
