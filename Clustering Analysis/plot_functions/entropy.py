# Built-in libraries
from urllib.parse import urlencode

# NumPy, SciPy and Pandas
import numpy as np

# Matplotlib
import matplotlib.pyplot as plt

def save_entropy_distribution(algorithm_name, params, combined_profiles, save_dir):
    # Entropy profile distribution
    plt.plot(combined_profiles.index, combined_profiles.entropy.sort_values())
    plt.xlabel('profile')
    plt.ylabel('entropy')
    plt.title('Profile Entropy Distribution')
    plt.savefig(save_dir + 'profile entropy distribution [algo<%s>, params<%s>].png' % (algorithm_name, urlencode(params)), bbox_inches='tight')
    plt.close()
    
    # Entropy building distribution
    combined_profiles_buildings = combined_profiles.drop_duplicates('Building')
    plt.plot(range(combined_profiles_buildings.shape[0]), combined_profiles_buildings.entropy.sort_values())
    plt.xlabel('building')
    plt.ylabel('entropy')
    plt.title('Building Entropy Distribution')
    plt.savefig(save_dir + 'building entropy distribution [algo<%s>, params<%s>].png' % (algorithm_name, urlencode(params)), bbox_inches='tight')
    plt.close()

def save_field_level_entropy_distribution(algorithm_name, params, combined_profiles, save_dir):
    for field in ['Timezone', 'PSU', 'Subindustry', 'dateflag', 'cluster']:
        plt.figure(figsize=(16, 8), dpi= 80, facecolor='w', edgecolor='k')
        combined_profiles_groups = combined_profiles.drop_duplicates('Building')[[field, 'entropy']].sort_values('entropy').groupby(field)
        groups_as_list = [combined_profiles_groups.get_group(x) for x in combined_profiles_groups.groups]
        list_of_tuples = [(groups_as_list[i][field].iloc[0], groups_as_list[i]['entropy'].as_matrix()) for i in range(len(groups_as_list))]
        for field_value, sorted_entropies in list_of_tuples:
            plt.plot(np.linspace(0,1, len(sorted_entropies)), sorted_entropies, label='%s (%d)' % (field_value, len(sorted_entropies)))
        plt.xlabel('Buildings Proportion')
        plt.ylabel('Entropy')
        plt.title('Entropy distribution by %s' % field)
        plt.legend()
        plt.savefig(save_dir + 'building entropy distribution by %s [algo<%s>, params<%s>].png' % (field, algorithm_name, urlencode(params)), bbox_inches='tight')
        plt.close()