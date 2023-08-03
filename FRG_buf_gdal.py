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

FRG = gdal.Open('Source_data/FRG/us_105frg.tif')

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_FRG = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_FRG = FPA_FOD_FRG.to_crs(crs = 'EPSG:5070')
    FPA_FOD_FRG['FRG_1km'] = None

    for i in range(len(FPA_FOD_FRG)):
        buffer = FPA_FOD_FRG.iloc[i : i + 1].buffer(distance = 1000, resolution = 6)
        buffer.to_file(filename = 'Source_data/FRG/buffer.shp', driver = 'ESRI Shapefile')

        buffer_FRG = gdal.Warp(destNameOrDestDS = 'Source_data/FRG/buffer.tif',
                               srcDSOrSrcDSTab = FRG, 
                               cutlineDSName = 'Source_data/FRG/buffer.shp',
                               cropToCutline = True, 
                               dstNodata = np.nan)
        buffer_FRG = buffer_FRG.GetRasterBand(1).ReadAsArray().flatten()
        buffer_FRG = np.delete(buffer_FRG, np.where(buffer_FRG == 0))
        buffer_FRG = pd.DataFrame(buffer_FRG).value_counts()

        if buffer_FRG.shape[0] == 0:
            continue
        elif buffer_FRG.shape[0] == 1:
            buffer_FRG = f"{buffer_FRG.index[0][0]}({int(round(buffer_FRG.iloc[0] / sum(buffer_FRG) * 100, ndigits = 0))}%)"
        elif buffer_FRG.shape[0] == 2:
            buffer_FRG = f"{buffer_FRG.index[0][0]}({int(round(buffer_FRG.iloc[0] / sum(buffer_FRG) * 100, ndigits = 0))}%) / {buffer_FRG.index[1][0]}({int(round(buffer_FRG.iloc[1] / sum(buffer_FRG) * 100, ndigits = 0))}%)"
        else:
            buffer_FRG = f"{buffer_FRG.index[0][0]}({int(round(buffer_FRG.iloc[0] / sum(buffer_FRG) * 100, ndigits = 0))}%) / {buffer_FRG.index[1][0]}({int(round(buffer_FRG.iloc[1] / sum(buffer_FRG) * 100, ndigits = 0))}%) / {buffer_FRG.index[2][0]}({int(round(buffer_FRG.iloc[2] / sum(buffer_FRG) * 100, ndigits = 0))}%)"

        FPA_FOD_FRG.loc[i, 'FRG_1km'] = buffer_FRG

    FPA_FOD_FRG = FPA_FOD_FRG.drop(labels = 'geometry', axis = 1)
    FPA_FOD_FRG.to_csv(path_or_buf = f'FRG/{year}_FPA_FOD_FRG_bf.csv', sep = ',', index = False)

