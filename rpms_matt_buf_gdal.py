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
start_year = 1992
end_year = 2020

for year in tqdm(range(start_year, end_year + 1)):
    rpms = gdal.Open(f'Source_data/Matt_data/rpms_{year}.tif')
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_rpms = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_rpms = FPA_FOD_rpms.to_crs(crs = 'EPSG:5070')
    FPA_FOD_rpms = FPA_FOD_rpms[['DISCOVERY_DATE', 'NWCG_GENERAL_CAUSE', 'FIRE_SIZE', 'LATITUDE', 'LONGITUDE', 'OWNER_DESCR', 'STATE', 'geometry', 'Year']]
    FPA_FOD_rpms['rpms_1km'] = None

    for i in range(len(FPA_FOD_rpms)):
        buffer = FPA_FOD_rpms.iloc[i : i + 1].buffer(distance = 1000, resolution = 6)
        buffer.to_file(filename = 'Source_data/Matt_data/buffer_rpms.shp', driver = 'ESRI Shapefile')

        buffer_rpms = gdal.Warp(destNameOrDestDS = 'Source_data/Matt_data/buffer_rpms.tif',
                               srcDSOrSrcDSTab = rpms, 
                               cutlineDSName = 'Source_data/Matt_data/buffer_rpms.shp',
                               cropToCutline = True, 
                               dstNodata = np.nan)
        FPA_FOD_rpms.loc[i, 'rpms_1km'] = buffer_rpms.GetRasterBand(1).ReadAsArray().mean()
        
    FPA_FOD_rpms = FPA_FOD_rpms.drop(labels = 'geometry', axis = 1)
    FPA_FOD_rpms.to_csv(path_or_buf = f'rpms/{year}_FPA_FOD_rpms_bf.csv', sep = ',', index = False)

