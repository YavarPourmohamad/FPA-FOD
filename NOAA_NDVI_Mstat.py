import pandas as pd
import numpy as np
import xarray as xr
import calendar
import datetime
import glob
from tqdm.auto import tqdm
from dateutil.relativedelta import relativedelta

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 1992
end_year = 2020

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')

    FPA_FOD_NOAA_NDVI_M = pd.read_csv(filepath_or_buffer = FPA_FOD_file_list[0], sep = ',')
    FPA_FOD_NOAA_NDVI_M['Month'] = pd.DatetimeIndex(FPA_FOD_NOAA_NDVI_M['DISCOVERY_DATE']).month
    FPA_FOD_NOAA_NDVI_M[['NDVI_min', 'NDVI_max', 'NDVI_mean']] = None

    start_date = datetime.datetime.strptime(str(year), '%Y')

    while 1:
        month = start_date.month
        year = start_date.year
        points = FPA_FOD_NOAA_NDVI_M[(FPA_FOD_NOAA_NDVI_M['Year'] == year) & (FPA_FOD_NOAA_NDVI_M['Month'] == month)]
        if points.empty == True:
            break
        NDVI_mean, NDVI_min, NDVI_max = np.empty(len(points)), np.empty(len(points)), np.empty(len(points))
        for i in range(1, 13):
            start_date_L = start_date - relativedelta(months = i)
            month_L = start_date_L.strftime('%m')
            year_L = start_date_L.strftime('%Y')
            nc_files = glob.glob(pathname = f'Source_data/NOAA_NDVI/{year_L}{month_L}_NOAA_NDVI.nc')
            DS = xr.open_dataset(filename_or_obj = nc_files[0])
            DA = DS.sel(indexers = {'latitude': xr.DataArray(points['LATITUDE']),
                                    'longitude': xr.DataArray(points['LONGITUDE'])}, method = 'nearest')

            NDVI_mean = np.column_stack((NDVI_mean, DA.NDVI_mean.round(2).astype(str)))
            NDVI_min = np.column_stack((NDVI_min, DA.NDVI_min.round(2).astype(str)))
            NDVI_max = np.column_stack((NDVI_max, DA.NDVI_max.round(2).astype(str)))

        NDVI_mean = np.delete(NDVI_mean, 0, axis = 1)
        NDVI_mean = np.char.replace(np.array([str(l).strip("[]") for l in NDVI_mean]), '\n', '')

        NDVI_min = np.delete(NDVI_min, 0, axis = 1)
        NDVI_min = np.char.replace(np.array([str(l).strip("[]") for l in NDVI_min]), '\n', '')

        NDVI_max = np.delete(NDVI_max, 0, axis = 1)
        NDVI_max = np.char.replace(np.array([str(l).strip("[]") for l in NDVI_max]), '\n', '')

        start_date = start_date + relativedelta(months = 1)

        FPA_FOD_NOAA_NDVI_M.loc[(FPA_FOD_NOAA_NDVI_M['Year'] == year) & (FPA_FOD_NOAA_NDVI_M['Month'] == month), 'NDVI_mean'] = NDVI_mean
        FPA_FOD_NOAA_NDVI_M.loc[(FPA_FOD_NOAA_NDVI_M['Year'] == year) & (FPA_FOD_NOAA_NDVI_M['Month'] == month), 'NDVI_min'] = NDVI_min
        FPA_FOD_NOAA_NDVI_M.loc[(FPA_FOD_NOAA_NDVI_M['Year'] == year) & (FPA_FOD_NOAA_NDVI_M['Month'] == month), 'NDVI_max'] = NDVI_max

    FPA_FOD_NOAA_NDVI_M.to_csv(path_or_buf = f'NDVI/{year - 1}_FPA_FOD_NOAA_NDVI_M.csv', sep = ',', index = False)
