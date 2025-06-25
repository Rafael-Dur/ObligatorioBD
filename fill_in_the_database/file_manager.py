import pandas as pd

def merge_csvs_with_incremental_id(prefix, count, id_column, output_path=None):
    """
    Merges multiple CSV files with a common prefix and reassigns the ID column incrementally.

    Parameters:
    - prefix (str): common file prefix (e.g., 'data/COSTUMER_ORDER_').
    - count (int): number of files to merge (e.g., 50).
    - id_column (str): name of the ID column to reassign (e.g., 'id_order').
    - output_path (str): path to save the combined file. If None, it won't be saved.

    Returns:
    - Combined DataFrame.
    """
    dataframes = []

    for i in range(1, count + 1):
        file_name = f"{prefix}{i}.csv"
        df = pd.read_csv(file_name)
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    if id_column in combined_df.columns:
        combined_df[id_column] = range(1, len(combined_df) + 1)
    else:
        raise ValueError(f"The column '{id_column}' does not exist in the files.")

    if output_path:
        combined_df.to_csv(output_path, index=False)
        print(f"✅ Combined file saved at: {output_path}")

    return combined_df

def load_df_from_csv(csv_path):
    """Loads a CSV into a DataFrame."""
    csv_df = pd.read_csv(csv_path)
    return csv_df
