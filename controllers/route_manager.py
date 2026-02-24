from services.sde import get_region_for_system, get_regions_for_system
from services.router import get_systems_in_range, find_route
from services.fetcher import fetch_all_orders


def group_orders_by_item(orders):
    market_data = {}
    for order in orders:
        type_id = order['type_id']
        if type_id not in market_data:
            market_data[type_id] = []
        market_data[type_id].append([order['volume_remain'],order['system_id'],order['price']])
    return market_data

def analyze_route(start_system, end_system, jump_radius):
    route = find_route(start_system, end_system)
    bubble = set()
    for system in route:
        systems = get_systems_in_range(system, jump_radius)
        bubble.update(systems)
        print(bubble)
    bubble_list = list(bubble)
    regions = get_regions_for_system(bubble_list)
    print(regions)

    all_orders = []
    for region in regions:
        orders = fetch_all_orders(region, "sell")
        all_orders.extend(orders)
    
    grouped_orders = group_orders_by_item(all_orders)

    grouped_orders_length = len(grouped_orders)
    print("Number of unique items: ", grouped_orders_length)
    return grouped_orders

def get_item_prices(grouped_orders):
    best_prices = {}
    for item_id in grouped_orders:
        #print(grouped_orders[item_id])
        lowest_price = min(grouped_orders[item_id], key=lambda x: x[2])
        best_prices[item_id] = lowest_price
    return best_prices
        
    
