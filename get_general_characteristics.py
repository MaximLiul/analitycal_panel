import pandas as pd

def get_general_characteristics(path_to_df_file_in_csv,
                                product_column_name,
                                user_column_name,
                                quantity_column_name,
                                date_column_name,
                                transactions_column_name,
                                total_price_column_name,
                                threashold_active_products = 100,
                                threashold_active_customers = 100):

    df = pd.read_csv(path_to_df_file_in_csv)
    df[date_column_name] = pd.to_datetime(df[date_column_name])

    df_grouped_by_customer_and_product = df.groupby([user_column_name, product_column_name], as_index=False)[quantity_column_name].sum()

    df_grouped_by_customer_and_transaction = df.groupby([user_column_name, transactions_column_name], as_index=False).count()
    df_grouped_by_customer = df_grouped_by_customer_and_transaction.groupby(user_column_name, as_index=False)[transactions_column_name].count()
    df_active_customers = df_grouped_by_customer.loc[df_grouped_by_customer[transactions_column_name] > threashold_active_customers].copy()

    df_grouped_by_product = df.groupby(product_column_name, as_index=False)[quantity_column_name].sum()
    df_active_products = df_grouped_by_product.loc[df_grouped_by_product[quantity_column_name] > threashold_active_products]

    number_of_products = len(df[product_column_name].unique())
    number_of_active_products = len(df_active_products)
    number_of_transactions = len(df[transactions_column_name].unique())
    number_of_customers = len(df[user_column_name].unique())
    number_of_active_customers = len(df_active_customers)
    time_duration_in_days = (df[date_column_name].max() - df[date_column_name].min()).days
    #df_grouped_by_customer_and_product.shape[0]

    dict_general_characteristics = {
        'time duration in days': time_duration_in_days,

        'number of purchases': len(df),
        'number of transactions': number_of_transactions,

        'number of products': number_of_products,
        'number of products with bought quantities more than {}'.format(threashold_active_products) : number_of_active_products,
        'active products sparsity':  number_of_active_products / number_of_products,

        'number of customers': number_of_customers,
        'number of customers who made more than {} visits'.format(threashold_active_customers) :  number_of_active_customers,
        'active customers sparsity': number_of_active_customers / number_of_customers,

        'average number of purchases per customer': len(df)/number_of_customers,
        'average number of transactions per customer': number_of_transactions / number_of_customers, #visits

        'average number of customers per day': number_of_transactions / time_duration_in_days,
        'average week visits of customer': number_of_transactions / ((time_duration_in_days / 7) * number_of_customers),    #how many visits a given user makes per week
        'average month visits of customer': number_of_transactions / ((time_duration_in_days / 30) * number_of_customers),   #how many visits a given user makes per month

        'number of interactions': len(df_grouped_by_customer_and_product),
        'sparsity': len(df_grouped_by_customer_and_product) / (number_of_products * number_of_customers),
        'average length of unique products per customer': len(df_grouped_by_customer_and_product) / number_of_customers,


        'average amount of product units per customer': df[quantity_column_name].sum() / number_of_customers, # 'average_amount_of_quantities_per_customer'
        'average expenses by user': df[total_price_column_name].sum() / number_of_customers,  # ??????

        'average number of product units in transaction': df[quantity_column_name].sum() / number_of_transactions, # 'average_amount_of_quantities_per_transaction'
        'average number of unique products in transaction': df[quantity_column_name].count() / number_of_transactions,

        'average check money': df[total_price_column_name].sum() / number_of_transactions, #??????
        'average check quantity': 0  # ??? = 'average_amount_of_quantities_per_transaction'

    }

    return dict_general_characteristics

print(get_general_characteristics('kauia_dataset_excluded.csv', 'Product Name', 'Member ID', 'Product Quantity', 'Transaction Date','Transaction ID', 'Product Total Price'))