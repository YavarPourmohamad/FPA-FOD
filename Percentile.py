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

for year in range(start_year, end_year + 1):
    file_list = glob.glob(pathname = f'Climate_daily/{year}_FPA_FOD_climate.csv')
    FPA_FOD_cli_percen = pd.read_csv(filepath_or_buffer = file_list[0], sep = ',')
    dates = FPA_FOD_cli_percen['DISCOVERY_DATE'].unique()

    nc_files = glob.glob(pathname = 'Source_data/Climate_Percentile/*.nc')
    for j in tqdm(nc_files):
      DS = xr.open_dataset(filename_or_obj = j)
      col = j.split(sep = '_')[-1].split(sep = '.')[0]
      j = j.split(sep = '_')[3]
      print(f'{j}_{col}')
      FPA_FOD_cli_percen[j + '_' + col] = None
      for i in dates:
        points = FPA_FOD_cli_percen[FPA_FOD_cli_percen['DISCOVERY_DATE'] == i]
        doy = int(datetime.datetime.strptime(i, '%Y-%m-%d').strftime('%j'))
        if calendar.isleap(year) == False and doy > 59:
            doy += 1
        DA = DS.sel(indexers = {'lat': xr.DataArray(points['LATITUDE']), 
                                'lon': xr.DataArray(points['LONGITUDE']), 
                                'time': f'{doy} days'}, method = 'nearest')
        FPA_FOD_cli_percen.loc[FPA_FOD_cli_percen['DISCOVERY_DATE'] == i, j + '_' + col] = DA[col].values

    for j in tqdm(nc_files):
      j = j.split(sep = '_')[3]
      print(j)
      FPA_FOD_cli_percen[j + '_Percentile'] = None
      if j == 'vpd':
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p98']), j + '_Percentile'] = '>98%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p95']) & (FPA_FOD_cli_percen[j + '_p98'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '95-98%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p90']) & (FPA_FOD_cli_percen[j + '_p95'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '90-95%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p80']) & (FPA_FOD_cli_percen[j + '_p90'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '80-90%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p70']) & (FPA_FOD_cli_percen[j + '_p80'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '70-80%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p50']) & (FPA_FOD_cli_percen[j + '_p70'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '50-70%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p30']) & (FPA_FOD_cli_percen[j + '_p50'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '30-50%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p20']) & (FPA_FOD_cli_percen[j + '_p30'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '20-30%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p10']) & (FPA_FOD_cli_percen[j + '_p20'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '10-20%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p5']) & (FPA_FOD_cli_percen[j + '_p10'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '5-10%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p2']) & (FPA_FOD_cli_percen[j + '_p5'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '2-5%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] < FPA_FOD_cli_percen[j + '_p2']), j + '_Percentile'] = '<2%'
#      elif j == 'eto':
#        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p95']), j + '_Percentile'] = '>95%'
#        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p90']) & (FPA_FOD_cli_percen[j + '_p95'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '90-95%'
#        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p70']) & (FPA_FOD_cli_percen[j + '_p90'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '70-90%'
#        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p50']) & (FPA_FOD_cli_percen[j + '_p70'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '50-70%'
#        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p30']) & (FPA_FOD_cli_percen[j + '_p50'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '30-50%'
#        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p10']) & (FPA_FOD_cli_percen[j + '_p30'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '10-30%'
#        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p5']) & (FPA_FOD_cli_percen[j + '_p10'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '10-30%'
#        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] < FPA_FOD_cli_percen[j + '_p5']), j + '_Percentile'] = '<10%'
      else:
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p90']), j + '_Percentile'] = '>90%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p70']) & (FPA_FOD_cli_percen[j + '_p90'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '70-90%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p50']) & (FPA_FOD_cli_percen[j + '_p70'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '50-70%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p30']) & (FPA_FOD_cli_percen[j + '_p50'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '30-50%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] > FPA_FOD_cli_percen[j + '_p10']) & (FPA_FOD_cli_percen[j + '_p30'] > FPA_FOD_cli_percen[j]), j + '_Percentile'] = '10-30%'
        FPA_FOD_cli_percen.loc[(FPA_FOD_cli_percen[j] < FPA_FOD_cli_percen[j + '_p10']), j + '_Percentile'] = '<10%'

    drop_list = []
    for i in range(len(nc_files)):
      value = nc_files[i].split(sep = '_')[3]
      per = nc_files[i].split(sep = '_')[-1].split(sep = '.')[0]
      drop_list.append(value + '_' + per)

    FPA_FOD_cli_percen = FPA_FOD_cli_percen.drop(labels = drop_list, axis = 1)

    col = ['DISCOVERY_DATE', 'Year', 'LATITUDE', 'LONGITUDE', 'FIRE_SIZE', 'NWCG_GENERAL_CAUSE', 'OWNER_DESCR', 'STATE', 'pr', 'tmmn', 'tmmx', 'rmin', 'rmax', 'sph', 'vs', 'th', 'srad', 'etr', 'fm100', 'fm1000', 'bi', 'vpd', 'erc',
           'pr_5D_mean', 'tmmn_5D_mean', 'tmmx_5D_mean', 'rmin_5D_mean', 'rmax_5D_mean', 'sph_5D_mean', 'vs_5D_mean', 'th_5D_mean', 'srad_5D_mean', 'etr_5D_mean', 'fm100_5D_mean', 'fm1000_5D_mean', 'bi_5D_mean', 'vpd_5D_mean', 'erc_5D_mean',
           'pr_5D_min', 'pr_5D_max', 'tmmn_5D_max', 'tmmx_5D_max', 'rmin_5D_min', 'rmax_5D_min', 'sph_5D_min', 'vs_5D_max', 'th_5D_max', 'srad_5D_max', 'etr_5D_max', 'fm100_5D_min', 'fm1000_5D_min', 'bi_5D_max', 'vpd_5D_max', 'erc_5D_max', 
           'tmmn_Percentile', 'tmmx_Percentile', 'sph_Percentile', 'vs_Percentile', 'fm100_Percentile', 'bi_Percentile', 'vpd_Percentile', 'erc_Percentile', ]
    FPA_FOD_cli_percen = FPA_FOD_cli_percen[col]

    FPA_FOD_cli_percen.to_csv(path_or_buf = f'Climate_percentile/{year}_FPA_FOD_Cli_Per.csv', sep = ',', index = False)
    del FPA_FOD_cli_percen

