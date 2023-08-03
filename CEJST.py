import pandas as pd
import geopandas as gpd
import geemap
import glob
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

CEJST = gpd.read_file(filename = 'Source_data/CEJST/usa.shp')
cols = CEJST.columns[3:]
CEJST = CEJST[cols]

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')

    FPA_FOD_CEJST = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0],
                                      latitude = 'LATITUDE',
                                      longitude = 'LONGITUDE')
    
    FPA_FOD_CEJST = gpd.sjoin(left_df = FPA_FOD_CEJST, right_df = CEJST, how = 'left')
    FPA_FOD_CEJST = FPA_FOD_CEJST.drop(labels = ['geometry', 'index_right'], axis = 1)
    
    FPA_FOD_CEJST.to_csv(path_or_buf = f'CEJST/{year}_FPA_FOD_CEJST.csv', sep = ',', index = False)

