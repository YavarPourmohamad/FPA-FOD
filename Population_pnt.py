import pandas as pd
import numpy as np
import geopandas as gpd
import xarray as xr
import geemap
import glob
import rioxarray
from osgeo import gdal
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_pop = pd.read_csv(FPA_FOD_file_list[0])
    FPA_FOD_pop['Population'] = None
    
    if year < 2000:
        FPA_FOD_pop.to_csv(path_or_buf = f'Population/{year}_FPA_FOD_pop_pt.csv', sep = ',', index = False)
        continue
        
    population = xr.open_rasterio(filename = f'Source_data/Pop/usa_ppp_{year}_UNadj.tif').drop('band')[0]
#     population = population.rio.reproject('EPSG:4326')
#     population = population.where(population > -99999.0 + 1, np.nan)

    population_pnt = population.sel(indexers={'y': xr.DataArray(FPA_FOD_pop['LATITUDE']),
                                              'x': xr.DataArray(FPA_FOD_pop['LONGITUDE'])}, method = 'nearest')
    FPA_FOD_pop['Population'] = population_pnt
    del population

    FPA_FOD_pop.to_csv(path_or_buf = f'Population/{year}_FPA_FOD_pop_pt.csv', sep = ',', index = False)

