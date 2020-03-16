import pandas as pd

def get_general_characteristics(path_to_df_file_in_csv,
                                product_column_name,
                                user_column_name,
                                quantity_column_name,
                                date_column_name,
                                transactions_column_name,
                                total_price_column_name,
                                threshold_active_customers_percent_by_visit_or_quantity, # 'visit' or 'quantity'
                                threshold_active_customers_percent = 10,
                                threshold_active_products_percent = 10
                                ):

    df = pd.read_csv(path_to_df_file_in_csv)
    df[date_column_name] = pd.to_datetime(df[date_column_name])

    number_of_products = len(df[product_column_name].unique())
    number_of_active_products = round((threshold_active_products_percent/100)*number_of_products)
    number_of_transactions = len(df[transactions_column_name].unique())
    number_of_customers = len(df[user_column_name].unique())
    number_of_active_customers = round((threshold_active_customers_percent/100)*number_of_customers)
    time_duration_in_days = (df[date_column_name].max() - df[date_column_name].min()).days

    df_grouped_by_customer_and_product = df.groupby([user_column_name, product_column_name], as_index=False)[quantity_column_name].sum()

    if threshold_active_customers_percent_by_visit_or_quantity == 'visit':
        df_grouped_by_customer_and_transaction = df.groupby([user_column_name, transactions_column_name],
                                                            as_index=False).count()
        df_grouped_by_customer = df_grouped_by_customer_and_transaction.groupby(user_column_name, as_index=False)[
                                                transactions_column_name].count().sort_values(transactions_column_name, ascending=False)
        df_active_customers = df_grouped_by_customer.head(number_of_active_customers)
    elif threshold_active_customers_percent_by_visit_or_quantity == 'quantity':
        df_grouped_by_customer = df.groupby(user_column_name, as_index=False)[quantity_column_name].sum().sort_values(quantity_column_name, ascending=False)
        df_active_customers = df_grouped_by_customer.head(number_of_active_customers)
    else:
        return print('The value of threshold_active_customers_percent_by_visit_or_quantity is not correct')

    df_grouped_by_product = df.groupby(product_column_name, as_index=False)[quantity_column_name].sum()
    df_active_products = df_grouped_by_product.head(number_of_active_products)
    #df_grouped_by_customer_and_product.shape[0]

    #working with active part
    df_only_active_customers = df.loc[df[user_column_name].isin(df_active_customers[user_column_name])].copy()
    df_only_active_customers_grouped_by_customer_and_product = \
                                df_only_active_customers.groupby([user_column_name, product_column_name], as_index=False)[quantity_column_name].sum()

    df_only_active_products = df.loc[df[product_column_name].isin(df_active_products[product_column_name])].copy()
    df_only_active_products_grouped_by_customer_and_product = df_only_active_products.groupby([user_column_name, product_column_name], as_index=False)[quantity_column_name].sum()

    df_active_part = df_only_active_customers.loc[df_only_active_customers[product_column_name].isin(df_active_products[product_column_name])].copy()
    df_active_part_grouped_by_customer_and_product = df_active_part.groupby([user_column_name, product_column_name], as_index=False)[quantity_column_name].sum()

    dict_general_characteristics = {
        'time duration in days': time_duration_in_days,

        'number of purchases': len(df),
        'number of transactions': number_of_transactions,

        'number of products': number_of_products,
        'number of top {} percents of products'.format(threshold_active_products_percent) : number_of_active_products,
        'active products sparsity':  number_of_active_products / number_of_products,

        'number of customers': number_of_customers,
        'number of top {} percents of the most active customers'.format(threshold_active_customers_percent) :  number_of_active_customers,
        'active customers sparsity': number_of_active_customers / number_of_customers,
        'number of customers per product': number_of_customers / number_of_products,
        'number of customers per active product': number_of_customers / number_of_active_products,

        'average number of purchases per customer': len(df)/number_of_customers,
        'average number of transactions per customer': number_of_transactions / number_of_customers, #visits

        'average number of customers per day': number_of_transactions / time_duration_in_days,
        'average week visits of customer': number_of_transactions / ((time_duration_in_days / 7) * number_of_customers),    #how many visits a given user makes per week
        'average month visits of customer': number_of_transactions / ((time_duration_in_days / 30) * number_of_customers),   #how many visits a given user makes per month

        'number of interactions': len(df_grouped_by_customer_and_product),
        'sparsity': len(df_grouped_by_customer_and_product) / (number_of_products * number_of_customers),
        'sparsity for active products': len(df_only_active_products_grouped_by_customer_and_product) / (number_of_active_products * number_of_customers),
        'sparsity for active customers': len(df_only_active_customers_grouped_by_customer_and_product) / (number_of_products * number_of_active_customers),
        'sparsity for active part': len(df_active_part_grouped_by_customer_and_product) / (
                    number_of_active_products * number_of_active_customers),
        'average acquiring of active products': len(df_only_active_products_grouped_by_customer_and_product) / number_of_active_products,
        'average user activity': len(df_grouped_by_customer_and_product) / number_of_customers,

        'average acquiring of products': len(df_grouped_by_customer_and_product) / number_of_products,
        'average length of unique products per customer': len(df_grouped_by_customer_and_product) / number_of_customers, # = 'average user activity'


        'average amount of product units per customer': df[quantity_column_name].sum() / number_of_customers, # 'average_amount_of_quantities_per_customer'
        'average expenses by user': df[total_price_column_name].sum() / number_of_customers,  # ??????

        'average number of product units in transaction': df[quantity_column_name].sum() / number_of_transactions, # 'average_amount_of_quantities_per_transaction'
        'average number of unique products in transaction': df[quantity_column_name].count() / number_of_transactions,

        'average check money': df[total_price_column_name].sum() / number_of_transactions, #??????
        'average check quantity': df[quantity_column_name].sum() / number_of_transactions  # ??? = 'average_amount_of_quantities_per_transaction'

    }

    return dict_general_characteristics

print(get_general_characteristics('kauia_dataset_excluded.csv', 'Product Name', 'Member ID', 'Product Quantity', 'Transaction Date','Transaction ID', 'Product Total Price', 'quantity'))