import pandas as pd
import os

def save_file(filename: str) -> str:
    if not os.path.exists("data"):
        os.makedirs("data")
    return f"data/{filename}"

def save_csv(df: pd.DataFrame, filename: str) -> None:
    filename = filename + ".csv"
    df.to_csv(save_file(filename), index=False)
    print(f"Saved {filename} to data directory")
