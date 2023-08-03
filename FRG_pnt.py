import pandas as pd
import numpy as np
import geopandas as gpd
import xarray as xr
import geemap
import glob
import rioxarray
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

FRG = xr.open_rasterio('Source_data/FRG/us_105frg.tif')

for year in tqdm(range(start_year, end_year + 1)):
    print(year)
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_FRG = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_FRG = FPA_FOD_FRG.to_crs(crs = 'EPSG:5070')
    FPA_FOD_FRG[['FRG', 'x', 'y']] = None
    FPA_FOD_FRG['x'] = FPA_FOD_FRG.geometry.x
    FPA_FOD_FRG['y'] = FPA_FOD_FRG.geometry.y

    FRG_ = FRG.sel(indexers={'y': xr.DataArray(FPA_FOD_FRG['y']),
                              'x': xr.DataArray(FPA_FOD_FRG['x'])}, method = 'nearest')

    FPA_FOD_FRG['FRG'] = FRG_[0].values
    del FRG_

    FPA_FOD_FRG = FPA_FOD_FRG.drop(labels = ['geometry', 'x', 'y'], axis = 1)
    FPA_FOD_FRG.to_csv(path_or_buf = f'FRG/{year}_FPA_FOD_FRG_pt.csv', sep = ',', index = False)

