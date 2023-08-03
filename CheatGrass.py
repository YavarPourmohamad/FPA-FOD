import pandas as pd
import xarray as xr
import glob
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

for year in tqdm(range(start_year, end_year + 1)):
    print(year)
    
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_cheat = pd.read_csv(filepath_or_buffer = FPA_FOD_file_list[0], sep = ',')
    FPA_FOD_cheat[['CheatGrass', 'ExoticAnnualGrass', 'Medusahead', 'PoaSecunda']] = None
    
    if year < 2016:
        continue
        
    DS_Cheat = xr.open_dataset(filename_or_obj = f'Source_data/CheatGrass/CheatGrass_{year}_WGS84.tif')
    DA_Cheat = DS_Cheat.sel(indexers = {'x': xr.DataArray(FPA_FOD_cheat['LONGITUDE']),
                                        'y': xr.DataArray(FPA_FOD_cheat['LATITUDE'])},
                            method = 'nearest').to_dataframe()
    del DS_Cheat
    
    DS_Exoti = xr.open_dataset(filename_or_obj = f'Source_data/CheatGrass/ExoticAnnualGrass_{year}_WGS84.tif')
    DA_Exoti = DS_Exoti.sel(indexers = {'x': xr.DataArray(FPA_FOD_cheat['LONGITUDE']),
                                        'y': xr.DataArray(FPA_FOD_cheat['LATITUDE'])},
                            method = 'nearest').to_dataframe()
    del DS_Exoti
    
    DS_Medus = xr.open_dataset(filename_or_obj = f'Source_data/CheatGrass/Medusahead_{year}_WGS84.tif')
    DA_Medus = DS_Medus.sel(indexers = {'x': xr.DataArray(FPA_FOD_cheat['LONGITUDE']),
                                        'y': xr.DataArray(FPA_FOD_cheat['LATITUDE'])},
                            method = 'nearest').to_dataframe()
    del DS_Medus
    
    DS_PoaSe = xr.open_dataset(filename_or_obj = f'Source_data/CheatGrass/PoaSecunda_{year}_WGS84.tif')
    DA_PoaSe = DS_PoaSe.sel(indexers = {'x': xr.DataArray(FPA_FOD_cheat['LONGITUDE']),
                                        'y': xr.DataArray(FPA_FOD_cheat['LATITUDE'])},
                            method = 'nearest').to_dataframe()
    del DS_PoaSe
    
    FPA_FOD_cheat['CheatGrass'] = DA_Cheat['band_data'].values
    FPA_FOD_cheat['ExoticAnnualGrass'] = DA_Exoti['band_data'].values
    FPA_FOD_cheat['Medusahead'] = DA_Medus['band_data'].values
    FPA_FOD_cheat['PoaSecunda'] = DA_PoaSe['band_data'].values
    
    FPA_FOD_cheat.to_csv(path_or_buf = f'CheatGrass/{year}_FPA_FOD_CheatGrass.csv', sep = ',')

