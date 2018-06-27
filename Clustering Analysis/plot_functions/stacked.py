# Built-in libraries
from urllib.parse import urlencode

# NumPy, SciPy and Pandas
import pandas as pd

# Matplotlib
import matplotlib.pyplot as plt

def save_stacked_bars(algorithm_name, params, combined_profiles, save_dir):
    def plot_stacked(col, by='cluster', proportion=True):
        '''Plots a horizontal stacked bar chart
        col: name of the field to be plotted
        by: which to split the data into subgroups on (cluster or value)
        proportion: show proportion or actual counts
        '''
        if by == 'cluster':
            x_label = 'cluster'
            y_label = col
        elif by == 'value':
            x_label = col
            y_label = 'cluster'
        else:
            raise Exception('Invalid by = %s' % by)
        cluster_stacked_vals = {}
        cluster_stacked = {}
        col_vals = set()
        for c in combined_profiles[y_label].unique():
            cluster_stacked_vals[c] = {}
            cluster_col = combined_profiles.loc[combined_profiles[y_label] == c, x_label]
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
        plt.savefig(save_dir + '%s breakdown [algo<%s>, params<%s>].png' % (col, algorithm_name, urlencode(params)), bbox_inches='tight')
        plt.close()

    plot_stacked('Climatezone')
    plot_stacked('Timezone')
    plot_stacked('PSU')
    plot_stacked('Industry')
    plot_stacked('Subindustry')
    plot_stacked('dateflag')