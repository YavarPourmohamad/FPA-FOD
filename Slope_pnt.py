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

slope = xr.open_rasterio(filename = 'Source_data/DEM/LC20_SlpD_220.tif').drop('band')[0]
slope = slope.rio.reproject('EPSG:4326')

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_elev = pd.read_csv(FPA_FOD_file_list[0])
    FPA_FOD_elev['Slope'] = None


    slope_pnt = slope.sel(indexers={'y': xr.DataArray(FPA_FOD_elev['LATITUDE']),
                                    'x': xr.DataArray(FPA_FOD_elev['LONGITUDE'])}, method = 'nearest')
 
    FPA_FOD_elev['Slope'] = slope_pnt
    del slope_pnt

    FPA_FOD_elev.to_csv(path_or_buf = f'Elevation/{year}_FPA_FOD_slp_pt.csv', sep = ',', index = False)

