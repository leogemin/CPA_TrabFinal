import pandas as pd
import json
import streamlit as st

def load_json_to_df(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

def dataframe_section(df: pd.DataFrame):
  st.dataframe(df)
