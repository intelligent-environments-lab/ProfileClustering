# Built-in libraries
from urllib.parse import urlencode

# NumPy, SciPy and Pandas
import numpy as np

# Matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def get_dict(col):
    vc_dict = {}
    vc = col.value_counts()
    for idx in vc.index:
        vc_dict[idx] = vc.loc[idx]
    return vc_dict

def get_thickness(val, all_vals):
    std_val = np.std(all_vals)
    if std_val == 0:
        return 2.5
    mean_val = np.mean(all_vals)
    dev_val = (val-mean_val) / std_val
    dev_val = max(-1.5, min(dev_val, 5.5))
    return 2.5 + dev_val

def save_profile_plots(algorithm_name, params, profiles, save_dir):
    labelled_mat = profiles.as_matrix()
    cluster_ids = profiles.cluster.unique()

    cluster_counts = get_dict(profiles.cluster)
    cluster_counts_as_list = list(cluster_counts.values())

    # Average Plot
    plt.figure(figsize=(16, 8), dpi= 80, facecolor='w', edgecolor='k')

    for cid in cluster_ids:
        cluster_rows = labelled_mat[profiles.cluster == cid, 3:(3+24)].astype(float)
        plot_color = plt.get_cmap('tab10')(int(cid))
        plt.plot(cluster_rows.mean(axis=0), c=plot_color, lw=get_thickness(cluster_counts[cid], cluster_counts_as_list))

    plt.xticks(range(24), ['0%d:00' % i for i in range(10)] + ['%d:00' % i for i in range(10, 24)])
    plt.xlabel('Hour')
    plt.ylabel('Mean Normalized Energy Use')
    plt.title('Average Cluster Energy Profile by Hour')
    plt.legend(['Cluster %d (%d)' % (cid, cluster_counts[cid]) for cid in cluster_ids])
    plt.savefig(save_dir + 'Average Cluster Energy Profile by Hour [algo<%s>, params<%s>].png' % (algorithm_name, urlencode(params)), bbox_inches='tight')
    plt.close()

    # Sample Plot
    N = 1000
    _alpha = .1 / len(cluster_ids)
    np.random.seed(42)
    cluster_handles = []
    plt.figure(figsize=(16, 8), dpi= 80, facecolor='w', edgecolor='k')
    for cid in cluster_ids:
        cluster_rows = labelled_mat[profiles.cluster == cid, 3:(3+24)].astype(float)
        rd_indices = np.random.choice(cluster_rows.shape[0], min(N, cluster_rows.shape[0]), replace=False)

        plot_color = plt.get_cmap('tab10')(int(cid))
        for i in rd_indices:
            plt.plot(cluster_rows[i], c=plot_color, alpha=_alpha)
        plt.xticks(range(24), ['0%d:00' % i for i in range(10)] + ['%d:00' % i for i in range(10, 24)])
        plt.xlabel('Hour')
        plt.ylabel('Mean Normalized Energy Use')
        plt.title('Cluster Energy Profiles by Hour')
        cluster_handles.append(mlines.Line2D([], [], color=plot_color, label='Cluster ' + str(cid)))

    plt.legend(handles=cluster_handles)
    plt.savefig(save_dir + 'Cluster Energy Profiles by Hour [algo<%s>, params<%s>].png' % (algorithm_name, urlencode(params)), bbox_inches='tight')
    plt.close()