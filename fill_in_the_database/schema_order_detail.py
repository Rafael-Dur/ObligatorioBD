import pandas as pd


def fix_prices_and_save(product_csv, order_details_csv, output_csv):
    # Read the CSV files
    df_product = pd.read_csv(product_csv)
    df_order = pd.read_csv(order_details_csv)

    # Merge on id_product
    df_merged = pd.merge(df_order, df_product[['id_product', 'price']], on='id_product',
                         how='left')

    # Keep a trace of original unit_price values
    df_merged['unit_price_original'] = df_merged[
        'unit_price']  # Optional: track changes if needed

    # Correct unit_price using the price from the product table
    df_merged['unit_price'] = df_merged['price']

    # Keep only the original order_details columns (with the corrected price)
    output_columns = ['id_detail', 'id_order', 'id_product', 'amount', 'unit_price']
    df_output = df_merged[output_columns]

    # Save the corrected file
    df_output.to_csv(output_csv, index=False)
    print(f"✅ Corrected file saved as '{output_csv}'")

    return df_output


def clean_unit_price_column(file_path):
    """
    Cleans the 'unit_price' column in a CSV file:
    - Removes '$' symbol and commas.
    - Converts values to float.
    - Saves the file by overwriting the original.
    """
    df = pd.read_csv(file_path)

    if 'unit_price' not in df.columns:
        raise ValueError("❌ The 'unit_price' column does not exist in the file.")

    # Clean and convert to float
    df['unit_price'] = df['unit_price'].replace(r'[\$,]', '', regex=True).astype(float)

    df.to_csv(file_path, index=False)
    print(f"✅ 'unit_price' column cleaned and file overwritten: {file_path}")


def remove_rows_with_zero_amount(file_path):
    df = pd.read_csv(file_path)
    if 'amount' not in df.columns:
        raise ValueError("❌ The 'amount' column does not exist.")

    before = len(df)
    df = df[df['amount'] > 0]
    after = len(df)

    df.to_csv(file_path, index=False)
    print(f"✅ Rows with amount=0 removed: {before - after}")
