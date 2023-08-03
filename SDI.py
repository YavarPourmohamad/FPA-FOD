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

src_filename = 'Source_data/SDI/CONUS_2022_90_SDI.tif'
src_ds = gdal.Open(src_filename) 
gt_forward = src_ds.GetGeoTransform()
gt_reverse = gdal.InvGeoTransform(gt_forward)
rb = src_ds.GetRasterBand(1)

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_SDI = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0],
                                    latitude = 'LATITUDE',
                                    longitude = 'LONGITUDE').to_crs('EPSG: 5070')
    FPA_FOD_SDI.to_file(filename = 'Source_data/SDI/SDI_pnt.shp')

    shp_filename = 'Source_data/SDI/SDI_pnt.shp'

    ds = ogr.Open(shp_filename)
    lyr = ds.GetLayer()

    FPA_FOD_SDI['SDI'] = None
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
            FPA_FOD_SDI.loc[i, 'SDI'] = intval[0]
            i = i + 1
        except:
            i = i + 1
            pass
    
    FPA_FOD_SDI = FPA_FOD_SDI.drop(labels = 'geometry', axis = 1)
    FPA_FOD_SDI['SDI'] = FPA_FOD_SDI['SDI'] / 100
    FPA_FOD_SDI.to_csv(path_or_buf = f'SDI/{year}_FPA_FOD_SDI.csv', sep = ',', index = False)

