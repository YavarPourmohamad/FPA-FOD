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
start_year = 2019
end_year = 2020

for year in tqdm(range(start_year, end_year + 1)):
    print(year)
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_NOAA_NDVI = pd.read_csv(filepath_or_buffer = FPA_FOD_file_list[0], sep = ',')
    FPA_FOD_NOAA_NDVI['NDVI-1day'] = None
    date = FPA_FOD_NOAA_NDVI['DISCOVERY_DATE'].unique()
    for day in date:
        points = FPA_FOD_NOAA_NDVI[FPA_FOD_NOAA_NDVI['DISCOVERY_DATE'] == day]

        day1 = datetime.datetime.strptime(day, '%Y-%m-%d') - datetime.timedelta(days = 1)
        year2 = day1.strftime('%Y')
        month2 = day1.strftime('%m')
        day2 = day1.strftime('%d')
        nc_files = glob.glob(pathname = f'Source_data/NOAA_NDVI/*_{year2}{month2}{day2}_*.nc')
        if bool(nc_files) == False:
            continue
        DS = xr.open_dataset(filename_or_obj = nc_files[0])
        DA = DS.sel(indexers = {'latitude': xr.DataArray(points['LATITUDE']),
                                'longitude': xr.DataArray(points['LONGITUDE'])}, method = 'nearest')
        FPA_FOD_NOAA_NDVI.loc[FPA_FOD_NOAA_NDVI['DISCOVERY_DATE'] == day, 'NDVI-1day'] = DA.NDVI[0]
    
    FPA_FOD_NOAA_NDVI.to_csv(path_or_buf = f'NDVI/{year}_FPA_FOD_NOAA_NDVI.csv', sep = ',', index = False)

