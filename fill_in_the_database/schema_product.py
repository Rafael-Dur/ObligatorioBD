import pandas as pd

from file_manager import load_df_from_csv


def update_product_stock(output_path):
    inventory_df = load_df_from_csv("data_completed/FINAL_INVENTORY_MOCK_DATA.csv")
    product_df = load_df_from_csv("data/PRODUCT_MOCK_DATA.csv")

    # Group stock by id_product
    stock_sum = inventory_df.groupby('id_product')['current_stock'].sum().reset_index()
    stock_sum.rename(columns={'current_stock': 'stock'}, inplace=True)

    # Remove stock column if it already exists to avoid conflicts
    if 'stock' in product_df.columns:
        product_df = product_df.drop(columns=['stock'])

    # Merge to add the stock column
    updated_product_df = product_df.merge(stock_sum, on='id_product', how='left')

    # Fill missing stock values with 0
    updated_product_df['stock'] = updated_product_df['stock'].fillna(0).astype(int)

    # Save the result
    save_updated_products(updated_product_df, output_path)
    print(f"✅ Product file with updated stock saved at: {output_path}")


def save_updated_products(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"✅ Updated product stock saved to {output_path}")


def clean_price_column(file_path):
    """
    Cleans the 'price' column in a CSV file:
    - Removes the '$' symbol and commas.
    - Converts values to float.
    - Saves the file by overwriting the original.
    """
    df = pd.read_csv(file_path)

    if 'price' not in df.columns:
        raise ValueError("❌ The 'price' column does not exist in the file.")

    # Clean and convert to float
    df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)

    df.to_csv(file_path, index=False)
    print(f"✅ 'price' column cleaned and file overwritten: {file_path}")
