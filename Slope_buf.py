import pandas as pd
import numpy as np
import geopandas as gpd
import xarray as xr
import geemap
import glob
import rioxarray
from osgeo import gdal
from tqdm.auto import tqdm
from shapely.geometry import mapping

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 1992
end_year = 2018

slope = xr.open_rasterio(filename = 'Source_data/DEM/LC20_SlpD_220.tif', masked = True).drop('band')[0]

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_elev = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_elev = FPA_FOD_elev.to_crs(crs = 'EPSG:26910')
    FPA_FOD_elev['Slope_1km'] = None

    buffer = FPA_FOD_elev.buffer(distance = 1000, resolution = 6)
    buffer_crs = buffer.crs
    buffer = buffer.geometry.apply(mapping)

    for i in range(len(FPA_FOD_elev)):
        buffer_slope = slope.rio.clip(buffer[i:i+1], crs = buffer_crs, drop = True, from_disk = True)
        FPA_FOD_elev.loc[i, 'Slope_1km'] = buffer_slope.where(((buffer_eleva != 32767)&(buffer_eleva != -9999.)), other = np.nan).mean().values
        del buffer_slope

    FPA_FOD_elev = FPA_FOD_elev.drop(labels = 'geometry', axis = 1)
    FPA_FOD_elev.to_csv(path_or_buf = f'Elevation/{year}_FPA_FOD_slp_bf.csv', sep = ',', index = False)


# https://www.earthdatascience.org/courses/use-data-open-source-python/intro-raster-data-python/raster-data-processing/crop-raster-data-with-shapefile-in-python/
