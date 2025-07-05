import pandas as pd
import random
from datetime import datetime

def clean_products_and_orders(details_path, orders_path, product_id_to_remove=793):
    # Load CSV files
    details_df = pd.read_csv(details_path)
    orders_df = pd.read_csv(orders_path)

    # Filter details by removing the specified product
    filtered_details = details_df[details_df['id_product'] != product_id_to_remove]

    # Get order IDs that still have details after removing the product
    remaining_order_ids = set(filtered_details['id_order'].unique())
    original_order_ids = set(details_df['id_order'].unique())
    order_ids_to_remove = original_order_ids - remaining_order_ids

    # Filter orders by removing those that no longer have any details
    filtered_orders = orders_df[~orders_df['id_order'].isin(order_ids_to_remove)]

    # Overwrite both files with the cleaned data
    filtered_details.to_csv(details_path, index=False)
    filtered_orders.to_csv(orders_path, index=False)

    print(f"Removed detail rows: {len(details_df) - len(filtered_details)}")
    print(f"Removed orders: {len(orders_df) - len(filtered_orders)}")

def ensure_bazaar_purchase(
    client_path,
    product_path,
    order_path,
    order_details_path
):
    # Load all CSVs
    clients = pd.read_csv(client_path)
    products = pd.read_csv(product_path)
    orders = pd.read_csv(order_path)
    order_details = pd.read_csv(order_details_path)

    # Find bazaar products
    bazaar_products = products[products['category'].str.lower() == 'bazaar']
    if bazaar_products.empty:
        print("No 'bazaar' products found. Aborting.")
        return

    # Get orders joined with details and products
    merged = order_details.merge(orders, on='id_order').merge(products, on='id_product')

    # Check if any client has bought a bazaar product
    has_bazaar = merged[merged['category'].str.lower() == 'bazaar']
    if not has_bazaar.empty:
        print("At least one client has already bought a 'bazaar' product.")
        return

    print("No 'bazaar' purchases found. Adding one...")

    # Pick a random client
    chosen_client = clients.sample(1).iloc[0]

    # Pick a random bazaar product
    chosen_product = bazaar_products.sample(1).iloc[0]

    # Generate next order ID and detail ID
    next_order_id = orders['id_order'].max() + 1
    next_detail_id = order_details['id_detail'].max() + 1

    # Create new order row
    new_order = {
        'id_order': next_order_id,
        'id_client': chosen_client['id_client'],
        'order_date': datetime.now().date().isoformat(),
        'total': chosen_product['price'],
        'state': 'completed'
    }

    # Create new order detail row
    new_detail = {
        'id_detail': next_detail_id,
        'id_order': next_order_id,
        'id_product': chosen_product['id_product'],
        'amount': 1,
        'unit_price': chosen_product['price']
    }

    # Append new records
    orders = pd.concat([orders, pd.DataFrame([new_order])], ignore_index=True)
    order_details = pd.concat([order_details, pd.DataFrame([new_detail])], ignore_index=True)

    # Save updates
    orders.to_csv(order_path, index=False)
    order_details.to_csv(order_details_path, index=False)

    print(f"✔ Added a new order (id: {next_order_id}) for client {chosen_client['id_client']} buying '{chosen_product['product_name']}'")