import pandas as pd
import xarray as xr
import glob
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

DS = xr.open_dataset(filename_or_obj = 'Source_data/GDP/GDP_per_capita_PPP_1990_2015_v2.nc')

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_GDP = pd.read_csv(filepath_or_buffer = FPA_FOD_file_list[0], sep = ',')
    FPA_FOD_GDP['GDP'] = None
    
    DA = DS.sel(indexers = {'latitude': xr.DataArray(FPA_FOD_GDP['LATITUDE']),
                            'longitude': xr.DataArray(FPA_FOD_GDP['LONGITUDE']),
                            'time': year}, method = 'nearest')
    FPA_FOD_GDP['GDP'] = DA['GDP_per_capita_PPP'].values

    FPA_FOD_GDP.to_csv(path_or_buf = f'GDP/{year}_FPA_FOD_GDP.csv', sep = ',', index = False)

