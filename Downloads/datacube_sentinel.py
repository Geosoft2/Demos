from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import geopandas as gpd
import getpass
import xarray as xr
import rasterio as rio
import os
import pandas as pd
import numpy as np
import shutil
from time import sleep
import stat
import io
from rasterio.enums import Resampling
import netCDF4 as nc
from datetime import datetime
from zipfile import ZipFile

def downloadingData (aoi, collectionDate, plName, prLevel, clouds,username,password,directory):
    '''
    Downloads the Sentinel2-Data with the given parameters

    Parameter:
        aoi(str) = The type and the coordinates of the area of interest
        collectionDate = The date of the data
        plName(str) = The name of the platform
        prLevel(str) = The name of the process
        clouds = The allowed percentage of the cloudcover
    '''
    api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')

    '''Choosing the data with bounding box (footprint), date, platformname, processinglevel and cloudcoverpercentage'''
    products = api.query(aoi, date = collectionDate, platformname = plName, processinglevel = prLevel, cloudcoverpercentage = clouds)

    '''Filters the products and sort the by cloudcoverpercentage'''
    products_gdf = api.to_geodataframe(products)
    products_gdf_sorted = products_gdf.sort_values(['cloudcoverpercentage'], ascending=[True])

    '''Downloads the choosen files from Scihub'''
    #saveFile(products_gdf_sorted)

    products_gdf_sorted.to_csv('w')
    api.download_all(products,directory, max_attempts=10, checksum=True)


def listDir (path):
    '''
    Lists all files from the given directory

    Parameter:
        path(str): Path to the directory

    Returns:
        path(str[]): An array of all filenames
    '''
    return os.listdir(path)


def unziping (filename, directory):
    '''
    Unzips the file with the given filename

    Parameter:
        filename(str): Name of the .zip file
    '''
    with ZipFile(os.path.join(directory, filename), 'r') as zipObj:
        zipObj.extractall(directory)

def delete (path):
    '''
    Deletes the file/directory with the given path

    Parameter:
        path(str): Path to the file/directory
    '''
    if os.path.exists(path):
        os.remove(path)
        print("File deleted: " + path)
    else:
        print("The file does not exist")

def extractBands (filename,resolution, directory):
    '''
    Extracts bandpaths from .SAFE file

    Parameter:
        filename(str): Sentinel .SAFE file

    Returns:
        bandPaths(str[]): An array of the paths for the red and nir band
    '''
    lTwoA = listDir(os.path.join(directory, filename, "GRANULE"))

    if resolution == 60:
        bandName = listDir (os.path.join(directory, filename, "GRANULE", str(lTwoA[0]), "IMG_DATA", "R60m"))
        pathRed = os.path.join(directory, filename, "GRANULE", str(lTwoA[0]), "IMG_DATA", "R60m", str(bandName[4]))
        pathNIR = os.path.join(directory, filename, "GRANULE", str(lTwoA[0]), "IMG_DATA", "R60m", str(bandName[11]))
        bandPaths = [pathRed, pathNIR]

    elif resolution == 20:
        bandName = listDir (os.path.join(directory, filename, "GRANULE", str(lTwoA[0]), "IMG_DATA", "R20m"))
        pathRed = os.path.join(directory, filename, "GRANULE", str(lTwoA[0]), "IMG_DATA", "R20m", str(bandName[3]))
        pathNIR = os.path.join(directory, filename, "GRANULE", str(lTwoA[0]), "IMG_DATA", "R20m", str(bandName[9]))
        bandPaths = [pathRed, pathNIR]

    elif resolution == 10:
        bandName = listDir (os.path.join(directory, filename, "GRANULE", str(lTwoA[0]), "IMG_DATA", "R10m"))
        pathRed = os.path.join(directory, filename, "GRANULE", str(lTwoA[0]), "IMG_DATA", "R10m", str(bandName[3]))
        pathNIR = os.path.join(directory, filename, "GRANULE", str(lTwoA[0]), "IMG_DATA", "R10m", str(bandName[4]))
        bandPaths = [pathRed, pathNIR]

    elif resolution == 100:
        bandName = listDir (os.path.join(directory, filename, "GRANULE", str(lTwoA[0]), "IMG_DATA", "R20m"))
        pathRed = os.path.join(directory, filename, "GRANULE", str(lTwoA[0]), "IMG_DATA", "R20m", str(bandName[3]))
        pathNIR = os.path.join(directory, filename, "GRANULE", str(lTwoA[0]), "IMG_DATA", "R20m", str(bandName[9]))
        bandPaths = [pathRed, pathNIR]
    else:
        print("no such resolution")
        return -1

    return bandPaths


