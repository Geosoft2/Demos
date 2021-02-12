import matplotlib.pyplot as plt
import xarray as xr
import os
import sys

def convert_nc_to_png():

    files = os.listdir(os.getcwd() + '//data')
    paths = [os.path.join(os.getcwd() + '//data', basename) for basename in files]
    newest = max(paths, key=os.path.getctime)
    nc = xr.open_dataset(newest)

    # examine the variables
    title = ""
    topo = ""
    cmap = ""


    if(sys.argv[1] == "mean_sst"):
        title = "SST"
        topo = nc.sst[::10,::10]
        cmap = "coolwarm"
    else:
        title = "NDVI"
        topo = nc.__xarray_dataarray_variable__[380:480,1000:1098] * -1
        cmap = "BrBG"
    

    # make image
    plt.figure(figsize=(5,5))
    plt.imshow(topo,origin='lower', cmap=cmap) 
    plt.title(title)
    plt.savefig('.//data//nc_preview.png', bbox_inches='tight')


if __name__ == "__main__":
    convert_nc_to_png()