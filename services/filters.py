import pandas as pd

def iqr_filter(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Filter out outliers using the IQR method."""
    if len(df) < 10:
        return df
    else:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
