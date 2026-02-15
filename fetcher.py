from requests import Session

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