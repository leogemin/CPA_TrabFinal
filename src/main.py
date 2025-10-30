import streamlit as st
from utils import load_json_to_df
import pandas as pd

def dataframe_section(df: pd.DataFrame):
  st.write("Tabela de dados utilizada para as análises gráficas:")
  df

def main():
  df = load_json_to_df("./assets/cleanedData.json")
  st.title("Trabalho Extensionista - CPA")
  dataframe_section(df)

if __name__ == "__main__":
  main()