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

#The output of the function is a dictionnary where keys are 'The portion of customers who has from start_value to step_value of column_name': portion of customers
#the diction will show portions until stop_value
def get_the_portion_of_users_loop(path_to_df_file_in_csv,
                            user_column,
                            product_column,
                            quantity_column,
                            transaction_column,
                            total_price_column,
                            product_list=None , # product_list = [start_value, stop_value, step_value] if product_list = None then proct column will not be considered
                            quantity_list=None,
                            transaction_list=None,
                            total_price_list=None,
                             ):
    analysis_list = []
    if product_list is None:
        product_list = []
        product_list.insert(0,product_column)
    else:
        product_list.insert(0, product_column)
        analysis_list.append(product_list)

    if quantity_list is None:
        quantity_list = []
        quantity_list.insert(0,quantity_column)
    else:
        quantity_list.insert(0, quantity_column)
        analysis_list.append(quantity_list)
    if transaction_list is None:
        transaction_list = []
        transaction_list.insert(0,transaction_column)
    else:
        transaction_list.insert(0,transaction_column)
        analysis_list.append(transaction_list)
    if total_price_list is None:
        total_price_list = []
        total_price_list.insert(0,total_price_column)
    else:
        total_price_list.insert(0, total_price_column)
        analysis_list.append(total_price_list)

    dict_portions = {}

    for list in analysis_list:
        portion = get_the_portion_of_users(path_to_df_file_in_csv,
                                               product_list[0],
                                               user_column,
                                               quantity_list[0],
                                               transaction_list[0],
                                               total_price_list[0],
                                               list[0],
                                               list[1], list[2], list[3])
        dict_portions.update(portion)
    return dict_portions

portions = get_the_portion_of_users_loop('kauia_dataset_excluded.csv',
                             'Member ID',
                            product_column = 'Product Name',
                            quantity_column = 'Product Quantity',
                            transaction_column = 'Transaction ID',
                            total_price_column = 'Product Total Price',
                             product_list= [0, 10, 2] , # product_list = [start_value, stop_value, step_value] if product_list = None then proct column will not be considered
                             quantity_list=[0, 10, 2],
                             transaction_list=[0, 10, 2],
                             total_price_list=None,
                             )
print(portions)


