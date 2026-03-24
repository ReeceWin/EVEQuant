import sqlite3
from config import DB_PATH


def get_item_name(item_id: int) -> str:
    """Fetches a single item name safely."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT typeName FROM invTypes WHERE typeID = ?", (item_id,))
        result = cursor.fetchone()
        return result[0] if result else f"Unknown Item ({item_id})"

def get_item_names(item_ids: list[int]) -> dict[int, str]:
    """Fetches multiple names at once (More efficient)."""
    if not item_ids:
        return {}

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        placeholders = ",".join(["?"] * len(item_ids))
        query = f"SELECT typeID, typeName FROM invTypes WHERE typeID IN ({placeholders})"
        
        cursor.execute(query, item_ids)
        return dict(cursor.fetchall())

def get_item_volume(item_id: int) -> float:
    """Fetches a single item volume safely."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(volume, 0) FROM invTypes WHERE typeID = ?", (item_id,))
        result = cursor.fetchone()
        return result[0] if result else 0.0

def get_all_jumps() -> list[tuple[int, int]]:
    """
    Fetches every stargate connection in the universe.
    Returns a list of tuples: (From_System, To_System)
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT fromSolarSystemID, toSolarSystemID FROM mapSolarSystemJumps")
        return cursor.fetchall()

def get_region_for_system(system_id: int) -> str:
    """
    Gets the region_id for the system_id given
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT regionID FROM mapSolarSystems WHERE solarSystemID = ?", (system_id,))
        result = cursor.fetchone()
        return result[0] if result else f"Unknown solarSystemId:({system_id})"

def get_regions_for_system(system_ids: list[int]) -> set[int]:
    """
    Returns all regions for a list of system_ids
    """
    if not system_ids:
        print("Regions for system is none.")
        return set()
    print("regions is not none")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        placeholders = ",".join(["?"] * len(system_ids))
        query = f"SELECT regionID FROM mapSolarSystems WHERE solarSystemID IN ({placeholders})"
        cursor.execute(query, system_ids)
        result = cursor.fetchall()
        regions = set()
        for row in result:
            regions.add(row[0])
    return regions

def get_location_name(location_id: int) -> str:
    """
    Returns the name of the location from the location_id
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT stationName FROM staStations WHERE stationID = ?", (location_id,))
        result = cursor.fetchone()
        return result[0] if result else f"Unknown locationID:({location_id})"

    


