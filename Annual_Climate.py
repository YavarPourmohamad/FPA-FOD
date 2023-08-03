import pandas as pd
import xarray as xr
import datetime
import calendar
import glob
from tqdm.auto import tqdm

# start_year = int(input('Select the start year: '))
# end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

for year in tqdm(range(start_year, end_year + 1)):
    print(year)
    nc_files = glob.glob(pathname = f'Source_data/GRIDMET/*{year}.nc')

    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_climate = pd.read_csv(FPA_FOD_file_list[0], sep = ',')
    dates = FPA_FOD_climate['DISCOVERY_DATE'].unique()
    for j in nc_files:
        DS = xr.open_dataset(filename_or_obj = j, decode_times = True)
        j = j.split('/')[-1].split('_')[0]
        FPA_FOD_climate[j] = None

        DA = DS.sel(indexers = {'lat': xr.DataArray(FPA_FOD_climate['LATITUDE']),
                                'lon': xr.DataArray(FPA_FOD_climate['LONGITUDE']),
                                'crs': 3}, method = 'nearest')
        DA = DA.to_dataframe()
        if j == 'pr':
            j = 'Annual_precipitation'
            FPA_FOD_climate[j] = DA.groupby(by = 'dim_0', as_index = False)['precipitation_amount'].sum(numeric_only = True).values
            FPA_FOD_climate[j] = FPA_FOD_climate[j].astype('int64')
        elif (j == 'tmmn') or (j == 'tmmx'):
            FPA_FOD_climate[j] = DA.groupby(by = 'dim_0', as_index = False)['air_temperature'].mean(numeric_only = True)
        elif j == 'etr':
            j = 'Annual_etr'
            FPA_FOD_climate[j] = DA.groupby(by = 'dim_0', as_index = False)['potential_evapotranspiration'].sum(numeric_only = True).values
            FPA_FOD_climate[j] = FPA_FOD_climate[j].astype('int64')

    FPA_FOD_climate['Annual_tempreture'] = FPA_FOD_climate[['tmmn', 'tmmx']].mean(axis = 1).round()
    FPA_FOD_climate['Aridity_index'] = (FPA_FOD_climate['Annual_precipitation'] / FPA_FOD_climate['Annual_etr']).round(2)

    FPA_FOD_climate = FPA_FOD_climate.drop(labels = ['tmmn', 'tmmx', 'etr', 'pr', 'fm1000', 'vs', 'fm100', 'vpd',
                                                     'sph', 'rmin', 'rmax', 'bi', 'srad', 'th', 'erc'], axis = 1)
    FPA_FOD_climate.to_csv(path_or_buf = f'Annual_Climate/{year}_FPA_FOD_Ann_clim.csv', sep = ',', index = False)

