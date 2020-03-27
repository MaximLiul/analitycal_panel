import pandas as pd

def get_the_portion_of_users(path_to_df_file_in_csv,
                             product_column,
                             user_column,
                             quantity_column,
                             transactions_column,
                             total_price_column,
                             analysis_column_name,
                             start_value, stop_value, step_value):
    df = pd.read_csv(path_to_df_file_in_csv)
    if analysis_column_name == quantity_column:
        df_grouped = df.groupby(user_column, as_index=False)[quantity_column].sum()
        df_grouped['Column for comparison'] = df_grouped[quantity_column]
    elif analysis_column_name == total_price_column:
        df_grouped = df.groupby(user_column, as_index=False)[total_price_column].sum()
        df_grouped['Column for comparison'] = df_grouped[total_price_column]
    elif analysis_column_name == transactions_column:
        df_grouped_temp = df.groupby([user_column, transactions_column], as_index=False).count()
        df_grouped = df_grouped_temp.groupby(user_column, as_index=False)[transactions_column].count()
        df_grouped['Column for comparison'] = df_grouped[transactions_column]
    elif analysis_column_name == product_column:
        df_grouped = df.groupby(user_column, as_index=False)[product_column].count()
        df_grouped['Column for comparison'] = df_grouped[product_column]
    else:
        return print("analysis_column_name is not correct")

    dict_portions={}
    for comparison_value in range(start_value, stop_value, step_value):
        dict_portions['The portion of customers who has from {} to {} of {}'.format(comparison_value, comparison_value + step_value, analysis_column_name)] = \
        df_grouped.loc[(df_grouped['Column for comparison'] >= comparison_value) &
                       (df_grouped['Column for comparison'] < comparison_value + step_value)][user_column].count() / len(df[user_column].unique())

    return dict_portions



print(get_the_portion_of_users('kauia_dataset_excluded.csv', 'Product Name', 'Member ID', 'Product Quantity', 'Transaction ID', 'Product Total Price', 'Product Name', 0, 100, 10))
print(get_the_portion_of_users('kauia_dataset_excluded.csv', 'Product Name', 'Member ID', 'Product Quantity', 'Transaction ID', 'Product Total Price', 'Product Quantity', 0, 100, 10))