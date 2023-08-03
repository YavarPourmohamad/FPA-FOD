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
    print(year)
    nc_files = glob.glob(pathname = f'Source_data/GRIDMET/*{year}.nc')
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_climate = pd.read_csv(FPA_FOD_file_list[0], sep = ',')
    dates = FPA_FOD_climate['DISCOVERY_DATE'].unique()
    for j in tqdm(nc_files):
        DS = xr.open_dataset(filename_or_obj = j, decode_times = True)
        j = j.split(sep = '/')[-1].split(sep = '_')[0]
        FPA_FOD_climate[j] = None
        print(f'Variable: {j}')
        for i in tqdm(dates):
            points = FPA_FOD_climate[FPA_FOD_climate['DISCOVERY_DATE'] == i]
            DA = DS.sel(indexers = {'lat': xr.DataArray(points['LATITUDE']),
                            'lon': xr.DataArray(points['LONGITUDE']),
                            'day': i, 'crs': 3}, method = 'nearest')
            DA.to_dataframe()
            if j == 'pr':
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['precipitation_amount'].values
            elif (j == 'rmax') or (j == 'rmin'):
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['relative_humidity'].values
            elif j == 'sph':
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['specific_humidity'].values
            elif j == 'srad':
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['surface_downwelling_shortwave_flux_in_air'].values
            elif j == 'th':
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['wind_from_direction'].values
            elif (j == 'tmmn') or (j == 'tmmx'):
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['air_temperature'].values
            elif j == 'vs':
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['wind_speed'].values
            elif j == 'erc':
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['energy_release_component-g'].values
            elif j == 'bi':
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['burning_index_g'].values
            elif j == 'fm100':
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['dead_fuel_moisture_100hr'].values
            elif j == 'fm1000':
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['dead_fuel_moisture_1000hr'].values
            elif j == 'etr':
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['potential_evapotranspiration'].values
            elif j == 'vpd':
              FPA_FOD_climate.loc[FPA_FOD_climate['DISCOVERY_DATE'] == i, j] = DA['mean_vapor_pressure_deficit'].values
    for j in tqdm(nc_files):
        DS = xr.open_dataset(filename_or_obj = j, decode_times = True)
        j = j.replace(str(year), str(year - 1))
        DS0 = xr.open_dataset(filename_or_obj = j, decode_times = True)
        j = j.replace(str(year - 1), str(year + 1))
        DS1 = xr.open_dataset(filename_or_obj = j, decode_times = True)
        col = j.split(sep = '/')[-1].split(sep = '_')[0]
        FPA_FOD_climate[[col + '_5D_mean', col + '_5D_min', col + '_5D_max']] = None
        for i in range(len(FPA_FOD_climate)):
            point = FPA_FOD_climate.iloc[i]
            point_date = pd.to_datetime(point['DISCOVERY_DATE'])
            start_date = point_date + datetime.timedelta(days = -2)
            range_date = [start_date + datetime.timedelta(days = x) for x in range(5)]
            doy = list(range(1, 367 if calendar.isleap(year) else 366))
            if point_date.day_of_year in (1, 2):
                DA = DS.sel(indexers = {'lat': point['LATITUDE'],
                                        'lon': point['LONGITUDE'],
                                        'crs': 3}, method = 'nearest')
                DA0 = DS0.sel(indexers = {'lat': point['LATITUDE'],
                                          'lon': point['LONGITUDE'],
                                          'crs': 3}, method = 'nearest')
                DA = DA0.merge(DA0).sel(indexers = {'day': range_date}, method = 'nearest')
                DA = DA.to_dataframe()
            elif point_date.day_of_year in (doy[-2], doy[-1]):
                DA = DS.sel(indexers = {'lat': point['LATITUDE'],
                                        'lon': point['LONGITUDE'],
                                        'crs': 3}, method = 'nearest')
                DA1 = DS1.sel(indexers = {'lat': point['LATITUDE'],
                                          'lon': point['LONGITUDE'], 
                                          'crs': 3}, method = 'nearest')
                DA = DA.merge(DA1).sel(indexers = {'day': range_date}, method = 'nearest')
                DA = DA.to_dataframe()
            else:
                DA = DS.sel(indexers = {'lat': point['LATITUDE'], 
                                        'lon': point['LONGITUDE'], 
                                        'day': range_date,
                                        'crs': 3}, method = 'nearest')
                DA = DA.to_dataframe()
            
            if col == 'pr':
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['precipitation_amount'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['precipitation_amount'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['precipitation_amount'].max()
            elif (col == 'rmax') or (col == 'rmin'):
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['relative_humidity'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['relative_humidity'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['relative_humidity'].max()
            elif col == 'sph':
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['specific_humidity'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['specific_humidity'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['specific_humidity'].max()
            elif col == 'srad':
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['surface_downwelling_shortwave_flux_in_air'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['surface_downwelling_shortwave_flux_in_air'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['surface_downwelling_shortwave_flux_in_air'].max()
            elif col == 'th':
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['wind_from_direction'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['wind_from_direction'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['wind_from_direction'].max()
            elif (col == 'tmmn') or (col == 'tmmx'):
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['air_temperature'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['air_temperature'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['air_temperature'].max()
            elif col == 'vs':
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['wind_speed'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['wind_speed'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['wind_speed'].max()
            elif col == 'erc':
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['energy_release_component-g'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['energy_release_component-g'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['energy_release_component-g'].max()
            elif col == 'bi':
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['burning_index_g'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['burning_index_g'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['burning_index_g'].max()
            elif col == 'fm100':
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['dead_fuel_moisture_100hr'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['dead_fuel_moisture_100hr'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['dead_fuel_moisture_100hr'].max()
            elif col == 'fm1000':
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['dead_fuel_moisture_1000hr'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['dead_fuel_moisture_1000hr'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['dead_fuel_moisture_1000hr'].max()
            elif col == 'etr':
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['potential_evapotranspiration'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['potential_evapotranspiration'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['potential_evapotranspiration'].max()
            elif col == 'vpd':
                FPA_FOD_climate[col + '_5D_mean'].iloc[i] = DA['mean_vapor_pressure_deficit'].mean()
                FPA_FOD_climate[col + '_5D_min'].iloc[i] = DA['mean_vapor_pressure_deficit'].min()
                FPA_FOD_climate[col + '_5D_max'].iloc[i] = DA['mean_vapor_pressure_deficit'].max()
    FPA_FOD_climate.to_csv(f'Climate_daily/{year}_FPA_FOD_climate.csv', sep = ',', index = False)
    del FPA_FOD_climate

