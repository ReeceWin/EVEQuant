from services.sde import get_item_name, get_item_volume

def analyze_orders(orders, item_id, ship_volume) -> str:
    ship_volume = ship_volume
    print(type(orders))
    
    #print(orders)
    order_type_id = orders.get(item_id)
    print("order_type_id: ", order_type_id)
    if order_type_id != None:
        prices = [order[3] for order in order_type_id]
        print("prices: ", prices)
        lowest_price = min(prices)
        print("lowest_price: ", lowest_price)
        for order in order_type_id:
            if order[3] == lowest_price:
                print("order: ", order)
                break
        item_volume = get_item_volume(item_id)
        item_name = get_item_name(item_id)
        if item_volume <= ship_volume:
            print("Item volume is less than ship volume")
            print(item_volume, item_name)
        if item_volume > ship_volume:
            print("Item volume is greater than ship volume")
            print(item_volume, item_name)
            
    