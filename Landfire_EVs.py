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
start_year = 2019
end_year = 2020

print('EVC')
for year in tqdm(range(start_year, end_year + 1)):
    if (year > 2000) & (year <= 2011):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_105evc.tif'
    elif (year <= 2012) & (year <= 2013):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_130evc.tif'
    elif (year <= 2014) & (year <= 2015):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_140evc.tif'
    elif (year <= 2016) & (year <= 2019):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/LC16_EVC_200.tif'
    elif (year <= 2020) & (year <= 2021):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/LC22_EVC_220.tif'

    src_ds = gdal.Open(src_filename) 
    gt_forward = src_ds.GetGeoTransform()
    gt_reverse = gdal.InvGeoTransform(gt_forward)
    rb = src_ds.GetRasterBand(1)

    FPA_FOD_file_list = glob.glob(pathname = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_EVC = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0],
                                    latitude = 'LATITUDE',
                                    longitude = 'LONGITUDE').to_crs('EPSG: 5070')
    FPA_FOD_EVC.to_file(filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/EVC_pnt.shp')

    shp_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/EVC_pnt.shp'

    ds = ogr.Open(shp_filename)
    lyr = ds.GetLayer()

    FPA_FOD_EVC['EVC'] = None
    i = 0
    
    for feat in lyr:
        try:
            geom = feat.GetGeometryRef()
            mx, my = geom.GetX(), geom.GetY()  #coord in map units

            #Convert from map to pixel coordinates.
            px, py = gdal.ApplyGeoTransform(gt_reverse, mx, my)
            px = floor(px) #x pixel
            py = floor(py) #y pixel
            
            # To get the Float values, assign buf_type to gdal.GDT_Float32 and in next line unpack it by 'f'
            # for integer value assign buf_type to UInt16 and in next line unpack it by 'h'
            structval = rb.ReadRaster(px, py, 1, 1, buf_type = gdal.GDT_Float32) #it used to be UInt16
            intval = struct.unpack('f' , structval) #use the 'short' format code (2 bytes) not int (4 bytes)
            FPA_FOD_EVC.loc[i, 'EVC'] = intval[0]
            i = i + 1
        except:
            i = i + 1
            pass
    
    FPA_FOD_EVC = FPA_FOD_EVC.drop(labels = 'geometry', axis = 1)
    FPA_FOD_EVC.to_csv(path_or_buf = f'scratch/Summer_2022/EV/{year}_FPA_FOD_EVC_pt.csv', sep = ',', index = False)

print('EVT')
for year in tqdm(range(start_year, end_year + 1)):
    if (year > 2000) & (year <= 2011):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_105evt.tif'
    elif (year <= 2012) & (year <= 2013):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_130evt.tif'
    elif (year <= 2014) & (year <= 2015):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_140evt.tif'
    elif (year <= 2016) & (year <= 2019):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/LC16_EVT_200.tif'
    elif (year <= 2020) & (year <= 2021):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/LC22_EVT_220.tif'

    src_ds = gdal.Open(src_filename) 
    gt_forward = src_ds.GetGeoTransform()
    gt_reverse = gdal.InvGeoTransform(gt_forward)
    rb = src_ds.GetRasterBand(1)

    FPA_FOD_file_list = glob.glob(pathname = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_EVT = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0],
                                    latitude = 'LATITUDE',
                                    longitude = 'LONGITUDE').to_crs('EPSG: 5070')
    FPA_FOD_EVT.to_file(filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/EVT_pnt.shp')

    shp_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/EVT_pnt.shp'

    ds = ogr.Open(shp_filename)
    lyr = ds.GetLayer()

    FPA_FOD_EVT['EVT'] = None
    i = 0
    
    for feat in lyr:
        try:
            geom = feat.GetGeometryRef()
            mx, my = geom.GetX(), geom.GetY()  #coord in map units

            #Convert from map to pixel coordinates.
            px, py = gdal.ApplyGeoTransform(gt_reverse, mx, my)
            px = floor(px) #x pixel
            py = floor(py) #y pixel
            
            # To get the Float values, assign buf_type to gdal.GDT_Float32 and in next line unpack it by 'f'
            # for integer value assign buf_type to UInt16 and in next line unpack it by 'h'
            structval = rb.ReadRaster(px, py, 1, 1, buf_type = gdal.GDT_Float32) #it used to be UInt16
            intval = struct.unpack('f' , structval) #use the 'short' format code (2 bytes) not int (4 bytes)
            FPA_FOD_EVT.loc[i, 'EVT'] = intval[0]
            i = i + 1
        except:
            i = i + 1
            pass
    
    FPA_FOD_EVT = FPA_FOD_EVT.drop(labels = 'geometry', axis = 1)
    FPA_FOD_EVT.to_csv(path_or_buf = f'scratch/Summer_2022/EV/{year}_FPA_FOD_EVT_pt.csv', sep = ',', index = False)

print('EVH')
for year in tqdm(range(start_year, end_year + 1)):
    if (year > 2000) & (year <= 2011):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_105evh.tif'
    elif (year <= 2012) & (year <= 2013):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_130evh.tif'
    elif (year <= 2014) & (year <= 2015):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/us_140evh.tif'
    elif (year <= 2016) & (year <= 2019):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/LC16_EVH_200.tif'
    elif (year <= 2020) & (year <= 2021):
        src_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/LC22_EVH_220.tif'

    src_ds = gdal.Open(src_filename) 
    gt_forward = src_ds.GetGeoTransform()
    gt_reverse = gdal.InvGeoTransform(gt_forward)
    rb = src_ds.GetRasterBand(1)

    FPA_FOD_file_list = glob.glob(pathname = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_EVH = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0],
                                    latitude = 'LATITUDE',
                                    longitude = 'LONGITUDE').to_crs('EPSG: 5070')
    FPA_FOD_EVH.to_file(filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/EVH_pnt.shp')

    shp_filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/LANDFIRE existing vegetation/EVH_pnt.shp'

    ds = ogr.Open(shp_filename)
    lyr = ds.GetLayer()

    FPA_FOD_EVH['EVH'] = None
    i = 0
    
    for feat in lyr:
        try:
            geom = feat.GetGeometryRef()
            mx, my = geom.GetX(), geom.GetY()  #coord in map units

            #Convert from map to pixel coordinates.
            px, py = gdal.ApplyGeoTransform(gt_reverse, mx, my)
            px = floor(px) #x pixel
            py = floor(py) #y pixel
            
            # To get the Float values, assign buf_type to gdal.GDT_Float32 and in next line unpack it by 'f'
            # for integer value assign buf_type to UInt16 and in next line unpack it by 'h'
            structval = rb.ReadRaster(px, py, 1, 1, buf_type = gdal.GDT_Float32) #it used to be UInt16
            intval = struct.unpack('f' , structval) #use the 'short' format code (2 bytes) not int (4 bytes)
            FPA_FOD_EVH.loc[i, 'EVH'] = intval[0]
            i = i + 1
        except:
            i = i + 1
            pass
    
    FPA_FOD_EVH = FPA_FOD_EVH.drop(labels = 'geometry', axis = 1)
    FPA_FOD_EVH.to_csv(path_or_buf = f'scratch/Summer_2022/EV/{year}_FPA_FOD_EVH_pt.csv', sep = ',', index = False)

