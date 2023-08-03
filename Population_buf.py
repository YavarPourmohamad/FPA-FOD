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

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_pop = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_pop = FPA_FOD_pop.to_crs(crs = 'EPSG:5070')
    FPA_FOD_pop['Popo_1km'] = None
    
    
    if year < 2000:
        FPA_FOD_pop.to_csv(path_or_buf = f'Population/{year}_FPA_FOD_pop_bf.csv', sep = ',', index = False)
        continue
    
    population = gdal.Open(f'Source_data/Pop/usa_ppp_{year}_UNadj.tif')

    for i in tqdm(range(len(FPA_FOD_pop))):
        buffer = FPA_FOD_pop.iloc[i : i + 1].buffer(distance = 1000, resolution = 6).to_crs('EPSG:4326')
        buffer.to_file(filename = 'Source_data/Pop/buffer.shp', driver = 'ESRI Shapefile')

        buffer_pop = gdal.Warp(destNameOrDestDS = 'Source_data/Pop/buffer.tif',
                               srcDSOrSrcDSTab = population, 
                               cutlineDSName = 'Source_data/Pop/buffer.shp',
                               cropToCutline = True, 
                               dstNodata = np.nan)
        FPA_FOD_pop.loc[i, 'Popo_1km'] = np.nanmean(buffer_pop.GetRasterBand(1).ReadAsArray())
        
    FPA_FOD_pop = FPA_FOD_pop.drop(labels = 'geometry', axis = 1)
    FPA_FOD_pop.to_csv(path_or_buf = f'Population/{year}_FPA_FOD_pop_bf.csv', sep = ',', index = False)

