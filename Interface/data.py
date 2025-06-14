import pandas as pd
import numpy as np
import os

def load_data():
    try:
        if os.path.exists("data/Morocco.csv"):
            df = pd.read_csv("data/Morocco.csv", index_col=0)
            print(f"Loaded Morocco.csv successfully with {len(df)} rows and {len(df.columns)} columns")
            return df
        else:
            print("Morocco.csv not found. Please make sure the file exists in the current directory.")
            return None
    except Exception as e:
        print(f"Error loading Morocco.csv: {e}")
        return None

def monthly_data():
    return ['brent_oil_prices(USD/barrel)',
            'crude_oil_prices(USD/barrel)',
            'daily_natural_gas_prices(USD/MMBtu)']
    



