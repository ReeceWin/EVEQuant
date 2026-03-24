from services.sde import get_item_name, get_item_volume, get_location_name
import config

sales_tax = config.sales_tax
broker_fee = config.brokers_fee

def analyze_orders(sell_orders, buy_orders, ship_volume, bubble_list) -> str:
    """
    Analyzes the market orders and returns the best routes for the ship. 
    """
    ship_volume = ship_volume
    profitable_items = []
    for current_item_id, order_list in sell_orders.items():
        if order_list != None:
            prices = [order[3] for order in order_list if order[1] in bubble_list]

            if prices:
                lowest_sell_order = min(prices) 
            else:
                continue
                
            margin = 0
            buy_order = buy_orders.get(current_item_id)

            if buy_order != None:
                buy_prices = [bOrder[3] for bOrder in buy_order if bOrder[1] in bubble_list]
                if buy_prices:
                    highest_buy_order = max(buy_prices)
                    for bOrder in buy_order:
                        if bOrder[3] == highest_buy_order:
                            buy_order_station = get_location_name(bOrder[2])
                    margin = (highest_buy_order * (1 - sales_tax)) - lowest_sell_order
                else:
                    continue
            else:
                pass

            for order in order_list:
                if order[3] == lowest_sell_order:
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
            if item_volume > ship_volume:
                continue

            if margin is not None and margin > 0 and quantity_needed > 0:
                profitable_items.append({
                    "item":item_name, 
                    "item_id":current_item_id,
                    "quantity":quantity_available, 
                    "station_name":station_name, 
                    "buy_order_station":buy_order_station, 
                    "highest_buy_order":highest_buy_order, 
                    "lowest_sell_order":lowest_sell_order, 
                    "margin":margin})
                profitable_items.sort(key=lambda x: x["margin"], reverse=True)
                """
                print("================Item: ", item_name, "================")
                print("================Quantity Available: ", quantity_available, "================")
                print("================Sell Order Location: ", station_name, "================")
                print("================Buy Order Location: ", buy_order_station if buy_order_station else "N/A", "================")
                print("================Highest Buy Order: ", highest_buy_order if highest_buy_order else "N/A", "================")
                print("================lowest_sell_order: ", lowest_sell_order, "================")
                print("================Margin: ", margin, "================")
                print("\n")
                """
    print("Top 10")
    for i in range(10):
        print(profitable_items[i])
            
            
    