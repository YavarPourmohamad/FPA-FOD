#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import geopandas as gpd
import geemap
import glob
from tqdm.auto import tqdm

# start_year = int(input('Select the start year: '))
# end_year = int(input('Select the end year: '))
start_year = 1992
end_year = 2018

road = gpd.read_file(filename = 'Source_data/Road/tlgdb_2021_a_us_roads.gdb').to_crs('EPSG:5070')
road = road[['RTTYP', 'geometry']]
road = road.dissolve(by = 'RTTYP')

year = 1992
# for year in tqdm(range(start_year, end_year + 1)):
FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
FPA_FOD_RDLen = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0],
                                  latitude = 'LATITUDE',
                                  longitude = 'LONGITUDE').to_crs('EPSG:5070')
FPA_FOD_RDLen = FPA_FOD_RDLen.iloc[0:100]

FPA_FOD_RDLen['Road_lenght_1km'] = None

FPA_FOD_RDLen['geometry'] = FPA_FOD_RDLen.buffer(distance = 1000, resolution = 16)

counter = gpd.sjoin(road, FPA_FOD_RDLen, how = "inner", op = 'intersects')

counter.groupby(['index_right']).lenght