def loadBand (bandpath,date,tile,resolution, clouds, plName, prLevel, directory):
    '''
    Opens and reads the red and nir band, saves them as NetCDF file

    Parameter:
        bandPaths(str[]): Array with the paths to the red and nir band
    '''
    b4 = rio.open(bandpath[0])
    b8 = rio.open(bandpath[1])
    red = b4.read()
    nir = b8.read()

    if resolution==10:
        res=1830*3*2
    elif resolution == 20:
        res = 1830*3
    elif resolution == 60:
        res = 1830
    elif resolution == 100:
        res = 1098
    else:
        print("No such resolution")
        return -1

    j=res-1
    i=0
    lat = [0]*res
    lon = [0]*res
    while j>=0:
        lon[i]=b4.bounds.left + i*resolution
        lat[i]=b4.bounds.bottom + j*resolution
        i=i+1
        j=j-1

    time = pd.date_range(date, periods=1)


    if resolution == 100:
        upscale_factor = (1/5)
        # resample data to target shape
        nir = b8.read(
               out_shape=(
                   b8.count,
                   int(b8.height * upscale_factor),
                   int(b8.width * upscale_factor)
                ),
                resampling=Resampling.bilinear)
            # scale image transform
        transform = b8.transform * b8.transform.scale(
                (b8.width / nir.shape[-1]),
                (b8.height / nir.shape[-2])
            )

        red = b4.read(
               out_shape=(
                   b4.count,
                   int(b4.height * upscale_factor),
                   int(b4.width * upscale_factor)
                ),
                resampling=Resampling.bilinear
            )

            # scale image transform
        transform = b4.transform * b4.transform.scale(
                (b4.width / red.shape[-1]),
                (b4.height / red.shape[-2])
            )

    dataset = xr.Dataset(
          {
        "red": (["time","lat", "lon"], red),
        "nir": (["time","lat", "lon"], nir)
        },
         coords=dict(
            time=time,
            lat=(["lat"], lat),
            lon=(["lon"], lon),
        ),
         attrs=dict(
             platform= plName,
             processingLevel= prLevel,
             cloudcover = clouds,
             source = "https://scihub.copernicus.eu/dhus",
             resolution= str(resolution) +" x "+ str(resolution)+" m"
         ),
    )


    dataset.to_netcdf(directory+"datacube_"+str(date)+"_"+str(tile)+"_R"+str(resolution)+".nc", 'w', format='NETCDF4')
    b4.close()
    b8.close()
    return dataset



def getDate(filename):
    '''
    extracts the Date of the Sentinelfilename
    Parameters:
        filename (str): name of the file
    Returns:
        (str): Date of the File ("2020-12-31")
    '''
    return filename[11:15]+"-"+filename[15:17]+"-"+filename[17:19]



def getTile(filename):
    '''
    extracts the UTM-tile of the Sentinelfilename
    Parameters:
        filename (str): name of the file
    Returns:
        (str): UTM-tile of the File ("31UMC")
    '''
    return filename[38:44]



def on_rm_error( func, path, exc_info):
       # path contains the path of the file that couldn't be removed
       # let's just assume that it's read-only and unlink it.
       os.chmod( path, stat.S_IWRITE )
       os.unlink( path )



def unzip(directory, deleteZip):
    '''

    '''
    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            unziping(filename, directory)
            if deleteZip == True:
                delete(os.path.join(directory, filename))
                continue
            else:
                continue
            continue
        else:
            continue



def buildCube(directory, deleteSafe, resolution, clouds, plName, prLevel):
    '''

    '''
    for filename in os.listdir(directory):
        if filename.endswith(".SAFE"):
            bandPath = extractBands(os.path.join(directory, filename),resolution, directory)
            band = loadBand(bandPath,getDate(filename),getTile(filename),resolution, clouds, plName, prLevel, directory)
            if deleteSafe==True:
                shutil.rmtree(os.path.join(directory, filename) , onerror = on_rm_error)
                continue
            else:
                continue
            print(" ")
            continue
        else:
            continue



def main(resolution, directory, collectionDate, aoi, clouds, username, password, deleteZip, deleteSafe):
    plName = 'Sentinel-2'
    prLevel = 'Level-2A'
    downloadingData (aoi, collectionDate, plName, prLevel, clouds, username, password, directory)
    unzip(directory, deleteZip)
    buildCube(directory, deleteSafe, resolution, clouds, plName, prLevel)

def merge_datacubes(ds_merge):
    '''
    merges datacubes by coordinates

    Parameters:
        ds_merge (array): array of datasets to be mearched

    Returns:
        ds1 (ds): A single datacube with all merged datacubes
        - Error, if no Datacubes given
    '''
    start = datetime.now()
    if len(ds_merge) == 0:
        print("error")
        return
    if len(ds_merge) == 1:
        return ds_merge[0]
    else:
        print('start merging')
        ds1 = ds_merge[0]
        count = 1
        while count < len(ds_merge):
            start1 = datetime.now()
            ds1 =  xr.combine_by_coords([ds1,ds_merge[count]],compat="override")
            count+=1
            print("succesfully merged cube nr "+ str(count)+" to the base cube ")
            end = datetime.now()
            diff = end - start1
            print('All cubes merged for ' + str(diff.seconds) + 's')
        print("result: ")
        print(ds1)
        end = datetime.now()
        diff = end - start
        print('All cubes merged for ' + str(diff.seconds) + 's')
        return ds1



def timeframe(ds,start,end):
    '''
    Slices Datacube down to given timeframe

    Parameters:
        ds (ds): source dataset
        start (str): start of the timeframe eg '2018-07-13'
        end (str): end of the timeframe eg '2018-08-23'

    Returns:
        ds_selected (ds): dataset sliced to timeframe
    '''
    if start>end:
        print("start and end of the timeframe do are not compatible!")
    else:
        ds_selected = ds.sel(time = slice(start,end))
        #print(ds_selected)
        return ds_selected



def safe_datacube(ds, timeframe):
    '''
    Saves the Datacube as NetCDF (.nc)

    Parameters:
        ds (ds): source dataset
        timeframe (str): timeframe eg '2017', '2015_2019'
    '''
    print("start saving")
    if type(timeframe) != str:
        timeframe=str(timeframe)
    ds.to_netcdf(systempath+ "sst.day.mean."+timeframe+".nc")
    print("done saving")
