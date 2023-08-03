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

Elevation = gdal.Open('Source_data/DEM/LC20_Elev_220.tif')

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_elev = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_elev = FPA_FOD_elev.to_crs(crs = 'EPSG:5070')
    FPA_FOD_elev['Elevation_1km'] = None

    for i in range(len(FPA_FOD_elev)):
        buffer = FPA_FOD_elev.iloc[i : i + 1].buffer(distance = 1000, resolution = 6)
        buffer.to_file(filename = 'Source_data/DEM/buffer_ele.shp', driver = 'ESRI Shapefile')

        buffer_ele = gdal.Warp(destNameOrDestDS = 'Source_data/DEM/buffer_ele.tif',
                               srcDSOrSrcDSTab = Elevation, 
                               cutlineDSName = 'Source_data/DEM/buffer_ele.shp',
                               cropToCutline = True, 
                               dstNodata = np.nan)
        FPA_FOD_elev.loc[i, 'Elevation_1km'] = buffer_ele.GetRasterBand(1).ReadAsArray().mean()
        
    FPA_FOD_elev = FPA_FOD_elev.drop(labels = 'geometry', axis = 1)
    FPA_FOD_elev.to_csv(path_or_buf = f'Elevation/{year}_FPA_FOD_elev_bf.csv', sep = ',', index = False)

