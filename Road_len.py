import geopandas as gpd
import glob
import geemap
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 1992
end_year = 2018

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
  
print('Loop starts:')
for year in tqdm(range(start_year, end_year + 1)):
    print(str(year) + 'lenght' + '1000m')
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_road = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0], latitude = 'LATITUDE', longitude = 'LONGITUDE')
    FPA_FOD_road = FPA_FOD_road.to_crs(crs = 'EPSG:4326')
    
    buffer = 1000
    col = ['road_county_len_1km', 'road_interstate_len_1km', 'road_common_name_len_1km', 'road_other_len_1km', 
           'road_state_len_1km', 'road_US_len_1km']
    FPA_FOD_road[col] = None
    buffer = FPA_FOD_road.buffer(distance = buffer)
    
    for i in tqdm(range(len(FPA_FOD_road))):
        point = FPA_FOD_road.iloc[i]
        point_buffer = buffer.iloc[i]
        intersected_county = road_county.intersection(other = point_buffer)
        intersected_interstate = road_interstate.intersection(other = point_buffer)
        intersected_common_name = road_common_name.intersection(other = point_buffer)
        intersected_other = road_other.intersection(other = point_buffer)
        intersected_state = road_state.intersection(other = point_buffer)
        intersected_US = road_US.intersection(other = point_buffer)
        
        FPA_FOD_road.loc[i, 'road_county_len_1km'] = sum(intersected_county.length)
        FPA_FOD_road.loc[i, 'road_interstate_len_1km'] = sum(intersected_interstate.length)
        FPA_FOD_road.loc[i, 'road_common_name_len_1km'] = sum(intersected_common_name.length)
        FPA_FOD_road.loc[i, 'road_other_len_1km'] = sum(intersected_other.length)
        FPA_FOD_road.loc[i, 'road_state_len_1km'] = sum(intersected_state.length)
        FPA_FOD_road.loc[i, 'road_US_len_1km'] = sum(intersected_US.length)
    
    print(str(year) + 'lenght' + '5000m')
    buffer = 5000
    col = ['road_county_len_5km', 'road_interstate_len_5km', 'road_common_name_len_5km', 'road_other_len_5km', 
           'road_state_len_5km', 'road_US_len_5km']
    FPA_FOD_road[col] = None
    buffer = FPA_FOD_road.buffer(distance = buffer)
    
    for i in tqdm(range(len(FPA_FOD_road))):
        point = FPA_FOD_road.iloc[i]
        point_buffer = buffer.iloc[i]
        intersected_county = road_county.intersection(other = point_buffer)
        intersected_interstate = road_interstate.intersection(other = point_buffer)
        intersected_common_name = road_common_name.intersection(other = point_buffer)
        intersected_other = road_other.intersection(other = point_buffer)
        intersected_state = road_state.intersection(other = point_buffer)
        intersected_US = road_US.intersection(other = point_buffer)

        FPA_FOD_road.loc[i, 'road_county_len_5km'] = sum(intersected_county.length)
        FPA_FOD_road.loc[i, 'road_interstate_len_5km'] = sum(intersected_interstate.length)
        FPA_FOD_road.loc[i, 'road_common_name_len_5km'] = sum(intersected_common_name.length)
        FPA_FOD_road.loc[i, 'road_other_len_5km'] = sum(intersected_other.length)
        FPA_FOD_road.loc[i, 'road_state_len_5km'] = sum(intersected_state.length)
        FPA_FOD_road.loc[i, 'road_US_len_5km'] = sum(intersected_US.length)
        
    FPA_FOD_road = FPA_FOD_road.drop(labels = 'geometry', axis = 1)
    FPA_FOD_road.to_csv(path_or_buf = f'Road/{year}_FPA_FOD_Road_len.csv', sep = ',', index = False)

