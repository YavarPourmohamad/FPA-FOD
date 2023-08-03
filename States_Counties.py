import geopandas as gpd
import glob
import geemap
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 1992
end_year = 2020

States = gpd.read_file(filename = 'Source_data/States_County/cb_2018_us_state_500k/cb_2018_us_state_500k.shp')
States = States.to_crs(crs = 'EPSG:4326')
States = States[['NAME', 'geometry']]

Counties = gpd.read_file(filename = 'Source_data/States_County/cb_2018_us_county_500k/cb_2018_us_county_500k.shp')
Counties = Counties.to_crs(crs = 'EPSG:4326')
Counties = Counties[['NAME', 'geometry']]

for year in tqdm(range(start_year, end_year + 1)):
    print(year)
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_States = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0],
                                           latitude = 'LATITUDE',
                                           longitude = 'LONGITUDE')
    FPA_FOD_States = gpd.sjoin(left_df = FPA_FOD_States,
                               right_df = States,
                               how = 'left')
    FPA_FOD_States = FPA_FOD_States.drop(labels = ['geometry', 'index_right'], axis = 1)
    FPA_FOD_States = FPA_FOD_States.rename(columns = {'NAME':'LatLong_State'})

    FPA_FOD_States = gpd.GeoDataFrame(data = FPA_FOD_States, crs = 'EPSG:4326',
                                      geometry = gpd.points_from_xy(x = FPA_FOD_States.LONGITUDE,
                                                                    y = FPA_FOD_States.LATITUDE))
    FPA_FOD_County = gpd.sjoin(left_df = FPA_FOD_States,
                               right_df = Counties,
                               how = 'left')
    FPA_FOD_County = FPA_FOD_County.drop(labels = ['geometry', 'index_right'], axis = 1)
    FPA_FOD_County = FPA_FOD_County.rename(columns = {'NAME':'LatLong_County'})

    col = ['DISCOVERY_DATE', 'NWCG_GENERAL_CAUSE', 'FIRE_SIZE', 'LATITUDE', 'LONGITUDE', 'OWNER_DESCR', 'STATE', 'Year',
           'LatLong_State', 'LatLong_County']
    FPA_FOD_County = FPA_FOD_County[col]
    FPA_FOD_County.to_csv(path_or_buf = f'States_Counties/{year}_FPA_FOD_States_Counties.csv', sep = ',', index = False)