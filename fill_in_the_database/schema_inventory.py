import random
import pandas as pd

def validate_and_fix_id_product(file_path, output_path, min_val=1, max_val=1000):
    """
    Validates and fixes the 'id_product' column:
    - Replaces duplicate or out-of-range IDs with new unique valid ones
    - Saves the corrected DataFrame to output_path
    """
    df = pd.read_csv(file_path)

    if "id_product" not in df.columns:
        raise ValueError("❌ The column 'id_product' does not exist in the file.")

    existing_ids = df["id_product"]
    new_ids = []
    used = set()
    available = list(set(range(min_val, max_val + 1)))

    # Remove already used valid IDs from the set of available ones
    for id_val in existing_ids:
        if id_val in used or not (min_val <= id_val <= max_val):
            new_ids.append(None)  # mark as needing replacement
        else:
            new_ids.append(id_val)
            used.add(id_val)
            if id_val in available:
                available.remove(id_val)

    # Replace the None values with new unique valid IDs
    available_iter = iter(sorted(available))
    for i in range(len(new_ids)):
        if new_ids[i] is None:
            try:
                new_ids[i] = next(available_iter)
            except StopIteration:
                raise ValueError("❌ Not enough available IDs to fix all conflicts.")

    df["id_product"] = new_ids
    df.to_csv(output_path, index=False)

    print(f"✅ Corrected file saved at: {output_path}")
    return df

def fix_id_product_inventory(inventory_path, product_path):
    """
    Fixes the values of id_product in FINAL_INVENTORY_MOCK_DATA.csv:
    - Replaces duplicate or invalid product IDs.
    - Ensures all id_product values are unique and valid.
    - Converts the IDs to integer type.
    """
    df_inventory = pd.read_csv(inventory_path)
    df_product = pd.read_csv(product_path)

    if 'id_product' not in df_inventory.columns or 'id_product' not in df_product.columns:
        raise ValueError("❌ Both files must contain an 'id_product' column.")

    # Convert to integers (in case they are floats)
    df_inventory['id_product'] = df_inventory['id_product'].astype(int)
    df_product['id_product'] = df_product['id_product'].astype(int)

    valid_ids = set(df_product['id_product'].tolist())
    used_ids = set()
    corrected_ids = []

    for id_val in df_inventory['id_product']:
        if id_val in valid_ids and id_val not in used_ids:
            corrected_ids.append(id_val)
            used_ids.add(id_val)
        else:
            # Look for a new valid and unused ID
            available = list(valid_ids - used_ids)
            if not available:
                raise ValueError("❌ No more valid IDs available to assign.")
            new_id = random.choice(available)
            corrected_ids.append(new_id)
            used_ids.add(new_id)

    # Assign and enforce integer type
    df_inventory['id_product'] = pd.Series(corrected_ids, dtype=int)

    # Save
    df_inventory.to_csv(inventory_path, index=False)
    print(f"✅ id_product fixed and file overwritten: {inventory_path}")

def convert_stock_to_integer(file_path):
    """
    Converts the 'current_stock' column to integer type in a CSV file.
    Overwrites the original file with the corrected values.
    """
    df = pd.read_csv(file_path)

    if 'current_stock' not in df.columns:
        raise ValueError("❌ The 'current_stock' column does not exist in the file.")

    # Convert to int (removes .0 decimals if present)
    df['current_stock'] = df['current_stock'].astype(int)

    df.to_csv(file_path, index=False)
    print(f"✅ 'current_stock' column converted to integer and file overwritten: {file_path}")