# NDVI Time Series Task

The repository contains a Python program that computes the NDVI time series for the given images and locations.

## Installation
Follow installation instructions to use the program.
### Clone repository
Navigate to your working directory and clone the repository.
```
git clone https://github.com/danielm09/NDVI_Analysis_Task.git
```
### Install dependencies
The program requires the following packages installed: numpy, pandas, geopandas, rasterio and matplotlib.
Use the environment.yml file to create conda environment with required packages.
```
conda env create -f environment.yml
```
> *Make sure the command is executed from the NDVI_Analysis_Task directory.*

Activate conda environment.
```
conda activate task_ecostack
```
## Usage
Run main.py to create a time series chart.
```
python main.py
```

Optionally, use the [Jupyter Notebook](visualize_ndvi_time_series.ipynb)

