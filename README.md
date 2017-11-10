# Profile Clustering Project with [BUDS Lab](http://www.budslab.org/) 

A project focused on extracting the right topology of building utilization from raw whole building sensor data

1. Data collection

- With multiple data sources (i.e., UTEXAS, MIT, PECAN, IRELAND, GENOME, ...), we choose .hdf5 data format to deal with a large size dataset. All the raw datasets are uploaded externally due to the limitation of uploading size. The transformation process is conducted by two stages. After running two ipython notebook below, we would get a complete hdf5 file for the whole dataset. 

- [data_collection_1](data_collection_1.ipynb) : Read temporal dataset and metadata (i.e., Industry, Sub-industry, Primary usage type, Region, Area) to generate .hdf5 file.

- [data_collection_2](data_collection_2.ipynb) : Explain outlier prunning method and apply [loadshape library](https://pypi.python.org/pypi/loadshape/) to fill outliers. In addition, Energy use intensity (kBtu/sqft) is calculated and stored as metadata.

2. Preprocessing

- We need to detect and eliminate outliers from the dataset. The detail outlier detection method is described in [here](Preprocessing_PILOT.ipynb).

3. metadata analysis

- You can find metadata analysis result for the datasets ([MIT](mit.ipynb), [UTEXAS](utexas.ipynb), [PECAN](pecan.ipynb), [GENOME](https://github.com/buds-lab/the-building-data-genome-project)). Combining all the datasets into a single .hdf5 file, we conducted a grand metadata analysis ([Metadata](Total.ipynb), [SQFT](GGplot.ipynb)).

4. Inner cluster analysis within a building

-

5. Cluster anlysis for all the buildings (vs EUI, program)

-
