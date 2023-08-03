import pandas as pd
import numpy as np
import geopandas as gpd
import xarray as xr
import geemap
import glob
import rioxarray
from osgeo import gdal, ogr
from tqdm.auto import tqdm
from shapely.geometry import mapping

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

Aspect = gdal.Open('Source_data/DEM/LC20_Asp_220.tif')

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_asp = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_asp = FPA_FOD_asp.to_crs(crs = 'EPSG:5070')
    FPA_FOD_asp['Aspect_1km'] = None

    for i in tqdm(range(len(FPA_FOD_asp))):
        buffer = FPA_FOD_asp.iloc[i : i + 1].buffer(distance = 1000, resolution = 6)
        buffer.to_file(filename = 'Source_data/DEM/buffer_asp.shp', driver = 'ESRI Shapefile')

        buffer_asp = gdal.Warp(destNameOrDestDS = 'Source_data/DEM/buffer_asp.tif',
                               srcDSOrSrcDSTab = Aspect, 
                               cutlineDSName = 'Source_data/DEM/buffer_asp.shp',
                               cropToCutline = True, 
                               dstNodata = np.nan)
        FPA_FOD_asp.loc[i, 'Aspect_1km'] = buffer_asp.GetRasterBand(1).ReadAsArray().mean()
        
    FPA_FOD_asp = FPA_FOD_asp.drop(labels = 'geometry', axis = 1)
    FPA_FOD_asp.to_csv(path_or_buf = f'Elevation/{year}_FPA_FOD_asp_bf.csv', sep = ',', index = False)

