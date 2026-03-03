import pandas as pd
import os
import json

def save_file(filename: str) -> str:
    if not os.path.exists("data"):
        os.makedirs("data")
    return f"data/{filename}"

def save_csv(df: pd.DataFrame, filename: str) -> None:
    filename = filename + ".csv"
    df.to_csv(save_file(filename), index=False)
    print(f"Saved {filename} to data directory")

def save_json(data: dict, filename: str) -> None:
    filename = filename + ".json"
    with open(save_file(filename), "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {filename} to data directory")

def load_json(filename: str) -> dict:
    filename = filename + ".json"
    with open(save_file(filename), "r") as f:
        return json.load(f)
