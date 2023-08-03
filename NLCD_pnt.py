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

year_range = np.array([1992, 2001, 2004, 2006, 2008, 2011, 2013, 2016, 2019])

for year in tqdm(range(start_year, end_year + 1)):
    print(year)
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_NLCD = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_NLCD = FPA_FOD_NLCD.to_crs(crs = 'EPSG:4326')
    FPA_FOD_NLCD['Land_Cover'] = None
    
    year_NLCD = year_range[year_range <= year].max()
    img_file_list = glob.glob(pathname = f'Source_data/NLCD/NLCD_{year_NLCD}.tif')
    NLCD = xr.open_dataset(filename_or_obj = img_file_list[0])

    NLCD = NLCD.sel(indexers={'y': xr.DataArray(FPA_FOD_NLCD['LATITUDE']),
                              'x': xr.DataArray(FPA_FOD_NLCD['LONGITUDE']),
                              'band': 1}, method = 'nearest')
    FPA_FOD_NLCD['Land_Cover'] = NLCD.band_data
    
    del NLCD

    FPA_FOD_NLCD = FPA_FOD_NLCD.drop(labels = 'geometry', axis = 1)
    FPA_FOD_NLCD.to_csv(path_or_buf = f'NLCD/{year}_FPA_FOD_NLCD_pt.csv', sep = ',', index = False)

