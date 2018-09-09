# Apples or Oranges? Identification of fundamental load shape profiles for benchmarking buildings using a large and diverse dataset 

Project Collaborators:

Intelligent Environments Laboratory, UT Austin, (http://nagy.caee.utexas.edu)

Building and Urban Data Science Lab, NUS Singapore, (http://www.budslab.org/) 

A project focused on extracting the right topology of building utilization from raw whole building sensor data

## Data collection & Preprocessing

- With multiple data sources (i.e., UTEXAS, MIT, PECAN, IRELAND, GENOME, ...), we choose .hdf5 data format to deal with a large size dataset. All the raw datasets are uploaded externally due to the limitation of uploading size. The data is transformed as .hdf5 file format. After running two ipython notebook below, we would get a complete hdf5 file for the whole dataset with complete metadata. 

- [Data Collection](Data%20Preprocessing/data_collection_1.ipynb): Read temporal dataset and metadata (i.e., Industry, Sub-industry, Primary usage type, Region, Area) to generate .hdf5 file.
- [Consolidate Meta Data](Clustering%20Analysis/Consolidate_Metadata.ipynb): Adding and consolidate meta data in the hdf5 data store
- [Addition of Washington Dataset](Clustering%20Analysis/Addition%20of%20Washington%20Dataset.ipynb): Adding the DC dataset and related meta data
- [Profile Generation](Clustering%20Analysis/Profile%20Generation.ipynb): Generate building daily energy profiles with attached meta data from the hdf5 data store

## Clustering & Validation

- [Clustering](Clustering%20Analysis/Clustering.ipynb): Generate building clusters based on daily energy profiles using K-Means, Bisecting K-Means and Gaussian Mixture Model
- [Clustering Validation Metrics](Clustering%20Analysis/Clustering%20Validation%20Metrics.ipynb): Calculate validation metrics for the clustering results for different choice of k and different algorithms

## Clustering Visualization

- [Heatmap](Clustering%20Analysis/Heatmap.ipynb): Generate building heatmaps displaying the cluster proportions and building meta data information grouped by dominant clusters
- [Dominant Cluster Bar Chart](Clustering%20Analysis/Dominant%20Cluster%20Bar%20Chart.ipynb): Generate bar charts that show the composition of buildings in each dominant cluster broken down by meta data fields
- [Tufte Table](Clustering%20Analysis/Tufte%20Table.ipynb): Display the fundamental load shape profiles for each cluster in an aggregated Tufte-style table as k and clustering algorithm vary
- [Benchmarking Plots](Clustering%20Analysis/Benchmarking%20Plots.ipynb): Apply the clustering results to compare against the traditional way of building benchmarking

## Detailed Notebook Information

### Profile Generation
This notebook generates a combined profiles dataframe from the hdf5 data store.

By default, the path to the hdf5 data store is set to be `meta/meta.hdf5`. You can change or rename the path by editing the first cell under `A. Read HDF5 Data`.

The following steps are performed
- Extract numerical and meta data from hdf5
- Convert time zones from UTC to local time zones for the genome dataset
- Iterate over the data to build the profiles, keeping only complete profiles
- Normalize the profiles by standardizing the profiles on a per-profile basis
- Convert Sqft to Sqm
- Calculate EUI by using the latest 365 days of data, or extrapolate if the available number of days is less than 365
- Create date flags (weekday, weekend or holiday). Holidays are determined based on the region of the building. If a holiday falls on a weekend, the date flag is recorded as `holiday`
- Get the day of year column based on the number of days from Jan 1 of that year for each profile
- Convert rare industries and PSUs to `Others` based on a predefined list

### Clustering

This notebook is responsible for running the clustering models and saving the basic plots generated.

The following preliminary steps are performed
- Read profiles generated from the Profile Generation notebook
- Classify the profiles into combined_profiles, residential_profiles and non_residential_profiles
- Read the various plot saving functions to be used in each of the clustering steps below

The ClusteringBaseModel is a class that wraps around the Scikit Learn models and additional implementation to enforce code modularity, maintainability and reusability.

*Initialization Arguments*

- `params_list` specifies the parameters to be used for different iterations. In most cases, this would be the values of K to be used.
- `profiles` determines the profiles to be used (combined, residential or non-residential as of now).
- `cluster_algo` is a string used to differentiate the results generated when saving the plot.
- `save_dir` determines the directory to be saved.
- `labels_dir` determines where the clustering results (labels) are saved. We save the labels, so for later analyses we do not repeat the clustering process multiple times.

`KmeansClustering`, `DBSCANClustering`, `HierarchicalClustering`, `GMMClustering` and `BisectingKMeansClustering` inherit the base model with additional implementation details. However, we are only using `KmeansClustering`, `BisectingKMeansClustering` and `GMMClustering` due to the long running time issues encountered for the other two.

*Steps for Each Iteration*

- Model checks if the labels have already been generated. If not, run the model and save the labels. Otherwise, read the clustering results from the `labels_dir` specified
- Calculate entropies based on the clustering results and append to the profiles
- Save the various plots based on the implemented plot save functions

### Heatmap
Heatmap generates a heatmap that describes the profile composition of the buildings categorized according to the dominant clusters. The meta data for each building is also appended for visual comparison of the clustering-based benchmarking strategy against the traditional meta-data-based benchmarking strategy.

The following meta data fields are included:
- Industry
- PSU
- Climatezone
- Sqm
- EUI

It is also possible to sort the buildings within each dominant cluster by the next non-dominant cluster.

*Implementation Details*

`plot_heatmap` is the master function that implements the heatmap plotting process. It mainly makes use of the two functions `create_heatmap_df_mix` and `generate_heatmap2 ` to generate the heatmap matrix populated with color values to be plotted using Matplotlib. The steps are outlined below:

- Read profiles data and extract buildings information from the profiles
- Based on clustering results, extract proportions of each cluster for the buildings and append as additional columns
- Sort the buildings sequentially based on dominant cluster index
- Specify widths and heights of plot
- Specify color schemes to be used for specific meta data fields
- For buildings in a specific dominant cluster, reorder the proportions columns and corresponding colors to display the dominant cluster on the extreme left
- Convert proportions to cumulative values in order to access the index of the corresponding columns easily when building the heatmap matrix
- Build the heatmap matrix based on the various specifications
- Save the plotted figure to the specified save directory

### Tufte Table
`Tufte Table` builds a table of clustering results based on the principles for tufte plots. It hides the horizontal and vertical axes for each plot and shows the relative size of the clusters by the thickness of the average profile shapes.

*Detailed Steps*

- Separate profiles into residential and non-residential profiles
- For each subplot, determine the algorithm and k and retrieve the labels stored in `Clustering`
- Calculate thicknesses for the plots based on the retrieved results
- Reorder the clusters and thicknesses based on proximity between the average profiles
- Plot the results in a table

*Reordering Specifics*

Because each time, the labels generated by any clustering algorithm are random (cluster labelled as 0 could turn out to be 1 or 2 in a different iteration of the algorithm), we reorder the generated clusters, so clusters that are meant to be identical or related share the same color and thickness.

For vertical reordering across different values of k, the results from Bisecting K-Means is used. Specifically:

- For two consecutive k (e.g. 4 and 5), find the tolerance level (Euclidean distance between average profiles) that differentiate the new clusters that are broken down
- Find the tolerance level that extracts one row that was broken down from before
- Replace the row to be deleted with the first row to be added and add the second row to the tail
- Modify thicknesses data accordingly

For horizontal reordering across clustering results for different algorithms with the same value of k, the following steps are performed:

- Use the results from Bisecting K-Means as a benchmark
- For average profile shape of the first cluster discovered for Bisecting K-Means, find the cluster in the current algorithm (e.g. K-Means or GMM) that produces an average profile shape which is closest in Euclidean distance to the Bisecting K-Means average profile shape
- Append the average profile to a new list and append the corresponding thicknesses data to a new list
- Delete this average profile from the previous list for the current algorithm and k value
- Repeat this for all clusters and construct a reordered average profile shape list and a reordered thicknesses data list
- Repeat this for every algorithm different than Bisecting K-Means and every k
- Now we have matched the order of the average profiles between Bisecting K-Means and any other algorithm used based on close the average profiles are in terms of Euclidean distance

The vertical and horizontal matching algorithms ensure that the average profiles across different subplots that are close in distance would share the same color.

*Thicknesses Calculation*

The thicknesses of the average profiles plotted represent the number of profiles in the respective cluster. However, thicknesses calculation is not strictly proportional to the absolute value of the number of profiles. This is because in some cases, the thicknesses of the profile shapes may be too thin or too chick to be seen on the plot.

```
    def get_thickness(val, all_vals):
        std_val = np.std(all_vals)
        if std_val == 0:
            return 2.5
        mean_val = np.mean(all_vals)
        dev_val = (val-mean_val) / std_val
        dev_val = max(-1.5, min(dev_val, 5.5))
        return 2.5 + dev_val
```

From the code above, it can be seen that the number of profiles for each cluster across the different clusters is standardized and centered around 2.5. The values that fall below 1.0 and the values that go above 8.0 are then clipped to the minimum 1.0 and maximum 8.0 respectively. These values are used as the line widths while plotting the average profile shapes. Therefore, the thicknesses are used as an indicative value but do not represent the absolute value.

Also, the y range of each individual subplot is determined by the minimum and maximum value of all the average profile shapes for all subplots as can be seen below:

```
# Get ylim by finding the maximum value and minimum value for all the tufte data

# execute in final plotting procedure
def get_min_max(save_dir):
    max_val, min_val = 0, 0
    for i in range(1, 3*9+1):
        max_val = max(max_val, np.load('%s/order_%d.npy' % (save_dir, i)).max())
        min_val = min(min_val, np.load('%s/order_%d.npy' % (save_dir, i)).min())
    return (min_val, max_val)
```

### Clustering Validation Metrics

Since the data we have do not contain actual cluster labels (namely, they do not exist), we can only use unsupervised clustering validation metrics. Moreover, due to the time complexity of some popular clustering validation metrics like Silhouette Score and Dunn's Index which require the calculation of pairwise distances between data points, these metrics are left out of the current analysis.

The `Clustering Validation Metrics` notebook implements the following internal cluster validation metrics:

- cohesion
- separation
- calinski_harabaz_score
- DB: Davies-Bouldin index
- RS: R-squared
- RMSSTD: Root-mean-square std dev
- XB: Xie-Beni index

The implementation is based on the mathematical definitions of the indices listed in this paper:
http://datamining.rutgers.edu/publication/internalmeasures.pdf

I have also created two test cases with manually calculated metrics to check the correctness of implementation.

*Detailed Calculations*

**cohesion**

```
def cohesion(data, labels):
    clusters = sorted(set(labels))
    sse = 0
    for cluster in clusters:
        cluster_data = data[labels == cluster, :]
        centroid = cluster_data.mean(axis = 0)
        sse += ((cluster_data - centroid)**2).sum()
    return sse
```

Cohesion calculates the sum of squared distances from each data point to its respective centroid.

**separation**

```
def separation(data, labels, cohesion_score):
    # calculate separation as SST - SSE
    return cohesion(data, np.zeros(data.shape[0])) - cohesion_score
```

Separation calculation leverages the fact that the following equation always holds true: TSS = WSS + BSS

where TSS is the total sum of squared distances from each data point to the overall centroid. WSS is cohesion and BSS is separation.

**calinski_harabaz_score**

`calinski_harabaz_score` is calculated using Scikit Learn's implementation.

The Calinski-Harabasz index (CH) evaluates the cluster validity based on the average between- and within- cluster sum of squares. It is a ratio of cohesion and separation adjusted by the respective degrees of freedom.

Higher values of CH index indicate better clustering performance.

**Davies-Bouldin index**

```
def DB_find_max_j(clusters, centroids, i):
    max_val = 0
    max_j = 0
    for j in range(len(clusters)):
        if j == i:
            continue
        cluster_i_stat = within_cluster_dist_sum(clusters[i], centroids[i], i) / clusters[i].shape[0]
        cluster_j_stat = within_cluster_dist_sum(clusters[j], centroids[j], j) / clusters[j].shape[0]
        val = (cluster_i_stat + cluster_j_stat) / (((centroids[i] - centroids[j]) ** 2).sum() ** .5)
        if val > max_val:
            max_val = val
            max_j = j
    return max_val

def DB(data, clusters, centroids):
    result = 0
    for i in range(len(clusters)):
        result += DB_find_max_j(clusters, centroids, i)
    return result / len(clusters)
```

`Davies-Bouldin index` iterates every cluster and calculates a statistic using `DB_find_max_j`. Then, it averages the statistic over all clusters.

The statistic is calculated as follows:

- For every other cluster, calculate the average distance of every point in that cluster to its centroid
- Also calculate the average distance of every point in the current cluster to the centroid
- Add the two values together
- Divide the sum by the Euclidean distance between the two cluster centroids and obtain a candidate value
- Find the maximum value among all the candidate values for every other cluster to be the statistic

The smaller the index is, the better the clustering result is. By minimizing this index, clusters are the most distinct from each other, and therefore achieves the best partition.

**R-squared**

```
def RS(data, clusters, centroids):
    sst = SST(data)
    sse = SSE(clusters, centroids)
    return (sst - sse) / sst
```

`R-squared` can be expressed in terms of `separation` and `cohesion` as follows: `R-squared = separation / (cohesion + separation)`

**Root-mean-square std dev**

```
def RMSSTD(data, clusters, centroids):
    df = data.shape[0] - len(clusters)
    attribute_num = data.shape[1]
    return (SSE(clusters, centroids) / (attribute_num * df)) ** .5
```

`RMSSTD` first computes the the sum of squared distances from each data point to its respective centroid, which is `SSE` or `cohesion`. Then, it divides the value by the product of the number of attributes and the degree of freedom, which is calculated as the number of data points minus the number of clusters. Lastly, the we take the square root of the value to obtain `RMSSTD`.

**Xie-Beni index**

```
def XB(data, clusters, centroids):
    sse = SSE(clusters, centroids)
    min_dist = ((centroids[0] - centroids[1]) ** 2).sum()
    for centroid_i, centroid_j in list(product(centroids, centroids)):
        if (centroid_i - centroid_j).sum() == 0:
            continue
        dist = ((centroid_i - centroid_j) ** 2).sum()
        if dist < min_dist:
            min_dist = dist
    return sse / (data.shape[0] * min_dist)
```

`Xie-Beni index` first calculates `SSE` or `cohesion` by taking the sum of the squared distances from each data point to its respective centroid. We denote this by A. Then, it finds the minimum pairwise squared distances between cluster centroids. We denote this by B. We denote the number of data points as n. `Xie-Beni index` is calculated as `A / (n*B)`.

The `Xie-Beni index` defines the inter-cluster separation as the minimum square distance between cluster centers, and the intra-cluster compactness as the mean square distance between each data object and its cluster center. The optimal cluster number is reached when the minimum of `Xie-Beni index` is found.
