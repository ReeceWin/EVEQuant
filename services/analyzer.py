from services.sde import get_item_name, get_item_volume, get_location_name

def analyze_orders(sell_orders, buy_orders, ship_volume) -> str:
    ship_volume = ship_volume
    for current_item_id, order_list in sell_orders.items():
        #print("Current item ID: ", current_item_id)
        #print("Order list: ", order_list)
        if order_list != None:
            prices = [order[3] for order in order_list]
            #print("prices: ", prices)
            lowest_price = min(prices)

            buy_order = buy_orders.get(current_item_id)
            print("//////////////////////////////////////////////////////////", buy_order)
            if buy_order != None:
                highest_buy_order = max([bOrder[3] for bOrder in buy_order])
                margin = highest_buy_order - lowest_price
                print("================Margin: ", margin)
            else:
                print("**********************BUY ORDER IS NONE") #WORK IN PROGRESS CONTINUE
            print("lowest_price: ", lowest_price)
            for order in order_list:
                if order[3] == lowest_price:
                    
                    station_name = get_location_name(order[2])
                    break
            item_volume = get_item_volume(current_item_id)
            item_name = get_item_name(current_item_id)
            if item_volume <= ship_volume:
                if item_volume != 0:
                    quantity_needed = int(ship_volume / item_volume)
                else:
                    quantity_needed = 0
                quantity_available = min([order[0], quantity_needed])
                #print("Quantity Needed: ", quantity_needed)
                #print("Quantity Available: ", quantity_available)
                #print("Purchase From: ", station_name)
                #print(item_volume, item_name)
            if item_volume > ship_volume:
                pass
            
            
    