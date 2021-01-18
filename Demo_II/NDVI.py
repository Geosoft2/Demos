import xarray
import rasterio as rio


'''define import path and concrete files'''
R60_a = '../demodata/sentinel_raw'

# Open b4 and b8
b2a = rio.open(R60_a + '/T33SVB_20200815T095039_B02.jp2')
b4a = rio.open(R60_a + '/T33SVB_20200815T095039_B04.jp2')

# read Red(b4) and NIR(b8) as arrays
blue_a = b2a.read()
red_a = b4a.read()

'''convert bands to xarray'''

dataset = xarray.DataArray(dims=["null","Band","null","X","Y"], data=[[blue_a,red_a]])
print(dataset)

'''save as NetCDF'''
dataset.to_netcdf('../demodata/datacube_NDVI_2.nc', 'w', format='NETCDF4')
