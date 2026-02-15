from requests import Session
import config
import pandas as pd


trade_hub_id = config.trade_hub_id
s = Session()

def fetch_all_orders(region_id: int, session: Session) -> list[dict]:
    """Fetch every page of market orders for a region. Returns a list of order dicts."""
    print("Fetching orders for region: ", region_id)
    url = f"https://esi.evetech.net/latest/markets/{region_id}/orders/?datasource=tranquility&page=1"

    response = session.get(url)
    
    noOfPages = int(response.headers["X-Pages"])
    print("Number of pages: ", noOfPages)
    data = []
    for page in range(1, noOfPages + 1):
        print(f"=========Fetching Orders for page: {page}=========")
        url = f"https://esi.evetech.net/latest/markets/{region_id}/orders/?datasource=tranquility&page={page}"
        response = session.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch orders: {response.text}")
        data.extend(response.json())
    return data

def create_dataframe(json: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(json)
    df['issued'] = pd.to_datetime(df['issued'])

    print(df.head())
    print(df.shape)
    print(df.dtypes)
    
    buy_orders = df[df['is_buy_order'] == True].copy()
    sell_orders = df[df['is_buy_order'] == False].copy()

    buy_orders.to_csv("buy_orders.csv", index=False)
    sell_orders.to_csv("sell_orders.csv", index=False)

    print("Buy orders max price: ", buy_orders['price'].max())
    print("Buy orders min price: ", buy_orders['price'].min())
    print("Buy orders mean price: ", buy_orders['price'].mean())
    print("Sell orders max price: ", sell_orders['price'].max())
    print("Sell orders min price: ", sell_orders['price'].min())
    print("Sell orders mean price: ", sell_orders['price'].mean())
    
    df.to_csv("orders.csv", index=False)    
    return df, buy_orders, sell_orders

def iqr_filter(group):
    if len(group) < 10:
        return group
    else:
        q1 = group['price'].quantile(0.25)
        q3 = group['price'].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
    return group[(group['price'] >= lower_bound) & (group['price'] <= upper_bound)]

def main():
    # Fetch all orders
    orders = fetch_all_orders(10000033, s)
    sell_orders = create_dataframe(orders)[2]
    buy_orders = create_dataframe(orders)[1]
    
    # Filter out outliers
    print("Filtering out outliers...")
    print("Sell orders shape: ", sell_orders.shape[0])
    print("Sell orders min price: ", sell_orders['price'].min())
    print("Sell orders max price: ", sell_orders['price'].max())
    print("Sell orders mean price: ", sell_orders['price'].mean())
    print("Buy orders shape: ", buy_orders.shape[0])
    print("Buy orders min price: ", buy_orders['price'].min())
    print("Buy orders max price: ", buy_orders['price'].max())
    print("Buy orders mean price: ", buy_orders['price'].mean())
    clean_sells = sell_orders.groupby('type_id', group_keys=False).apply(iqr_filter)
    clean_buys = buy_orders.groupby('type_id', group_keys=False).apply(iqr_filter)
    print("Clean sells shape: ", clean_sells.shape[0])
    print("Clean sells min price: ", clean_sells['price'].min())
    print("Clean sells max price: ", clean_sells['price'].max())
    print("Clean sells mean price: ", clean_sells['price'].mean())
    print("Clean buys shape: ", clean_buys.shape[0])
    print("Clean buys min price: ", clean_buys['price'].min())
    print("Clean buys max price: ", clean_buys['price'].max())
    print("Clean buys mean price: ", clean_buys['price'].mean())
    big_item = clean_sells[clean_sells['price'] == 700000000000.0]
    print(big_item)
    print(clean_sells[clean_sells['type_id'] == big_item['type_id'].values[0]].shape[0])
    # Create dataframe
    

main()







"""
response = s.get(f"https://esi.evetech.net/latest/markets/prices/?region_id={trade_hub_id}")

print(response.json())

df = pd.DataFrame(response.json())

print(df.head())
"""