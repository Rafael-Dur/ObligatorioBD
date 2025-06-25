import random
import pandas as pd

# === Helper function 1: fix order dates ===
def fix_order_dates(df_orders, df_clients):
    df = pd.merge(
        df_orders,
        df_clients[['id_client', 'registration_date']],
        left_on='id_client',
        right_on='id_client',
        how='left'
    )

    df['order_date'] = pd.to_datetime(df['order_date'])
    df['registration_date'] = pd.to_datetime(df['registration_date'])

    df['order_date'] = df.apply(
        lambda row: row['registration_date'] if row['order_date'] < row['registration_date'] else row['order_date'],
        axis=1
    )

    return df.drop(columns=['registration_date'])

# === Helper function 2: add total column ===
def add_total_column(df_orders, df_order_details):
    # Clean and convert to float
    df_order_details['unit_price'] = df_order_details['unit_price'].replace(r'[\$,]', '', regex=True).astype(float)
    df_order_details['amount'] = df_order_details['amount'].astype(float)

    # Ensure id_order has the same type
    df_orders['id_order'] = df_orders['id_order'].astype(int)
    df_order_details['id_order'] = df_order_details['id_order'].astype(int)

    # Calculate total per order
    df_totals = (
        df_order_details
        .assign(total=lambda df: df['unit_price'] * df['amount'])
        .groupby('id_order')['total']
        .sum()
        .reset_index()
    )

    # Merge with orders to add total column
    df_orders = pd.merge(df_orders, df_totals, on='id_order', how='left')

    return df_orders

# === Main function ===
def validate_and_fix_orders(order_details_csv, client_csv, orders_csv, output_csv):
    # Load CSVs
    df_order_details = pd.read_csv(order_details_csv)
    df_clients = pd.read_csv(client_csv)
    df_orders = pd.read_csv(orders_csv)

    # Apply corrections
    df_orders = fix_order_dates(df_orders, df_clients)
    df_orders = add_total_column(df_orders, df_order_details)

    # Save final result
    df_orders.to_csv(output_csv, index=False)
    print(f"✅ Final file successfully generated: {output_csv}")

    return df_orders

def validate_and_complete_id_order(order_details_csv, orders_csv, output_csv, product_csv=None):
    # Load files
    df_order_details = pd.read_csv(order_details_csv)
    df_orders = pd.read_csv(orders_csv)

    # Ensure id_order has the same type (int)
    df_order_details['id_order'] = df_order_details['id_order'].astype(int)
    df_orders['id_order'] = df_orders['id_order'].astype(int)

    # Valid id_order list
    valid_order_ids = list(df_orders['id_order'].unique())

    # === Step 1: Fix invalid id_order values ===
    invalid_mask = ~df_order_details['id_order'].isin(valid_order_ids)
    num_invalid = invalid_mask.sum()

    if num_invalid > 0:
        print(f"⚠️ Found {num_invalid} invalid id_order values. They will be replaced.")
        df_order_details.loc[invalid_mask, 'id_order'] = [
            random.choice(valid_order_ids) for _ in range(num_invalid)
        ]
    else:
        print("✅ All id_order values in order_details are valid.")

    # === Step 2: Add missing orders that are not in order_details ===
    present_orders = set(df_order_details['id_order'])
    missing_orders = set(valid_order_ids) - present_orders
    num_missing = len(missing_orders)

    print(f"🔍 Found {num_missing} id_order values not present in order_details. They will be added.")

    # Get a valid id_product if product CSV is provided
    valid_product_id = 1
    if product_csv:
        df_products = pd.read_csv(product_csv)
        if not df_products.empty:
            valid_product_id = random.choice(df_products['id_product'].astype(int).tolist())

    # Calculate last id_detail
    max_id_detail = df_order_details['id_detail'].max() if not df_order_details.empty else 0

    # Create new rows
    new_rows = []
    for i, id_order in enumerate(missing_orders, start=1):
        new_rows.append({
            'id_detail': max_id_detail + i,
            'id_order': id_order,
            'id_product': valid_product_id,
            'amount': 0,
            'unit_price': 0
        })

    if new_rows:
        df_new = pd.DataFrame(new_rows)
        df_order_details = pd.concat([df_order_details, df_new], ignore_index=True)

    # Save result
    df_order_details.to_csv(output_csv, index=False)
    print(f"✅ Fixed and completed file saved as: {output_csv}")

    return df_order_details

def reorder_csv_columns(input_path, ordered_columns, output_path=None):
    """
    Reorders the columns of a CSV file according to the specified order.

    Parameters:
    - input_path: Path to the original CSV file.
    - ordered_columns: List with the desired column order.
    - output_path: Path to save the reordered CSV. If None, overwrites the original.
    """
    df = pd.read_csv(input_path)

    # Validate that all specified columns exist in the file
    missing = [col for col in ordered_columns if col not in df.columns]
    if missing:
        raise ValueError(f"❌ Missing columns in the CSV: {missing}")

    df = df[ordered_columns]

    destination = output_path or input_path
    df.to_csv(destination, index=False)

    print(f"✅ CSV reordered and saved to: {destination}")
