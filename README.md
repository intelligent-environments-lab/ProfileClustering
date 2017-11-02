# Profile Clustering Project with [BUDS Lab](http://www.budslab.org/) 

A project focused on extracting the right topology of building utilization from raw whole building sensor data

1. Data collection

- With multiple data sources (i.e., UTEXAS, MIT, PECAN, IRELAND, GENOME, ...), we choose .hdf5 data format to deal with a large size dataset. All the raw datasets are uploaded externally due to the limitation of uploading size. The transformation process is described in this Jupyter notebook ([Transformation(csv > hdf5)](Transformation_Code.ipynb)). After running transformation code, we would get a complete hdf5 file for the whole dataset, and this dataset has 4 attributes (i.e., location, industry, sub-industry, primary space usage, SQFT, EUI) 

2. Preprocessing

- We need to detect and eliminate outliers from the dataset. The detail outlier detection method is described in [here](Preprocessing_PILOT.ipynb).

3. metadata analysis

- You can find metadata analysis result for the datasets ([MIT](mit.ipynb), [UTEXAS](utexas.ipynb), [PECAN](pecan.ipynb), [GENOME](https://github.com/buds-lab/the-building-data-genome-project)). Combining all the datasets into a single .hdf5 file, we conducted a grand metadata analysis ([Metadata](Total.ipynb), [SQFT](GGplot.ipynb)).

3. Inner cluster analysis within a building

-

4. Cluster anlysis for all the buildings (vs EUI, program)

-
