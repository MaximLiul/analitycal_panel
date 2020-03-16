import pandas as pd
import matplotlib.pyplot as plt

def get_top_elements(path_to_df_file_in_csv, column_for_analysis, choose_first_n = 10, save_or_show_histogram = None):  #possible values for save_or_show_histogram are 'save' and 'show'
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
            plt.savefig('histogram_top_{}_elements_{}.png'.format(choose_first_n, column_for_analysis, column_for_analysis), dpi=250)
        else: return print('save_or_show_histogram is not correct')

    return top_elements

print(get_top_elements('kauia_dataset_excluded.csv', 'Member ID', choose_first_n = 10))