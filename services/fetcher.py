from requests import Session
from services.storage import save_json
import json

def fetch_all_orders(region_id: int, order_type: str) -> list[dict]:
    """Fetch every page of market orders for a region. Returns a list of order dicts."""
    print("Fetching orders for region: ", region_id)

    session = Session()

    url = f"https://esi.evetech.net/latest/markets/{region_id}/orders?order_type={order_type}"
    response = session.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch orders: {response.text}")
    
    noOfPages = int(response.headers["X-Pages"])
    lastModifiedDateTime = response.headers["Last-Modified"]
    if "Last-Modified" in response.headers and response.headers["Last-Modified"] != lastModifiedDateTime:
        print("Last modified date and time: ", lastModifiedDateTime)
        print("Number of pages: ", noOfPages)
        data = []
        for page in range(1, noOfPages + 1):
            print(f"=========Fetching Orders for page: {page}=========")
            url = f"https://esi.evetech.net/latest/markets/{region_id}/orders?order_type={order_type}&page={page}"
            response = session.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch orders: {response.text}")
            data.extend(response.json())
        save_json(data, f"orders_{region_id}")
        print(f"Data saved to cache: {region_id}", "using date and time: ", lastModifiedDateTime)
    else:
        print(f"Using cached data: {region_id}")
        data = json.load(open(f"data/orders_{region_id}.json"))
    
    return data