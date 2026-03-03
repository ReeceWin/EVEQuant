from controllers.route_manager import analyze_route, get_item_prices
from services.analyzer import analyze_orders

def main():
    start_system = 30000142
    end_system = 30002187
    jump_radius = 2
    grouped_orders = analyze_route(start_system=start_system, end_system=end_system, jump_radius=jump_radius)
    #get_item_prices(grouped_orders)
    get_item_prices(grouped_orders)
    analyze_orders(grouped_orders, 34, 10000)

main()