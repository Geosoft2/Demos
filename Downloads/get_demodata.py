import xarray as xr
import matplotlib.pyplot as plt
import shutil
import urllib.request as request
from contextlib import closing
import netCDF4 as nc4
from ftplib import FTP
from datetime import datetime
import progressbar
import os
import sys

'''
Changed function from the first demo for SST datacubes
'''
def download_sst (year):
    '''
    Downloads the according file by given year from ftp server

    Parameters:
        year (int): The given year

    '''

    '''connect to FTP server'''
    start = datetime.now()
    ftp = FTP('ftp.cdc.noaa.gov')
    ftp.login()
    '''change path'''
    ftp.cwd('/Projects/Datasets/noaa.oisst.v2.highres/')

    '''List All Files'''
    files = ftp.nlst()
    '''initialize counter'''
    counter = 0

    '''Find files according to given year'''
    for file in files:

        if file == 'sst.day.mean.'+ str(year)+'.nc':
            print("Downloading..." + file)
            '''Insert other path here'''
            size = ftp.size(file)

            local = open( '../demodata' + '\\' + file, 'wb')

            pwidgets = [progressbar.Percentage(),' ',
                        progressbar.Bar(), ' ',
                        progressbar.FileTransferSpeed(), ' ',
                        progressbar.ETA(), ' ',
                        progressbar.DataSize(), '/', str(round(size*9.5367431640625*1e-7, 2)) + 'MiB' ]
            pbar = progressbar.ProgressBar( maxval= size, widgets=pwidgets)
            pbar.start()

            def file_write(data):
               local.write(data)
               nonlocal pbar
               pbar += len(data)

            ftp.retrbinary("RETR " + file ,file_write, 8*1024)
            ftp.close()
            end = datetime.now()
            diff = end - start
            print('All files downloaded for ' + str(diff.seconds) + 's')
        else: counter+=1

    if counter == len(files):
        print('No matching dataset found for this year')



def merge_datacubes(ds_merge):
    '''
    Merges datacubes by coordinates

    Parameters:
        ds_merge (xArray Dataset[]): Array of datasets to be merged

    Returns:
        ds1 (xArray Dataset): A single datacube with all merged datacubes
    '''

    start = datetime.now()
    if len(ds_merge) == 0:
        print("Error: No datacubes to merge", file=sys.stderr)
        return
    if len(ds_merge) == 1:
        return ds_merge[0]
    else:
        print('Start merging', file=sys.stderr)
        ds1 = ds_merge[0]
        count = 1
        while count < len(ds_merge):
            start1 = datetime.now()
            ds1 =  xr.combine_by_coords([ds1, ds_merge[count]], combine_attrs="override")
            count += 1
            diff = datetime.now() - start1
            print("Succesfully merged cube nr " + str(count) + " to the base cube in "+ str(diff.seconds) + 's', file=sys.stderr)
        diff = datetime.now() - start
        print('All cubes merged for ' + str(diff.seconds) + 's', file=sys.stderr)
        return ds1
