import geopandas as gpd
import glob
import geemap
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

print('Loading the road gdb file ...')
road_gpd = gpd.read_file(filename = 'Source_data/Road/tlgdb_2021_a_us_roads.gdb')
road_gpd = road_gpd.to_crs(crs = 'EPSG:4326')
print('Finish loading the road gdb file and start seperating based on the route type.')
road_county = road_gpd[road_gpd['RTTYP'] == 'C']
road_interstate = road_gpd[road_gpd['RTTYP'] == 'I']
road_common_name = road_gpd[road_gpd['RTTYP'] == 'M']
road_other = road_gpd[road_gpd['RTTYP'] == 'O']
road_state = road_gpd[road_gpd['RTTYP'] == 'S']
road_US = road_gpd[road_gpd['RTTYP'] == 'U']
col = ['road_county_dis', 'road_interstate_dis', 'road_common_name_dis', 'road_other_dis', 'road_state_dis', 'road_US_dis']

print('Calculating Distance from roads: ...')
for year in tqdm(range(start_year, end_year + 1)):
    print(str(year) + 'Distance')
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_road = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_road = FPA_FOD_road.to_crs(crs = 'EPSG:4326')
    
    FPA_FOD_road['road_county_dis'] = road_county.distance(other = FPA_FOD_road['geometry'])
    FPA_FOD_road['road_interstate_dis'] = road_interstate.distance(other = FPA_FOD_road['geometry'])
    FPA_FOD_road['road_common_name_dis'] = road_common_name.distance(other = FPA_FOD_road['geometry'])
    FPA_FOD_road['road_other_dis'] = road_other.distance(other = FPA_FOD_road['geometry'])
    FPA_FOD_road['road_state_dis'] = road_state.distance(other = FPA_FOD_road['geometry'])
    FPA_FOD_road['road_US_dis'] = road_US.distance(other = FPA_FOD_road['geometry'])
    
    FPA_FOD_road = FPA_FOD_road.drop(labels = 'geometry', axis = 1)
    FPA_FOD_road.to_csv(path_or_buf = f'Road/{year}_FPA_FOD_Road_dis.csv', sep = ',', index = False)

