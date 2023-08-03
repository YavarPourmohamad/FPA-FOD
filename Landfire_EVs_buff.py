import numpy as np
import pandas as pd
import glob
import geemap
import struct
from math import floor
from osgeo import gdal,ogr
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 1992
end_year = 2020

print('EVC')
for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_EVC = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_EVC = FPA_FOD_EVC.to_crs(crs = 'EPSG:5070')
    FPA_FOD_EVC['EVC_1km'] = None

    if (year > 2000) & (year <= 2011):
        EVC = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_105evc.tif')
    elif (year <= 2012) & (year <= 2013):
        EVC = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_130evc.tif')
    elif (year <= 2014) & (year <= 2015):
        EVC = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_140evc.tif')
    elif (year <= 2016) & (year <= 2019):
        EVC = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/LC16_EVC_200.tif')
    elif (year <= 2020) & (year <= 2021):
        EVC = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/LC22_EVC_220.tif')
    
    for i in range(len(FPA_FOD_EVC)):
        buffer = FPA_FOD_EVC.iloc[i : i + 1].buffer(distance = 1000, resolution = 6).to_crs('EPSG:4326')
        buffer.to_file(filename = 'Source_data/LANDFIRE existing vegetation/buffer.shp', driver = 'ESRI Shapefile')

        buffer_EVC = gdal.Warp(destNameOrDestDS = 'Source_data/LANDFIRE existing vegetation/buffer.tif',
                               srcDSOrSrcDSTab = EVC, 
                               cutlineDSName = 'Source_data/LANDFIRE existing vegetation/buffer.shp',
                               cropToCutline = True, 
                               dstNodata = np.nan)
        buffer_EVC = buffer_EVC.GetRasterBand(1).ReadAsArray().flatten()
        buffer_EVC = np.delete(buffer_EVC, np.where(buffer_EVC == 0))
        buffer_EVC = pd.DataFrame(buffer_EVC).value_counts()
        
        if buffer_EVC.shape[0] == 0:
            continue
        if buffer_EVC.shape[0] == 1:
            buffer_EVC = f"{buffer_EVC.index[0][0]}({int(round(buffer_EVC.iloc[0] / sum(buffer_EVC) * 100, ndigits = 0))}%)"
        elif buffer_EVC.shape[0] == 2:
            buffer_EVC = f"{buffer_EVC.index[0][0]}({int(round(buffer_EVC.iloc[0] / sum(buffer_EVC) * 100, ndigits = 0))}%) / {buffer_EVC.index[1][0]}({int(round(buffer_EVC.iloc[1] / sum(buffer_EVC) * 100, ndigits = 0))}%)"
        else:
            buffer_EVC = f"{buffer_EVC.index[0][0]}({int(round(buffer_EVC.iloc[0] / sum(buffer_EVC) * 100, ndigits = 0))}%) / {buffer_EVC.index[1][0]}({int(round(buffer_EVC.iloc[1] / sum(buffer_EVC) * 100, ndigits = 0))}%) / {buffer_EVC.index[2][0]}({int(round(buffer_EVC.iloc[2] / sum(buffer_EVC) * 100, ndigits = 0))}%)"

        FPA_FOD_EVC.loc[i, 'EVC_1km'] = buffer_EVC

        
    FPA_FOD_EVC = FPA_FOD_EVC.drop(labels = 'geometry', axis = 1)
    FPA_FOD_EVC.to_csv(path_or_buf = f'EV/{year}_FPA_FOD_EVC_bf.csv', sep = ',', index = False)

