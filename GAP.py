import geopandas as gpd
import pandas as ps
import geemap
import glob
from tqdm.auto import tqdm
from osgeo import gdal, ogr

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

GAP = gpd.read_file(filename = 'Source_data/GAP/PADUS3_0VectorAnalysis_Simp_SingP_StateUni_ClipCensus_CONUS_Diss.shp')

for year in tqdm(range(start_year, end_year + 1)):
    print(year)
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_GAP = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    
    FPA_FOD_GAP = FPA_FOD_GAP.sjoin(GAP, how = 'left')
    
    FPA_FOD_GAP = FPA_FOD_GAP.drop(labels = ['geometry', 'index_right', 'OBJECTID', 'Pub_Access', 'STUSPS', 'NAME',
                                             'MngTp_Desc', 'MngNm_Desc', 'ST_Name', 'SUM_GIS_Ac', 'Shape_Leng',
                                             'Shape_Area', 'JnID', 'RastDrop', 'GIS_Acres'], axis = 1)
    FPA_FOD_GAP.to_csv(path_or_buf = f'GAP/{year}_FPA_FOD_GAP.csv', sep = ',', index = False)

