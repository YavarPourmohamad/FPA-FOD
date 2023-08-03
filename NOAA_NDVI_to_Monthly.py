import pandas as pd
import numpy as np
import xarray as xr
import calendar
import datetime
import glob
from tqdm.auto import tqdm
from dateutil.relativedelta import relativedelta

start_date = '2017-01'
start_date = datetime.datetime.strptime(start_date, '%Y-%m')

nc_files = 1
pbar = tqdm(total = 36)

while nc_files:
    year = start_date.strftime('%Y')
    month = start_date.strftime('%m')
    nc_files = glob.glob(pathname = f'Source_data/NOAA_NDVI/VIIRS-Land*{year}{month}*.nc')
    if bool(nc_files) == False:
        break
    dataset = []
    for nc in nc_files:
        DS = xr.open_dataset(filename_or_obj = nc)
        DS = DS.drop(labels = ['crs', 'lat_bnds', 'lon_bnds', 'TIMEOFDAY', 'QA'])
        dataset.append(DS)
    dataset = xr.concat(dataset, dim = 'time')
    
    dataset = dataset.assign(NDVI_min = dataset.min('time').NDVI)
    dataset = dataset.assign(NDVI_max = dataset.max('time').NDVI)
    dataset = dataset.assign(NDVI_mean = dataset.mean('time').NDVI)
    dataset = dataset.drop(labels = 'NDVI')
    
    dataset = dataset.assign_coords(time = np.datetime64(start_date.strftime('%Y-%m')).flatten())
    
    dataset.to_netcdf(path = f'Source_data/NOAA_NDVI/{year}{month}_NOAA_NDVI.nc')
    
    start_date = start_date + relativedelta(months = 1)
    pbar.update(1)

