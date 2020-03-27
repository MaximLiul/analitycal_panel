import pandas as pd

def get_general_characteristics(path_to_df,
                                date_column,
                                transactions_column,
                                total_price_column = None,
                                product_column='StockCode',
                                user_column='CustomerID',
                                quantity_column='Quantity',
                                threshold_active_customers_percent_by_visit_or_quantity = 'visit', # 'visit' or 'quantity'
                                threshold_active_customers_percent=10,
                                threshold_active_products_percent=10
                                ):

    df = pd.read_csv(path_to_df)
    df[date_column] = pd.to_datetime(df[date_column])

    number_of_products = len(df[product_column].unique())
    number_of_active_products = round((threshold_active_products_percent/100)*number_of_products)
    number_of_transactions = len(df[transactions_column].unique())
    number_of_customers = len(df[user_column].unique())
    number_of_active_customers = round((threshold_active_customers_percent/100)*number_of_customers)
    time_duration_in_days = (df[date_column].max() - df[date_column].min()).days

    df_gr_customer_and_product = df.groupby([user_column, product_column], as_index=False)[quantity_column].sum()

    if threshold_active_customers_percent_by_visit_or_quantity == 'visit':
        df_gr_customer_and_transaction = df.groupby([user_column, transactions_column],
                                                            as_index=False).count()
        df_gr_customer = df_gr_customer_and_transaction.groupby(user_column, as_index=False)[
                                                transactions_column].count().sort_values(transactions_column, ascending=False)
        df_active_customers = df_gr_customer.head(number_of_active_customers)
    elif threshold_active_customers_percent_by_visit_or_quantity == 'quantity':
        df_gr_customer = df.groupby(user_column, as_index=False)[quantity_column].sum().sort_values(quantity_column, ascending=False)
        df_active_customers = df_gr_customer.head(number_of_active_customers)
    else:
        return print('The value of threshold_active_customers_percent_by_visit_or_quantity is not correct')

    df_gr_product = df.groupby(product_column, as_index=False)[quantity_column].sum()
    df_active_products = df_gr_product.head(number_of_active_products)

    #working with active part
    df_only_active_customers = df.loc[df[user_column].isin(df_active_customers[user_column])].copy()
    df_only_active_customers_gr_customer_and_product = \
                                df_only_active_customers.groupby([user_column, product_column], as_index=False)[quantity_column].sum()

    df_only_active_products = df.loc[df[product_column].isin(df_active_products[product_column])].copy()
    df_only_active_products_gr_customer_and_product = df_only_active_products.groupby([user_column, product_column], as_index=False)[quantity_column].sum()

    df_active_part = df_only_active_customers.loc[df_only_active_customers[product_column].isin(df_active_products[product_column])].copy()
    df_active_part_gr_customer_and_product = df_active_part.groupby([user_column, product_column], as_index=False)[quantity_column].sum()

    dict_general_characteristics = {
        'time duration in days': time_duration_in_days,

        'number of purchases': len(df),
        'number of transactions': number_of_transactions,
        'number of products': number_of_products,
        'number of top {} percents of products'.format(threshold_active_products_percent) : number_of_active_products,
        #'active products sparsity':  number_of_active_products / number_of_products,
        'number of customers': number_of_customers,
        'number of top {} percents of the most active customers'.format(threshold_active_customers_percent) :  number_of_active_customers,
        #'active customers sparsity': number_of_active_customers / number_of_customers,

        'number of customers per product': number_of_customers / number_of_products,
        'number of customers per active product': number_of_customers / number_of_active_products,

        'average number of purchases per customer': len(df)/number_of_customers,
        'average number of transactions per customer': number_of_transactions / number_of_customers, #visits

        'average number of customers per day': number_of_transactions / time_duration_in_days,
        'average week visits of customer': number_of_transactions / ((time_duration_in_days / 7) * number_of_customers),    #how many visits a given user makes per week
        'average month visits of customer': number_of_transactions / ((time_duration_in_days / 30) * number_of_customers),   #how many visits a given user makes per month

        'number of interactions': len(df_gr_customer_and_product),
        'sparsity': len(df_gr_customer_and_product) / (number_of_products * number_of_customers),
        'sparsity for active products': len(df_only_active_products_gr_customer_and_product) / (number_of_active_products * number_of_customers),
        'sparsity for active customers': len(df_only_active_customers_gr_customer_and_product) / (number_of_products * number_of_active_customers),
        'sparsity for active part': len(df_active_part_gr_customer_and_product) / (
                    number_of_active_products * number_of_active_customers),

        'average acquiring of active products': len(df_only_active_products_gr_customer_and_product) / number_of_active_products,
        'average user activity': len(df_gr_customer_and_product) / number_of_customers,

        'average acquiring of products': len(df_gr_customer_and_product) / number_of_products,
        'average length of unique products per customer': len(df_gr_customer_and_product) / number_of_customers, # = 'average user activity'


        'average amount of product units per customer': df[quantity_column].sum() / number_of_customers, # 'average_amount_of_quantities_per_customer'


        'average number of product units in transaction': df[quantity_column].sum() / number_of_transactions, # 'average_amount_of_quantities_per_transaction'
        'average number of unique products in transaction': df[quantity_column].count() / number_of_transactions,
        'average check quantity': df[quantity_column].sum() / number_of_transactions, # ??? = 'average_amount_of_quantities_per_transaction'
    }
    if total_price_column is not None:
        dict_general_characteristics['average check money'] = df[total_price_column].sum() / number_of_transactions  # ??????
        dict_general_characteristics['average expenses by user'] = df[total_price_column].sum() / number_of_customers  # ??????
    return dict_general_characteristics


characteristics = get_general_characteristics('kauia_dataset_excluded.csv',
                                              'Transaction Date',
                                              'Transaction ID',
                                              'Product Total Price',
                                              'Product Name',
                                              'Member ID',
                                              'Product Quantity',
                                              'quantity')

print(characteristics)