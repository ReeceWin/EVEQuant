import sqlite3
  # Assuming we might put the DB path here later

DB_PATH = "eve.db"

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

def get_all_jumps() -> list[tuple[int, int]]:
    """
    Fetches every stargate connection in the universe.
    Returns a list of tuples: (From_System, To_System)
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT fromSolarSystemID, toSolarSystemID FROM mapSolarSystemJumps")
        return cursor.fetchall()