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
end_year = 2000

src_filename = 'Source_data/NLCD/NLCD_1992.tif'
for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    geemap.csv_to_shp(in_csv = FPA_FOD_file_list[0],
                      latitude = 'LATITUDE',
                      longitude = 'LONGITUDE',
                      out_shp = 'Source_data/NLCD/NLCD_pnt.shp')
    FPA_FOD_NLCD = pd.read_csv(filepath_or_buffer = FPA_FOD_file_list[0], sep = ',')

    shp_filename = 'Source_data/NLCD/NLCD_pnt.shp'

    src_ds = gdal.Open(src_filename) 
    gt_forward = src_ds.GetGeoTransform()
    gt_reverse = gdal.InvGeoTransform(gt_forward)
    rb = src_ds.GetRasterBand(1)

    ds = ogr.Open(shp_filename)
    lyr = ds.GetLayer()

    FPA_FOD_NLCD['Land_Cover'] = None
    i = 0
    
    for feat in lyr:
        try:
            geom = feat.GetGeometryRef()
            mx, my = geom.GetX(), geom.GetY()  #coord in map units

            #Convert from map to pixel coordinates.
            px, py = gdal.ApplyGeoTransform(gt_reverse, mx, my)
            px = floor(px) #x pixel
            py = floor(py) #y pixel

            structval = rb.ReadRaster(px, py, 1, 1, buf_type = gdal.GDT_UInt16) #Assumes 16 bit int aka 'short'
            intval = struct.unpack('h' , structval) #use the 'short' format code (2 bytes) not int (4 bytes)
            FPA_FOD_NLCD.loc[i, 'Land_cover'] = intval[0]
            i = i + 1
        except:
            i = i + 1
            pass
    FPA_FOD_NLCD.to_csv(path_or_buf = f'NLCD/{year}_FPA_FOD_NLCD_pt.csv', sep = ',', index = False)

