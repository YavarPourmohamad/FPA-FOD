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

Pyromes = gpd.read_file(filename = 'Source_data/Pyromes/Pyromes_CONUS_20200206.shp')
Pyromes = Pyromes.to_crs('EPSG: 4326')
for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_pyro = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    
    FPA_FOD_pyro = FPA_FOD_pyro.sjoin(Pyromes, how = 'left')
    
    FPA_FOD_pyro = FPA_FOD_pyro.drop(labels = ['geometry', 'index_right', 'PYROME'], axis = 1)
    FPA_FOD_pyro.to_csv(path_or_buf = f'Pyromes/{year}_FPA_FOD_Pyromes.csv', sep = ',', index = False)

