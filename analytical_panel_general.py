import pandas as pd
import matplotlib.pyplot as plt

def get_general_characteristics(path_to_df,
                                date_column,
                                transaction_column='index',
                                total_price_column=None,
                                product_column='StockCode',
                                user_column='CustomerID',
                                quantity_column='Quantity',
                                threshold_active_customers_percent_by_visit_or_quantity='visit', # 'visit' or 'quantity'; we can range users by visits or quantities
                                threshold_active_customers_percent=10,
                                threshold_active_products_percent=10
                                ):

    df=pd.read_csv(path_to_df)

    if transaction_column == 'index':
        transaction_column='transaction_id'
        df[transaction_column] = df.index
    df[date_column]=pd.to_datetime(df[date_column])

    number_of_products=len(df[product_column].unique())
    number_of_active_products=round((threshold_active_products_percent/100)*number_of_products)
    number_of_transactions=len(df[transaction_column].unique())
    number_of_customers=len(df[user_column].unique())
    number_of_active_customers=round((threshold_active_customers_percent/100)*number_of_customers)
    time_duration_in_days=(df[date_column].max() - df[date_column].min()).days
    print(number_of_transactions)
    df_gr_customer_and_product = df.groupby([user_column, product_column], as_index=False)[quantity_column].sum()

    if threshold_active_customers_percent_by_visit_or_quantity == 'visit':
        df_gr_customer_and_transaction = df.groupby([user_column, transaction_column],
                                                            as_index=False).count()
        df_gr_customer = df_gr_customer_and_transaction.groupby(user_column, as_index=False)[
                                                transaction_column].count().sort_values(transaction_column, ascending=False)
        df_active_customers = df_gr_customer.head(number_of_active_customers)
    elif threshold_active_customers_percent_by_visit_or_quantity == 'quantity':
        df_gr_customer = df.groupby(user_column, as_index=False)[quantity_column].sum().sort_values(quantity_column, ascending=False)
        df_active_customers = df_gr_customer.head(number_of_active_customers)
    else:
        return print('The value of threshold_active_customers_percent_by_visit_or_quantity is not correct')

    df_gr_product = df.groupby(product_column, as_index=False)[quantity_column].sum().sort_values(quantity_column, ascending=False)
    df_active_products = df_gr_product.head(number_of_active_products)

    #working with active part
    df_only_active_customers = df.loc[df[user_column].isin(df_active_customers[user_column])].copy()
    df_only_active_customers_gr_customer_and_product=\
                                df_only_active_customers.groupby([user_column, product_column], as_index=False)[quantity_column].sum()

    df_only_active_products = df.loc[df[product_column].isin(df_active_products[product_column])].copy()
    df_only_active_products_gr_customer_and_product = df_only_active_products.groupby([user_column, product_column], as_index=False)[quantity_column].sum()

    df_active_part = df_only_active_customers.loc[df_only_active_customers[product_column].isin(df_active_products[product_column])].copy()
    df_active_part_gr_customer_and_product = df_active_part.groupby([user_column, product_column], as_index=False)[quantity_column].sum()

    dict_general_characteristics={
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
        'average length of unique products per customer': len(df_gr_customer_and_product) / number_of_customers, #='average user activity'


        'average amount of product units per customer': df[quantity_column].sum() / number_of_customers, # 'average_amount_of_quantities_per_customer'


        'average number of product units in transaction': df[quantity_column].sum() / number_of_transactions, # 'average_amount_of_quantities_per_transaction'
        'average number of unique products in transaction': df[quantity_column].count() / number_of_transactions,
        'average check quantity': df[quantity_column].sum() / number_of_transactions, # ???='average_amount_of_quantities_per_transaction'
    }
    if total_price_column is not None:
        dict_general_characteristics['average check money'] = df[total_price_column].sum() / number_of_transactions  # ??????
        dict_general_characteristics['average expenses by user'] = df[total_price_column].sum() / number_of_customers  # ??????
    return dict_general_characteristics

def get_the_portion_of_users(path_to_df,
                             analysis_column_name,
                             start_value, stop_value, step_value,
                             product_column='StockCode',
                             user_column='CustomerID',
                             quantity_column='Quantity',
                             transactions_column=None,
                             total_price_column=None
                             ):
    df=pd.read_csv(path_to_df)
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
        dict_portions['The portion of customers who has from {} to {} of {}'.format(comparison_value, comparison_value + step_value, analysis_column_name)]=\
        df_grouped.loc[(df_grouped['Column for comparison'] >= comparison_value) &
                       (df_grouped['Column for comparison'] < comparison_value + step_value)][user_column].count() / len(df[user_column].unique())

    return dict_portions

#The output of the function is a dictionnary where keys are 'The portion of customers who has from start_value to step_value of column_name': portion of customers
#the diction will show portions until stop_value
def get_the_portion_of_users_general(path_to_df,
                            transaction_column=None,
                            total_price_column=None,
                            product_column='StockCode',
                            user_column='CustomerID',
                            quantity_column='Quantity',
                            product_list=None , # product_list=[start_value, stop_value, step_value] if product_list=None then proct column will not be considered
                            quantity_list=None,
                            transaction_list=None,
                            total_price_list=None,
                             ):
    analysis_list=[]
    if product_list is None:
        product_list=[]
        product_list.insert(0,product_column)
    else:
        product_list.insert(0, product_column)
        analysis_list.append(product_list)

    if quantity_list is None:
        quantity_list=[]
        quantity_list.insert(0,quantity_column)
    else:
        quantity_list.insert(0, quantity_column)
        analysis_list.append(quantity_list)
    if transaction_list is None:
        transaction_list=[]
        transaction_list.insert(0,transaction_column)
    else:
        transaction_list.insert(0,transaction_column)
        analysis_list.append(transaction_list)
    if total_price_list is None:
        total_price_list=[]
        total_price_list.insert(0,total_price_column)
    else:
        total_price_list.insert(0, total_price_column)
        analysis_list.append(total_price_list)

    dict_portions={}

    for list in analysis_list:
        portion=get_the_portion_of_users(path_to_df,
                                               list[0],
                                               list[1], list[2], list[3],
                                               product_list[0],
                                               user_column,
                                               quantity_list[0],
                                               transaction_list[0],
                                               total_price_list[0]
                                               )
        dict_portions.update(portion)
    return dict_portions

