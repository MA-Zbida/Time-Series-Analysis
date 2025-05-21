import numpy as np
import pandas as pd

def get_indicators(df = pd.read_csv("Morocco.csv", index_col=0)):
    columns = [col for col in df.columns if col != "event"]

    return columns

print(get_indicators())