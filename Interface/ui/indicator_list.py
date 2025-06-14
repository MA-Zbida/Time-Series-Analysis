import pandas as pd
import os
from data import load_data
def get_indicators():
    df = load_data()
    return [col for col in df.columns if col != 'event']
