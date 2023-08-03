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

TRI = gdal.DEMProcessing(destName = 'Source_data/DEM/TRI.tif',
                         srcDS = 'Source_data/DEM/LC20_Elev_220.tif',
                         processing = 'TRI')

TRI = gdal.Open('Source_data/DEM/TRI.tif')

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_TRI = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_TRI = FPA_FOD_TRI.to_crs(crs = 'EPSG:5070')
    FPA_FOD_TRI['TRI_1km'] = None
    for i in range(len(FPA_FOD_TRI)):
        if (i % 10000 == 0):
            print(i)
        buffer = FPA_FOD_TRI.iloc[i : i + 1].buffer(distance = 1000, resolution = 6)
        buffer.to_file(filename = 'Source_data/DEM/buffer_TRI.shp', driver = 'ESRI Shapefile')

        buffer_TRI = gdal.Warp(destNameOrDestDS = 'Source_data/DEM/buffer_TRI.tif',
                               srcDSOrSrcDSTab = TRI, 
                               cutlineDSName = 'Source_data/DEM/buffer_TRI.shp',
                               cropToCutline = True, 
                               dstNodata = np.nan)

        FPA_FOD_TRI.loc[i, 'TRI_1km'] = np.nanmean(buffer_TRI.GetRasterBand(1).ReadAsArray())



    FPA_FOD_TRI = FPA_FOD_TRI.drop(labels = 'geometry', axis = 1)
    FPA_FOD_TRI.to_csv(path_or_buf = f'TRI/{year}_FPA_FOD_TRI_bf.csv', sep = ',', index = False)

