import pandas as pd

def get_the_portion_of_users(path_to_df_file_in_csv, product_column_name, user_column_name, quantity_column_name, transactions_column_name, total_price_column_name, column_for_analysis,
                             start_value, stop_value, step_value):
    df = pd.read_csv(path_to_df_file_in_csv)
    if column_for_analysis == quantity_column_name:
        df_grouped = df.groupby(user_column_name, as_index=False)[quantity_column_name].sum()
        df_grouped['Column for comparison'] = df_grouped[quantity_column_name]
    elif column_for_analysis == total_price_column_name:
        df_grouped = df.groupby(user_column_name, as_index=False)[total_price_column_name].sum()
        df_grouped['Column for comparison'] = df_grouped[total_price_column_name]
    elif column_for_analysis == transactions_column_name:
        df_grouped_temp = df.groupby([user_column_name, transactions_column_name], as_index=False).count()
        df_grouped = df_grouped_temp.groupby(user_column_name, as_index=False)[transactions_column_name].count()
        df_grouped['Column for comparison'] = df_grouped[transactions_column_name]
    elif column_for_analysis == product_column_name: #it shows amount of unique products for customers
        df_grouped = df.groupby(user_column_name, as_index=False)[product_column_name].count()
        df_grouped['Column for comparison'] = df_grouped[product_column_name]
    else:
        return print("column_for_analysis is not correct")

    dict_portions={}
    for comparison_value in range(start_value, stop_value, step_value):
        dict_portions['The portion of customers who has from {} to {} of {}'.format(comparison_value, comparison_value + step_value, column_for_analysis)] = \
        df_grouped.loc[(df_grouped['Column for comparison'] >= comparison_value) & (df_grouped['Column for comparison'] < comparison_value + step_value)][user_column_name].count() / len(df[user_column_name].unique())


    return dict_portions


print(get_the_portion_of_users('kauia_dataset_excluded.csv', 'Product Name', 'Member ID', 'Product Quantity', 'Transaction ID', 'Product Total Price', 'Product Name', 0, 100, 10))
print(get_the_portion_of_users('kauia_dataset_excluded.csv', 'Product Name', 'Member ID', 'Product Quantity', 'Transaction ID', 'Product Total Price', 'Product Quantity', 0, 100, 10))