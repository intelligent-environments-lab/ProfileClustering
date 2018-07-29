# Built-in libraries
from urllib.parse import urlencode

# NumPy, SciPy and Pandas
import pandas as pd

# Matplotlib
import matplotlib.pyplot as plt

def NULL_FUNC():
    return

def plot_stacked(col, data, by='cluster', proportion=True, proc_plot=NULL_FUNC):
    '''Plots a horizontal stacked bar chart
    col: name of the field to be plotted
    by: which to split the data into subgroups on (cluster or value)
    proportion: show proportion or actual counts
    '''
    if by == 'cluster':
        x_label = 'cluster'
        y_label = col
    elif by == 'dominant_cluster':
        x_label = 'dominant_cluster'
        y_label = col
    elif by == 'value':
        x_label = col
        y_label = 'cluster'
    else:
        raise Exception('Invalid by = %s' % by)
    cluster_stacked_vals = {}
    cluster_stacked = {}
    col_vals = set()
    for c in data[y_label].unique():
        cluster_stacked_vals[c] = {}
        cluster_col = data.loc[data[y_label] == c, x_label]
        val_counts = cluster_col.value_counts()
        for val in val_counts.index:
            col_vals.add(val)
            _count = val_counts[val]
            cluster_stacked_vals[c][val] = _count
    col_vals = list(col_vals)
    for c in cluster_stacked_vals:
        cluster_stacked[c] = []
        v_counts = cluster_stacked_vals[c]
        for col_val in col_vals:
            if col_val in v_counts:
                cluster_stacked[c].append(v_counts[col_val])
            else:
                cluster_stacked[c].append(0)
    pd_cluster_stacked = pd.DataFrame.from_dict(cluster_stacked)
    pd_cluster_stacked.index = col_vals
    if proportion:
        for i in range(pd_cluster_stacked.shape[0]):
            total_count = pd_cluster_stacked.iloc[i, :].sum()
            for j in range(pd_cluster_stacked.shape[1]):
                pd_cluster_stacked.iloc[i, j] = pd_cluster_stacked.iloc[i, j] / total_count
    # check if dataframe is empty
    if pd_cluster_stacked.shape[0] == 0:
        plt.close()
        return
    pd_cluster_stacked.plot(kind='barh', stacked=True, legend=False)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel(y_label)
    plt.ylabel(x_label)
    proc_plot(plt)
    plt.close()

def save_stacked_bars(algorithm_name, params, profiles, save_dir):
    def proc_plot(plt):
        plt.savefig(save_dir + '%s breakdown [algo<%s>, params<%s>].png' % (col, algorithm_name, urlencode(params)), bbox_inches='tight')

    plot_stacked('Climatezone', profiles, proc_plot=proc_plot)
    plot_stacked('Timezone', profiles, proc_plot=proc_plot)
    plot_stacked('PSU', profiles, proc_plot=proc_plot)
    plot_stacked('Industry', profiles, proc_plot=proc_plot)
    plot_stacked('Subindustry', profiles, proc_plot=proc_plot)
    plot_stacked('dateflag', profiles, proc_plot=proc_plot)
