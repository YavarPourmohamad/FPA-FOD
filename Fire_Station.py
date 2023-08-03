import numpy as np
import geopandas as gpd
import geemap
import glob
from tqdm.auto import tqdm

# start_year = int(input('Select the start year: '))
# end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

FS = gpd.read_file(filename = 'Source_data/Fire_Station/Fire_Stations.shp').to_crs('EPSG:5070')
buffer = [1000, 5000, 10000, 20000]

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_FS = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0],
                                   latitude = 'LATITUDE',
                                   longitude = 'LONGITUDE').to_crs('EPSG:5070')
    for buf in buffer:
        FPA_FOD_FS[f'No_FireStation_{buf/1000}km'] = None

        FPA_FOD_FS['geometry'] = FPA_FOD_FS.buffer(distance = buf, resolution = 16)

        counter = gpd.sjoin(FS, FPA_FOD_FS, how = "inner", op = 'intersects')
        counter['const'] = 1
        FPA_FOD_FS[f'No_FireStation_{buf/1000}km'] = counter.groupby(['index_right']).sum()['const']

    FPA_FOD_FS = FPA_FOD_FS.drop(labels = 'geometry', axis = 1)
    FPA_FOD_FS.to_csv(path_or_buf = f'FS/{year}_FPA_FOD_FS.csv', sep = ',', index = False)

