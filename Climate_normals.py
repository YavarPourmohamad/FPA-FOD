import pandas as pd
import numpy as np
import geopandas as gpd
import xarray as xr
import sqlite3
import rtree
import geemap
import glob
import datetime
import wget
import calendar
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_CN = pd.read_csv(filepath_or_buffer = FPA_FOD_file_list[0], sep = ',')
    nc_files = glob.glob(pathname = 'Source_data/Normals/*.nc')
    for j in tqdm(nc_files):
      col = j.split(sep = '_')[2]
      FPA_FOD_CN[col + '_Normal'] = None
      print(col)
      if col == 'rmin' or col == 'rmax' or col == 'fm1000':
        DS = xr.open_dataset(filename_or_obj = j, decode_times = False)
        for i in range(len(FPA_FOD_CN)):
          point = FPA_FOD_CN.iloc[i]
          date_strp = datetime.datetime.strptime(point['DISCOVERY_DATE'], '%Y-%m-%d')
          if calendar.isleap(year = year):
            if date_strp >= datetime.datetime.strptime(f'{year}-2-29', '%Y-%m-%d'):
              doy = float(date_strp.strftime('%j')) - 1
              DA = DS.sel(indexers = {'lat': point['LATITUDE'],
                                      'lon': point['LONGITUDE']}, method = 'nearest')
              DA = DA.to_dataframe()
              FPA_FOD_CN[col + '_Normal'].iloc[[i]] = DA[DA['days'] == float(doy)][col].values
            continue
          doy = float(date_strp.strftime('%j'))
          DA = DS.sel(indexers = {'lat': point['LATITUDE'], 
                                  'lon': point['LONGITUDE']}, method = 'nearest')
          DA = DA.to_dataframe()
          FPA_FOD_CN[col + '_Normal'].iloc[[i]] = DA[DA['days'] == float(doy)][col].values
        continue
      DS = xr.open_dataset(filename_or_obj = j, decode_times = True)
      for i in range(len(FPA_FOD_CN)):
        point = FPA_FOD_CN.iloc[i]
        doy = int(datetime.datetime.strptime(point['DISCOVERY_DATE'], '%Y-%m-%d').strftime('%j'))
        DA = DS.sel(indexers = {'lat': point['LATITUDE'], 
                                'lon': point['LONGITUDE'], 
                                'time': str(doy) + ' days'}, method = 'nearest')
        FPA_FOD_CN[col + '_Normal'].iloc[[i]] = DA[col].values

    col = ['DISCOVERY_DATE', 'NWCG_GENERAL_CAUSE', 'FIRE_SIZE', 'LATITUDE', 'LONGITUDE', 'OWNER_DESCR', 'STATE', 'Year',
           'ppt_Normal', 'tmmn_Normal', 'tmmx_Normal', 'rmin_Normal', 'rmax_Normal', 'sph_Normal', 'srad_Normal', 
           'fm100_Normal', 'fm1000_Normal', 'bi_Normal', 'vpd_Normal', 'erc_Normal']
    FPA_FOD_CN = FPA_FOD_CN[col]
    FPA_FOD_CN.columns = ['DISCOVERY_DATE', 'NWCG_GENERAL_CAUSE', 'FIRE_SIZE', 'LATITUDE', 'LONGITUDE', 'OWNER_DESCR', 'STATE',
                          'Year', 'pr_Normal', 'tmmn_Normal', 'tmmx_Normal', 'rmin_Normal', 'rmax_Normal', 'sph_Normal',
                          'srad_Normal', 'fm100_Normal', 'fm1000_Normal', 'bi_Normal', 'vpd_Normal', 'erc_Normal']
    FPA_FOD_CN.to_csv(path_or_buf = f'Climate_normals/{year}_FPA_FOD_CN.csv', sep = ',', index = False)
    del FPA_FOD_CN

