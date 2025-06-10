if __name__ == "__main__":
    # Modo de teste rápido da Steam API
    print("=== Teste Steam API ===")
    item_name = input("Digite o market_hash_name do item: ")
    price, volume = get_item_price(item_name)
    if price is not None:
        print(f"Item: {item_name}\nPreço: R$ {price:.2f}\nVolume: {volume}")
    else:
        print(f"Não foi possível obter dados para '{item_name}'.")
