# Built-in libraries
from urllib.parse import urlencode

# Matplotlib
import matplotlib.pyplot as plt

# JoyPy
import joypy

def save_continuous_plots(algorithm_name, params, combined_profiles, save_dir):
    plot_data = combined_profiles.copy()
    plot_data['cluster'] = plot_data['cluster'].map(lambda x: str(x))

    combined_profiles.cluster = combined_profiles.cluster.map(lambda x: str(x))
    fig, axes = joypy.joyplot(combined_profiles.loc[combined_profiles.Sqm < 30000,:], column=['Sqm', 'cluster'], by='cluster')
    plt.xlabel('sqm')
    plt.ylabel('cluster')
    plt.savefig(save_dir + 'sqm breakdown [algo<%s>, params<%s>].png' % (algorithm_name, urlencode(params)), bbox_inches='tight')
    plt.close()

    combined_profiles.cluster = combined_profiles.cluster.map(lambda x: str(x))
    fig, axes = joypy.joyplot(combined_profiles.loc[combined_profiles.EUI < 400,:], column=['EUI', 'cluster'], by='cluster')
    plt.xlabel('EUI')
    plt.ylabel('cluster')
    plt.savefig(save_dir + 'EUI breakdown [algo<%s>, params<%s>].png' % (algorithm_name, urlencode(params)), bbox_inches='tight')
    plt.close()
    
    # k must be greater than 1 to avoid singularity error
    combined_profiles.cluster = combined_profiles.cluster.map(lambda x: str(x))
    fig, axes = joypy.joyplot(combined_profiles, column=['entropy', 'cluster'], by='cluster')
    plt.xlabel('entropy')
    plt.ylabel('cluster')
    plt.savefig(save_dir + 'entropy breakdown [algo<%s>, params<%s>].png' % (algorithm_name, urlencode(params)), bbox_inches='tight')
    plt.close()
    
    combined_profiles.cluster = combined_profiles.cluster.map(lambda x: str(x))
    fig, axes = joypy.joyplot(combined_profiles, column=['dayofyear', 'cluster'], by='cluster')
    plt.xlabel('dayofyear')
    plt.ylabel('cluster')
    plt.savefig(save_dir + 'dayofyear breakdown [algo<%s>, params<%s>].png' % (algorithm_name, urlencode(params)), bbox_inches='tight')
    plt.close()
    
    # Boxplots
    for field_to_plot in ['Sqm', 'EUI', 'entropy', 'dayofyear']:
        combined_profiles.boxplot(field_to_plot, by='cluster', vert=False)
        plt.xlabel(field_to_plot)
        plt.ylabel('Cluster')
        plt.title('')
        plt.savefig(save_dir + field_to_plot + ' boxplot [algo<%s>, params<%s>].png' % (algorithm_name, urlencode(params)), bbox_inches='tight')
        plt.close()