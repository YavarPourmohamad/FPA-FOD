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

# TPI = gdal.DEMProcessing(destName = 'Source_data/DEM/TPI.tif',
#                          srcDS = 'Source_data/DEM/LC20_Elev_220.tif',
#                          processing = 'TPI')

TPI = gdal.Open('Source_data/DEM/TPI.tif')

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_TPI = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_TPI = FPA_FOD_TPI.to_crs(crs = 'EPSG:5070')
    FPA_FOD_TPI['TPI_1km'] = None
    for i in range(len(FPA_FOD_TPI)):
        buffer = FPA_FOD_TPI.iloc[i : i + 1].buffer(distance = 1000, resolution = 6)
        buffer.to_file(filename = 'Source_data/DEM/buffer.shp', driver = 'ESRI Shapefile')

        buffer_TPI = gdal.Warp(destNameOrDestDS = 'Source_data/DEM/buffer.tif',
                               srcDSOrSrcDSTab = TPI, 
                               cutlineDSName = 'Source_data/DEM/buffer.shp',
                               cropToCutline = True, 
                               dstNodata = np.nan)

        FPA_FOD_TPI.loc[i, 'TPI_1km'] = np.nanmean(buffer_TPI.GetRasterBand(1).ReadAsArray())

    FPA_FOD_TPI = FPA_FOD_TPI.drop(labels = 'geometry', axis = 1)
    FPA_FOD_TPI.to_csv(path_or_buf = f'TPI/{year}_FPA_FOD_TPI_bf.csv', sep = ',', index = False)

