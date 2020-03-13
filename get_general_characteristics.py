import pandas as pd

def get_general_characteristics(path_to_df_file_in_csv,
                                product_column_name,
                                user_column_name,
                                quantity_column_name,
                                date_column_name,
                                transactions_column_name,
                                total_price_column_name,
                                threashold_active_products = 1,
                                threashold_active_users = 1):
    df = pd.read_csv(path_to_df_file_in_csv)
    df[date_column_name] = pd.to_datetime(df[date_column_name])
    df_grouped_by_customer_and_product = df.groupby([user_column_name, product_column_name], as_index=False)[
        quantity_column_name].sum()
    df_grouped_by_transaction_and_product = df.groupby([transactions_column_name, product_column_name], as_index=False)[
        quantity_column_name].sum()

    number_of_products = len(df[product_column_name].unique())
    number_of_transactions = len(df[transactions_column_name].unique())
    number_of_customers = len(df[user_column_name].unique())
    time_duration_in_days = (df[date_column_name].max() - df[date_column_name].min()).days
    #df_grouped_by_customer_and_product.shape[0]

    dict_general_characteristics = {
        'time_duration_in_days': time_duration_in_days,

        'number_of_purchases': len(df),
        'number_of_transactions': number_of_transactions,

        'number_of_products': number_of_products,
        'number_of_customers': number_of_customers,

        'average_number_of_purchases_per_customer': len(df)/number_of_customers,
        'average_number_of_transactions_per_customer': number_of_transactions / number_of_customers, #visits
        'average month/week visits': 0,

        'number_of_interactions': len(
            df_grouped_by_customer_and_product),
        'sparsity': len(df_grouped_by_customer_and_product) / (number_of_products * number_of_customers),
        'average_length_of_unique_products_per_customer': len(
            df_grouped_by_customer_and_product) / number_of_customers,


        'average_amount_of_product_units_per_customer': df[quantity_column_name].sum() / number_of_customers, # 'average_amount_of_quantities_per_customer'
        'average_expenses_by_user': df[total_price_column_name].sum() / number_of_customers,  # ??????

        'average_number_of_product_units_in_transaction': df[quantity_column_name].sum() / number_of_transactions, # 'average_amount_of_quantities_per_transaction'
        'average_number_of_unique_products_in_transaction': df[
                                                                  quantity_column_name].count() / number_of_transactions,

        'average_check_money': df[total_price_column_name].sum() / number_of_transactions, #??????
        'average_check_quantity': 0  # ??? = 'average_amount_of_quantities_per_transaction'

    }

    return dict_general_characteristics

print(get_general_characteristics('kauia_dataset_excluded.csv', 'Product Name', 'Member ID', 'Product Quantity', 'Transaction Date','Transaction ID', 'Product Total Price'))