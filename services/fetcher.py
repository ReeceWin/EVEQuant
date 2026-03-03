from requests import Session
from services.storage import save_json
import json
from datetime import date, datetime
from multiprocessing import Pool
import os

def fetch_all_orders(region_id: int, order_type: str) -> list[dict]:
    """Fetch every page of market orders for a region. Returns a list of order dicts."""
    print("Fetching orders for region: ", region_id)
    lastModifiedDateTime = ""
    metadata = {}
    data = []
    if os.path.exists(f"data/orders_metadata.json"):
        with open(f"data/orders_metadata.json", "r") as f:
            metadata = json.load(f)
            lastModifiedDateTime = metadata.get(f"{region_id}_{order_type}")
    else:
        with open(f"data/orders_metadata.json", "w") as f:
            metadata = {}
            lastModifiedDateTime = ""
    print(lastModifiedDateTime)
    session = Session()

    headers = {'If-Modified-Since': lastModifiedDateTime}
    url = f"https://esi.evetech.net/latest/markets/{region_id}/orders?order_type={order_type}"
    response = session.get(url, headers=headers)
    if response.status_code != 200 and response.status_code != 304:
        raise Exception(f"Failed to fetch orders: {response.text}")

    if response.status_code == 304:
        print("Using cached data: ", region_id)
        return json.load(open(f"data/orders_{region_id}_{order_type}.json"))
    elif response.status_code == 200 and lastModifiedDateTime != response.headers.get("Last-Modified"):
        noOfPages = int(response.headers["X-Pages"])
        lastModifiedDateTime = response.headers["Last-Modified"]
        lastModifiedDateTimeDict = {f"{region_id}_{order_type}": lastModifiedDateTime}
        metadata.update(lastModifiedDateTimeDict)
        save_json(metadata, f"orders_metadata")

        print("Last modified date and time: ", lastModifiedDateTime)
        print("Number of pages: ", noOfPages)

        for page in range(1, noOfPages + 1):
            print(f"=========Fetching Orders for page: {page}=========")
            url = f"https://esi.evetech.net/latest/markets/{region_id}/orders?order_type={order_type}&page={page}"
            response = session.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch orders: {response.text}")
            data.extend(response.json())
        save_json(data, f"orders_{region_id}_{order_type}")
        print(f"Data saved to cache: {region_id}", "using date and time: ", lastModifiedDateTime)

    
    return data