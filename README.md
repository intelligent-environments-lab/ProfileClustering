# Profile Clustering Project with [BUDS Lab](http://www.budslab.org/) 

A project focused on extracting the right topology of building utilization from raw whole building sensor data

1. Data collection & Preprocessing

- With multiple data sources (i.e., UTEXAS, MIT, PECAN, IRELAND, GENOME, ...), we choose .hdf5 data format to deal with a large size dataset. All the raw datasets are uploaded externally due to the limitation of uploading size. The data is transformed as .hdf5 file format, and the outliers are detected and eliminated. After running two ipython notebook below, we would get a complete hdf5 file for the whole dataset with complete metadata. 

- [data_collection_1](data_collection_1.ipynb) : Read temporal dataset and metadata (i.e., Industry, Sub-industry, Primary usage type, Region, Area) to generate .hdf5 file.

- [data_collection_2](data_collection_2.ipynb) : Explain outlier prunning method and how we fill outliers. In addition, Energy use intensity (kBtu/sqft) is calculated and stored as metadata.

2. metadata analysis

- You can find metadata analysis result for the datasets.

- For each dataset: [MIT](mit.ipynb), [UTEXAS](utexas.ipynb), [PECAN](pecan.ipynb), [IRELAND](ireland.ipynb), [GENOME](https://github.com/buds-lab/the-building-data-genome-project). 

- Based on industry type: [Total](Total.ipynb), [Total_area](GGplot.ipynb), [Non-residential](meta_nonresi.ipynb), [Residential](meta_resi.ipynb). 

3. Clustering analysis (vs metadata)

-