def get_top_elements(path_to_df,
                     product_column='StockCode',
                     user_column='CustomerID',
                     is_get_top_products=True,
                     is_get_top_users=True,
                     n_top_elements=10,
                     show_histogram_or_output_file_name=None):  #possible values for save_or_show_histogram are 'show' or name of output file for saving histogram. the resulting name of file will be product (user) + output_file_name
    df=pd.read_csv(path_to_df)


    if is_get_top_products:
        top_elements_products = df[product_column].value_counts().head(n_top_elements)
        if show_histogram_or_output_file_name is not None:
            fig=plt.figure(figsize=(12, 12))  # define plot area
            ax=fig.gca()  # define axis
            top_elements_products.plot.bar(ax=ax, color='blue')
            ax.set_title('{}'.format(product_column))  # Give the plot a main title
            ax.set_xlabel('Names of {} columns'.format(product_column))  # Set text for the x axis
            ax.set_ylabel('Number of times')  # Set text for y axis
            if show_histogram_or_output_file_name == 'show':
                plt.show()
            else:
                plt.savefig('products_{}'.format(show_histogram_or_output_file_name), dpi=250)
    else:
        top_elements_products={}

    if is_get_top_users:
        top_elements_users = df[user_column].value_counts().head(n_top_elements)
        if show_histogram_or_output_file_name is not None:
            fig=plt.figure(figsize=(12, 12))  # define plot area
            ax=fig.gca()  # define axis
            top_elements_users.plot.bar(ax=ax, color='blue')
            ax.set_title('{}'.format(user_column))  # Give the plot a main title
            ax.set_xlabel('Names of {} columns'.format(user_column))  # Set text for the x axis
            ax.set_ylabel('Number of times')  # Set text for y axis
            if show_histogram_or_output_file_name == 'show':
                plt.show()
            else:
                plt.savefig('users_{}'.format(show_histogram_or_output_file_name), dpi=250)
    else:
        top_elements_users={}

    return top_elements_users, top_elements_products




def analytical_panel_general(path_to_df,
                             date_column,
                             transactions_column,
                             total_price_column,
                             threshold_active_customers_percent_by_visit_or_quantity='quantity', #we can range users by visits or quantities
                             product_column='StockCode',
                             user_column='CustomerID',
                             quantity_column='Quantity',
                             threshold_active_customers_percent=10,
                             threshold_active_products_percent=10,
                             is_get_general_characteristics=False,
# product_list=[start_value, stop_value, step_value] if product_list=None then proct column will not be considered
#One of the outputs is a dictionnary where keys are 'The portion of customers who has from start_value to step_value of column_name': portion of customers
#the diction will show portions until stop_value
                             product_list=None, # product_list=[start_value, stop_value, step_value] if product_list=None then proct column will not be considered
                             quantity_list=None,
                             transaction_list=None,
                             total_price_list=None,
                             is_get_top_products=True,
                             is_get_top_users=False,
                             n_top_elements=10,
                             show_histogram_or_output_file_name=None #possible values for save_or_show_histogram are 'show' or name of output file for saving histogram. the resulting name of file will be product (user) + output_file_name
                             ):


    if is_get_general_characteristics:
        dict_general_characteristics=get_general_characteristics(path_to_df,
                                date_column,
                                transactions_column,
                                total_price_column,
                                product_column,
                                user_column,
                                quantity_column,
                                threshold_active_customers_percent_by_visit_or_quantity, # 'visit' or 'quantity'
                                threshold_active_customers_percent,
                                threshold_active_products_percent)
    else:
        dict_general_characteristics=None

    if product_list or quantity_list or transaction_list or total_price_list is not None:
        dict_portions=get_the_portion_of_users_general(path_to_df,
                            transactions_column,
                            total_price_column,
                            product_column,
                            user_column,
                            quantity_column,
                            product_list, # product_list=[start_value, stop_value, step_value] if product_list=None then proct column will not be considered
                            quantity_list,
                            transaction_list,
                            total_price_list
                             )
    else:
        dict_portions=None

    if is_get_top_products or is_get_top_users:
        top_elements=get_top_elements(path_to_df,
                      product_column,
                      user_column,
                      is_get_top_products,
                      is_get_top_users,
                      n_top_elements,
                      show_histogram_or_output_file_name)
    else:
        top_elements=None

    return dict_general_characteristics, dict_portions, top_elements

panel=analytical_panel_general('kauia_dataset_excluded.csv',
                             product_column='Product Name',
                             user_column='Member ID',
                             quantity_column='Product Quantity',
                             date_column='Transaction Date',
                            threshold_active_customers_percent=10,
                            threshold_active_products_percent=10,
                             transactions_column='index',
                             total_price_column=None,
                             is_get_general_characteristics=True,
                             threshold_active_customers_percent_by_visit_or_quantity='quantity',
                             product_list=[0,7,1],
                             quantity_list=None,
                             transaction_list=None,
                             total_price_list=None,
                             is_get_top_products=False,
                             is_get_top_users=False,
                             n_top_elements=10,
                             show_histogram_or_output_file_name=None)
print(panel)