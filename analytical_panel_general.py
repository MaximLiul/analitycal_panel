import pandas as pd
import matplotlib.pyplot as plt

def analytical_panel_general(path_to_df_file_in_csv,
                             product_column_name,
                             user_column_name,
                             quantity_column_name,
                             transactions_column_name,
                             price_column_name,
                             is_get_general_characteristics = False,
                             column_for_analysis_portions= None,
                             get_the_portion_start_value = None,
                             get_the_portion_stop_value = None,
                             get_the_portion_step_value = None,
                             column_for_analysis_top_elements = None,
                             choose_first_n=10,
                             save_or_show_histogram=None
                             ):

    def get_general_characteristics(path_to_df_file_in_csv, product_column_name, user_column_name, quantity_column_name,
                                    transactions_column_name, price_column_name):
        df = pd.read_csv(path_to_df_file_in_csv)
        df_grouped_by_customer_and_product = df.groupby([user_column_name, product_column_name], as_index=False)[
            quantity_column_name].sum()

        number_of_products = len(df[product_column_name].value_counts())
        number_of_transactions = len(df[transactions_column_name].value_counts())
        number_of_customers = len(df[user_column_name].value_counts())

        dict_general_characteristics = {
            'number_of_products': number_of_products,
            'number_of_transactions': number_of_transactions,
            'number_of_customers': number_of_customers,
            'average_length_of_quantities_per_customer': df[quantity_column_name].sum() / number_of_customers,
            'average_length_of_unique_products_per_customer': len(
                df_grouped_by_customer_and_product) / number_of_customers,
            'sparsity': len(df_grouped_by_customer_and_product) / (number_of_products * number_of_customers),
            'average_number_of_quantities_in_a_transaction': df[quantity_column_name].sum() / number_of_transactions,
            'average_number_of_unique_products_in_a_transaction': df[
                                                                      quantity_column_name].count() / number_of_transactions,
            'average_number_of_transaction_per_customer': number_of_transactions / number_of_customers,
            'average_check': df[price_column_name].sum() / number_of_transactions,
            'average_expenses_by_user': df[price_column_name].sum() / number_of_customers
        }

        return dict_general_characteristics

    def get_the_portion_of_users(path_to_df_file_in_csv, product_column_name, user_column_name, quantity_column_name,
                                 transactions_column_name, price_column_name, column_for_analysis,
                                 start_value, stop_value, step_value):
        df = pd.read_csv(path_to_df_file_in_csv)
        if column_for_analysis == quantity_column_name:
            df_grouped = df.groupby(user_column_name, as_index=False)[quantity_column_name].sum()
            df_grouped['Column for comparison'] = df_grouped[quantity_column_name]
        elif column_for_analysis == price_column_name:
            df_grouped = df.groupby(user_column_name, as_index=False)[price_column_name].sum()
            df_grouped['Column for comparison'] = df_grouped[price_column_name]
        elif column_for_analysis == transactions_column_name:
            df_grouped_temp = df.groupby([user_column_name, transactions_column_name], as_index=False).count()
            df_grouped = df_grouped_temp.groupby(user_column_name, as_index=False)[transactions_column_name].count()
            df_grouped['Column for comparison'] = df_grouped[transactions_column_name]
        elif column_for_analysis == product_column_name:
            df_grouped = df.groupby(user_column_name, as_index=False)[product_column_name].count()
            df_grouped['Column for comparison'] = df_grouped[product_column_name]
        else:
            return print("column_for_analysis is not correct")

        dict_portions = {}
        for comparison_value in range(start_value, stop_value, step_value):
            dict_portions['The portion of customers who has from {} to {} of {}'.format(comparison_value,
                                                                                        comparison_value + step_value,
                                                                                        column_for_analysis)] = \
                df_grouped.loc[(df_grouped['Column for comparison'] >= comparison_value) & (
                            df_grouped['Column for comparison'] < comparison_value + step_value)][
                    user_column_name].count() / len(df[user_column_name].value_counts())

        return dict_portions

    def get_top_elements(path_to_df_file_in_csv, column_for_analysis, choose_first_n=10,
                         save_or_show_histogram=None):  # possible values for save_or_show_histogram are 'save' and 'show'
        df = pd.read_csv(path_to_df_file_in_csv)
        top_elements = df[column_for_analysis].value_counts().head(choose_first_n)
        top_elements_dict = {}
        for element in top_elements.index:
            top_elements_dict[element] = top_elements.loc[top_elements.index == element].values[0]

        if save_or_show_histogram is not None:
            fig = plt.figure(figsize=(12, 12))  # define plot area
            ax = fig.gca()  # define axis
            top_elements[:choose_first_n].plot.bar(ax=ax, color='blue')
            ax.set_title('{}'.format(column_for_analysis))  # Give the plot a main title
            ax.set_xlabel('Names of {} columns'.format(column_for_analysis))  # Set text for the x axis
            ax.set_ylabel('Number of times')  # Set text for y axis
            if save_or_show_histogram == 'show':
                plt.show()
            elif save_or_show_histogram == 'save':
                plt.savefig(
                    'histogram_top_{}_elements_{}.png'.format(choose_first_n, column_for_analysis, column_for_analysis),
                    dpi=250)
            else:
                return print('save_or_show_histogram is not correct')

        return top_elements_dict



    if is_get_general_characteristics:
        dict_general_characteristics = get_general_characteristics(path_to_df_file_in_csv, product_column_name, user_column_name, quantity_column_name,
                                    transactions_column_name, price_column_name)
    else:
        dict_general_characteristics = None

    if column_for_analysis_portions is not None:
        dict_portions = get_the_portion_of_users(path_to_df_file_in_csv, product_column_name, user_column_name, quantity_column_name,
                                 transactions_column_name, price_column_name, column_for_analysis_portions,
                                 get_the_portion_start_value, get_the_portion_stop_value, get_the_portion_step_value)
    else:
        dict_portions = None

    if column_for_analysis_top_elements is not None:
        top_elements_dict = get_top_elements(path_to_df_file_in_csv, column_for_analysis_top_elements, choose_first_n, save_or_show_histogram)


    return [dict_general_characteristics, dict_portions, top_elements_dict]



#print(analytical_panel_general('kauia_dataset_excluded.csv', 'Product Name', 'Member ID', 'Product Quantity','Transaction ID', 'Product Total Price'))

print(
analytical_panel_general(    'kauia_dataset_excluded.csv',
                             'Product Name',
                             'Member ID',
                             'Product Quantity',
                             'Transaction ID',
                             'Product Total Price',
                             is_get_general_characteristics = True,
                             column_for_analysis_portions = 'Product Total Price',
                             is_get_the_portion_of_users = True,
                             get_the_portion_start_value = 0,
                             get_the_portion_stop_value = 1000,
                             get_the_portion_step_value = 100,
                             column_for_analysis_top_elements = 'Product Name',
                             choose_first_n=10,
                             save_or_show_histogram= 'show'
                             )
)