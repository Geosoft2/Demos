import xarray as xr
import dask
import matplotlib.pyplot as plt
import holoviews as hv
from holoviews.operation.datashader import datashade

hv.extension('bokeh', width=100)

def createSubset(ds, minLon, minLat, maxLon, maxLat):
  '''
  Erstellt ein räumliches Subset.

  Parameter:
    ds (dask dataset): Dataset, aus dem ein Subset genommen werden soll.
    minLon (double): linker Wert
    minLat (double): unterer Wert
    maxLon (double): rechter Wert
    maxLat (double): oberer Wert

  Returns:
    ds_subset (dask dataset): Räumlich begrenztes Dataset.
  '''
  if (minLon > maxLon):
    ds_subset1 = ds.sel(lon=slice(minLon, 360), lat=slice(minLat, maxLat))
    ds_subset2 = ds.sel(lon=slice(0, maxLon), lat=slice(minLat, maxLat))
    ds_subset_concat = xr.concat([ds_subset1, ds_subset2], "lon")
    return ds_subset_concat
  else:
    ds_subset = ds.sel(lon=slice(minLon, maxLon), lat=slice(minLat, maxLat))
    return ds_subset

def mean_sst(timeframe, bbox = [0,-90,360,90]):
  '''
  Berechnet die durchschnittliche Meeresoberflächentemperatur.

  Parameter:
    timeframe ([str]): Array mit zwei Einträgen für Anfangs- und Enddatum, z.B. ['1981-10-01','1981-11-01'].
    bbox ([double]): optional, Array mit vier Einträgen: min Longitude, min Latitude, max Longitude, max Latitude.

  Returns:
    ds_timeframe_mean (dask dataset): Dataset mit durchschnittlichen Meeresoberflächentemperaturen.
  '''
  start = timeframe[0]
  end = timeframe[1]
  start_year_str = start[0:4]
  end_year_str = end[0:4]
  start_year = int(start_year_str)
  end_year = int(end_year_str)
  if (start == end):
    ds = xr.open_dataset("./sst.day.mean." + start_year_str + ".nc")
    ds_day = ds.sel(time=start)
    if (bbox != [0,-90,360,90]):
      ds_day = createSubset(ds_day, bbox[0], bbox[1], bbox[2], bbox[3])
    return ds_day
  elif (start_year_str == end_year_str):
    ds = xr.open_dataset("./sst.day.mean." + start_year_str + ".nc", chunks={"time": 100})
    ds_timeframe = ds.sel(time=slice(start, end))
    if (bbox != [0,-90,360,90]):
      ds_timeframe = createSubset(ds_timeframe, bbox[0], bbox[1], bbox[2], bbox[3])
    ds_timeframe_mean = ds_timeframe.sst.mean(dim=('time'))
    return ds_timeframe_mean.compute()
  else:
    list = []
    for x in range(start_year, end_year+1):
      list.append("./sst.day.mean." + str(x) + ".nc")
    ds = xr.open_mfdataset(list, parallel=True, chunks={"time": 100})
    ds_timeframe = ds.sel(time=slice(start, end))
    if (bbox != [0,-90,360,90]):
      ds_timeframe = createSubset(ds_timeframe, bbox[0], bbox[1], bbox[2], bbox[3])
    ds_timeframe_mean = ds_timeframe.sst.mean(dim=('time'))
    return ds_timeframe_mean.compute()

def min360(x):
  if x > 180:
    return x-360
  else:
    return x