print('EVH')
for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_EVH = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_EVH = FPA_FOD_EVH.to_crs(crs = 'EPSG:5070')
    FPA_FOD_EVH['EVH_1km'] = None
    
    if (year > 2000) & (year <= 2011):
        EVH = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_105evh.tif')
    elif (year <= 2012) & (year <= 2013):
        EVH = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_130evh.tif')
    elif (year <= 2014) & (year <= 2015):
        EVH = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_140evh.tif')
    elif (year <= 2016) & (year <= 2019):
        EVH = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/LC16_EVH_200.tif')
    elif (year <= 2020) & (year <= 2021):
        EVH = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/LC22_EVH_220.tif')

    for i in range(len(FPA_FOD_EVH)):
        buffer = FPA_FOD_EVH.iloc[i : i + 1].buffer(distance = 1000, resolution = 6).to_crs('EPSG:4326')
        buffer.to_file(filename = 'Source_data/LANDFIRE existing vegetation/buffer.shp', driver = 'ESRI Shapefile')

        buffer_EVH = gdal.Warp(destNameOrDestDS = 'Source_data/LANDFIRE existing vegetation/buffer.tif',
                               srcDSOrSrcDSTab = EVH, 
                               cutlineDSName = 'Source_data/LANDFIRE existing vegetation/buffer.shp',
                               cropToCutline = True, 
                               dstNodata = np.nan)
        buffer_EVH = buffer_EVH.GetRasterBand(1).ReadAsArray().flatten()
        buffer_EVH = np.delete(buffer_EVH, np.where(buffer_EVH == 0))
        buffer_EVH = pd.DataFrame(buffer_EVH).value_counts()
        
        if buffer_EVH.shape[0] == 0:
            continue
        if buffer_EVH.shape[0] == 1:
            buffer_EVH = f"{buffer_EVH.index[0][0]}({int(round(buffer_EVH.iloc[0] / sum(buffer_EVH) * 100, ndigits = 0))}%)"
        elif buffer_EVH.shape[0] == 2:
            buffer_EVH = f"{buffer_EVH.index[0][0]}({int(round(buffer_EVH.iloc[0] / sum(buffer_EVH) * 100, ndigits = 0))}%) / {buffer_EVH.index[1][0]}({int(round(buffer_EVH.iloc[1] / sum(buffer_EVH) * 100, ndigits = 0))}%)"
        else:
            buffer_EVH = f"{buffer_EVH.index[0][0]}({int(round(buffer_EVH.iloc[0] / sum(buffer_EVH) * 100, ndigits = 0))}%) / {buffer_EVH.index[1][0]}({int(round(buffer_EVH.iloc[1] / sum(buffer_EVH) * 100, ndigits = 0))}%) / {buffer_EVH.index[2][0]}({int(round(buffer_EVH.iloc[2] / sum(buffer_EVH) * 100, ndigits = 0))}%)"

        FPA_FOD_EVH.loc[i, 'EVH_1km'] = buffer_EVH

        
    FPA_FOD_EVH = FPA_FOD_EVH.drop(labels = 'geometry', axis = 1)
    FPA_FOD_EVH.to_csv(path_or_buf = f'EV/{year}_FPA_FOD_EVH_bf.csv', sep = ',', index = False)

print('EVT')
for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_EVT = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_EVT = FPA_FOD_EVT.to_crs(crs = 'EPSG:5070')
    FPA_FOD_EVT['EVT_1km'] = None

    if (year > 2000) & (year <= 2011):
        EVT = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_105evt.tif')
    elif (year <= 2012) & (year <= 2013):
        EVT = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_130evt.tif')
    elif (year <= 2014) & (year <= 2015):
        EVT = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_140evt.tif')
    elif (year <= 2016) & (year <= 2019):
        EVT = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/LC16_EVT_200.tif')
    elif (year <= 2020) & (year <= 2021):
        EVT = gdal.Open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/LC22_EVT_220.tif')

    for i in range(len(FPA_FOD_EVT)):
        buffer = FPA_FOD_EVT.iloc[i : i + 1].buffer(distance = 1000, resolution = 6).to_crs('EPSG:4326')
        buffer.to_file(filename = 'Source_data/LANDFIRE existing vegetation/buffer.shp', driver = 'ESRI Shapefile')

        buffer_EVT = gdal.Warp(destNameOrDestDS = 'Source_data/LANDFIRE existing vegetation/buffer.tif',
                                srcDSOrSrcDSTab = EVT, 
                                cutlineDSName = 'Source_data/LANDFIRE existing vegetation/buffer.shp',
                                cropToCutline = True,
                                dstNodata = np.nan)
        
        buffer_EVT = buffer_EVT.GetRasterBand(1).ReadAsArray().flatten()
        buffer_EVT = np.delete(buffer_EVT, np.where(buffer_EVT == 0))
        buffer_EVT = pd.DataFrame(buffer_EVT).value_counts()
        
        if buffer_EVT.shape[0] == 0:
            continue
        if buffer_EVT.shape[0] == 1:
            buffer_EVT = f"{buffer_EVT.index[0][0]}({int(round(buffer_EVT.iloc[0] / sum(buffer_EVT) * 100, ndigits = 0))}%)"
        elif buffer_EVT.shape[0] == 2:
            buffer_EVT = f"{buffer_EVT.index[0][0]}({int(round(buffer_EVT.iloc[0] / sum(buffer_EVT) * 100, ndigits = 0))}%) / {buffer_EVT.index[1][0]}({int(round(buffer_EVT.iloc[1] / sum(buffer_EVT) * 100, ndigits = 0))}%)"
        else:
            buffer_EVT = f"{buffer_EVT.index[0][0]}({int(round(buffer_EVT.iloc[0] / sum(buffer_EVT) * 100, ndigits = 0))}%) / {buffer_EVT.index[1][0]}({int(round(buffer_EVT.iloc[1] / sum(buffer_EVT) * 100, ndigits = 0))}%) / {buffer_EVT.index[2][0]}({int(round(buffer_EVT.iloc[2] / sum(buffer_EVT) * 100, ndigits = 0))}%)"

        FPA_FOD_EVT.loc[i, 'EVT_1km'] = buffer_EVT
        
    FPA_FOD_EVT = FPA_FOD_EVT.drop(labels = 'geometry', axis = 1)
    FPA_FOD_EVT.to_csv(path_or_buf = f'EV/{year}_FPA_FOD_EVT_bf.csv', sep = ',', index = False)

