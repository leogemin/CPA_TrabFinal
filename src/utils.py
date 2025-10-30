import pandas as pd

def load_json_to_df(file_path: str):
  try:
    df = pd.read_json(file_path)
    return df
  except Exception as e:
    print(f"Error loading {file_path}: {e}")
    return None