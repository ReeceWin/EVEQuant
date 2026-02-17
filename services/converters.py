import pandas as pd

def json_to_df(json: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(json)
    df['issued'] = pd.to_datetime(df['issued'])
    return df

def df_to_buy(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['is_buy_order'] == True].copy()

def df_to_sell(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['is_buy_order'] == False].copy()

