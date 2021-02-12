# Demos
 The software demonstrations of the course "Geosoftware II" from the winter semester 20/21.

 **Note: The cells must be run sequentially. Otherwise we cant grantee the outcome!**
#### Used demodata

The demo data are datacubes which can be downloaded using this [jupyter notebook](./Downloads/Downloads Instructions.ipynb).  Theycome from two sources.

1. Satellite data for the NDVI from the EUs Copernicus program under these [terms](https://scihub.copernicus.eu/twiki/pub/SciHubWebPortal/TermsConditions/TC_Sentinel_Data_31072014.pdf).

2. A daily Sea surface temperature [dataset](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C01606) from 1981 to 2020 provided by the NOAA.

> Boyin; Liu, Chunying; Banzon, Viva F.; Freeman, Eric; Graham, Garrett; Hankins, Bill; Smith, Thomas M.; Zhang, Huai-Min. (2020): NOAA 0.25-degree Daily Optimum Interpolation Sea Surface Temperature (OISST), Version 2.1. [Subsets were Used]. NOAA National Centers for Environmental Information. https://doi.org/10.25921/RE9P-PT57. Accessed 24.01.2021.

#### Used Software

 You need [Python](https://www.python.org/) ( We have used 3.8.6) and [Docker](https://www.docker.com/). In addition the [openeo backend validator](https://github.com/Open-EO/openeo-backend-validator) must be installed.

##### Python Packages

 Software | Version
 ------ | ------
 *Standard Python Library* |
 [os](https://docs.python.org/3/library/os.html)   | -
 [sys](https://docs.python.org/3/library/sys.html)   | -
 [json](https://docs.python.org/3/library/json.html)  | -
 [datetime](https://docs.python.org/3/library/datetime.html)   | -
 [shutil](https://docs.python.org/3/library/shutil.html) | -
 [urllib](https://docs.python.org/3/library/urllib.html) | -
 [contextlib](https://docs.python.org/3/library/contextlib.html) | -
 [getpass](https://docs.python.org/3/library/getpass.html) | -
 [zipfile](https://docs.python.org/3/library/zipfile.html) | -
 [math](https://docs.python.org/3/library/math.html) | -
 [unittest](https://docs.python.org/3/library/unittest.html) | -
 [stat](https://docs.python.org/3/library/stat.html) | -
 [io](https://docs.python.org/3/library/io.html) | -
 *Other Packages* |
 [flask](https://flask.palletsprojects.com/en/1.1.x/)   | 1.1.2
 [xarray](http://xarray.pydata.org/en/stable/)   | 0.16.2
 [matplotlib](https://matplotlib.org/) | 3.3.2
 [netCDF4](https://unidata.github.io/netcdf4-python/netCDF4/index.html) | 1.5.4
 [cartopy](https://pypi.org/project/Cartopy/) | 0.18.0
 [holoviews](https://holoviews.org/) | 1.14.0
 [dask](https://dask.org/) | 2.30.0
 [rasterio](https://pypi.org/project/rasterio/) | 1.1.8
 [pytest](https://docs.pytest.org/en/stable/) | 6.1.2
 [progressbar2](https://pypi.org/project/progressbar2/) | 3.5.1
 [pandas](https://pandas.pydata.org/) | 1.1.4
 [geopandas](https://geopandas.org/) | 0.8.1
 [numpy](https://numpy.org/) | 1.19.3
 [sentinelsat](https://sentinelsat.readthedocs.io/en/master/api_overview.html) | 0.14
 [requests](https://requests.readthedocs.io/en/master/)   | 2.25.0
 [hvplot](https://hvplot.holoviz.org/) | 0.7.0 


 *Note: These are the versions used in the presentations. Other Version might work also.*
