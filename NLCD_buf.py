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

year_range = np.array([1992, 2001, 2004, 2006, 2008, 2011, 2013, 2016, 2019])

for year in tqdm(range(start_year, end_year + 1)):
    print(year)
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_NLCD = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_NLCD = FPA_FOD_NLCD.to_crs(crs = 'EPSG:5070')
    FPA_FOD_NLCD['Land_Cover_1km'] = None

    year_NLCD = year_range[year_range <= year].max()
    NLCD = gdal.Open(f'Source_data/NLCD/NLCD_{year_NLCD}.tif')

    for i in range(len(FPA_FOD_NLCD)):
        buffer = FPA_FOD_NLCD.iloc[i : i + 1].buffer(distance = 1000, resolution = 6).to_crs('EPSG:4326')
        buffer.to_file(filename = 'Source_data/NLCD/buffer.shp', driver = 'ESRI Shapefile')

        buffer_NLCD = gdal.Warp(destNameOrDestDS = 'Source_data/NLCD/buffer.tif',
                                srcDSOrSrcDSTab = NLCD, 
                                cutlineDSName = 'Source_data/NLCD/buffer.shp',
                                cropToCutline = True,
                                dstNodata = np.nan)
        
        buffer_NLCD = buffer_NLCD.GetRasterBand(1).ReadAsArray().flatten()
        buffer_NLCD = np.delete(buffer_NLCD, np.where(buffer_NLCD == 0))
        buffer_NLCD = pd.DataFrame(buffer_NLCD).value_counts()
        
        if buffer_NLCD.shape[0] == 0:
            continue
        if buffer_NLCD.shape[0] == 1:
            buffer_NLCD = f"{buffer_NLCD.index[0][0]}({int(round(buffer_NLCD.iloc[0] / sum(buffer_NLCD) * 100, ndigits = 0))}%)"
        elif buffer_NLCD.shape[0] == 2:
            buffer_NLCD = f"{buffer_NLCD.index[0][0]}({int(round(buffer_NLCD.iloc[0] / sum(buffer_NLCD) * 100, ndigits = 0))}%) / {buffer_NLCD.index[1][0]}({int(round(buffer_NLCD.iloc[1] / sum(buffer_NLCD) * 100, ndigits = 0))}%)"
        else:
            buffer_NLCD = f"{buffer_NLCD.index[0][0]}({int(round(buffer_NLCD.iloc[0] / sum(buffer_NLCD) * 100, ndigits = 0))}%) / {buffer_NLCD.index[1][0]}({int(round(buffer_NLCD.iloc[1] / sum(buffer_NLCD) * 100, ndigits = 0))}%) / {buffer_NLCD.index[2][0]}({int(round(buffer_NLCD.iloc[2] / sum(buffer_NLCD) * 100, ndigits = 0))}%)"

        FPA_FOD_NLCD.loc[i, 'Land_Cover_1km'] = buffer_NLCD
        
    FPA_FOD_NLCD = FPA_FOD_NLCD.drop(labels = 'geometry', axis = 1)
    FPA_FOD_NLCD.to_csv(path_or_buf = f'NLCD/{year}_FPA_FOD_NLCD_bf.csv', sep = ',', index = False)

