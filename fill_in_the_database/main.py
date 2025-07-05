from adjust_values_for_optimization import clean_products_and_orders, \
    ensure_bazaar_purchase
from file_manager import merge_csvs_with_incremental_id
from schema_inventory import validate_and_fix_id_product, fix_id_product_inventory, \
    convert_stock_to_integer
from schema_order import validate_and_complete_id_order, validate_and_fix_orders, \
    reorder_csv_columns
from schema_order_detail import fix_prices_and_save, clean_unit_price_column, \
    remove_rows_with_zero_amount
from schema_product import update_product_stock, clean_price_column

if __name__ == "__main__":
    # --- Merge client CSVs ---
    merge_csvs_with_incremental_id("data/CLIENT_MOCK_DATA_", 2, "id_cliente",
                                   "data_completed/FINAL_CLIENT_MOCK_DATA.csv")

    # --- Fix duplicate product IDs in inventory data ---
    validate_and_fix_id_product(file_path="data/INVENTORY_MOCK_DATA.csv",
                                output_path="data_completed/FINAL_INVENTORY_MOCK_DATA.csv")

    # --- Update product stock based on inventory data ---
    updated_product_df = update_product_stock(
        "data_completed/FINAL_PRODUCT_MOCK_DATA.csv")

    # --- Merge orders_details incrementally ---
    merge_csvs_with_incremental_id("data/order_details/ORDER_DETAILS_MOCK_DATA_", 190,
                                   "id_detail",
                                   "data/ORDER_DETAILS_MOCK_DATA_MERGED.csv")

    # --- Correct prices in order details ---
    fix_prices_and_save("data_completed/FINAL_PRODUCT_MOCK_DATA.csv",
                        "data/ORDER_DETAILS_MOCK_DATA_MERGED.csv",
                        "data/PRE_FINAL_ORDER_DETAILS_MOCK_DATA.csv")

    # --- Merge orders incrementally ---
    merge_csvs_with_incremental_id("data/orders/COSTUMER_ORDER_", 50, "id_order",
                                   "data/ORDERS_MOCK_DATA_MERGED.csv")

    # --- Validate and correct order IDs ---
    validate_and_complete_id_order(
        order_details_csv="data/PRE_FINAL_ORDER_DETAILS_MOCK_DATA.csv",
        orders_csv="data/ORDERS_MOCK_DATA_MERGED.csv",
        output_csv="data_completed/FINAL_ORDER_DETAILS_MOCK_DATA.csv",
        product_csv="data_completed/FINAL_PRODUCT_MOCK_DATA.csv")

    # --- Validate data consistency ---
    validate_and_fix_orders("data_completed/FINAL_ORDER_DETAILS_MOCK_DATA.csv",
                            "data_completed/FINAL_CLIENT_MOCK_DATA.csv",
                            "data/ORDERS_MOCK_DATA_MERGED.csv",
                            "data_completed/FINAL_ORDER_MOCK_DATA.csv")

    # --- Clean price column in final product data ---
    clean_price_column("data_completed/FINAL_PRODUCT_MOCK_DATA.csv")

    # --- Update product stock based on inventory data ---
    fix_id_product_inventory("data_completed/FINAL_INVENTORY_MOCK_DATA.csv",
                             "data_completed/FINAL_PRODUCT_MOCK_DATA.csv")

    # --- Convert stock to integer in final product data ---
    convert_stock_to_integer("data_completed/FINAL_INVENTORY_MOCK_DATA.csv")

    # --- Update product stock in final product data ---
    reorder_csv_columns(input_path="data_completed/FINAL_ORDER_MOCK_DATA.csv",
                        ordered_columns=["id_order", "id_client", "order_date", "total",
                                         "state"])

    # --- Clean unit_price column in final product data ---
    clean_unit_price_column("data_completed/FINAL_ORDER_DETAILS_MOCK_DATA.csv")

    # --- Remove rows with amount=0 in final order details data ---
    remove_rows_with_zero_amount("data_completed/FINAL_ORDER_DETAILS_MOCK_DATA.csv")

    # --- Clean products and orders data ---
    clean_products_and_orders("data_completed/FINAL_ORDER_DETAILS_MOCK_DATA.csv",
                              "data_completed/FINAL_ORDER_MOCK_DATA.csv")

    # --- Ensure at least one bazaar purchase exists ---
    ensure_bazaar_purchase(client_path="data_completed/FINAL_CLIENT_MOCK_DATA.csv",
                           product_path="data_completed/FINAL_PRODUCT_MOCK_DATA.csv",
                           order_path="data_completed/FINAL_ORDER_MOCK_DATA.csv",
                           order_details_path="data_completed/FINAL_ORDER_DETAILS_MOCK_DATA.csv")
