import pandas as pd
from services.fetcher import fetch_all_orders
from services.converters import json_to_df, df_to_buy, df_to_sell
from services.storage import save_csv
from services.filters import iqr_filter
import config
from requests import Session

def fetch_all_regions(region_id: list[int]) -> None:
    orders = []
    session = Session()
    for region in region_id:
        orders.extend(fetch_all_orders(region, session))
    
    df = json_to_df(orders)

    buy_orders = df_to_buy(df)
    sell_orders = df_to_sell(df)

    save_csv(buy_orders, "buy_orders")
    save_csv(sell_orders, "sell_orders")
    
    clean_buy_orders = buy_orders.groupby('type_id', group_keys=False).apply(iqr_filter, 'price')
    clean_sell_orders = sell_orders.groupby('type_id', group_keys=False).apply(iqr_filter, 'price')
    
    save_csv(clean_buy_orders, "clean_buy_orders")
    save_csv(clean_sell_orders, "clean_sell_orders")

if __name__ == "__main__":
    fetch_all_regions(config.regions)