import geopandas as gpd
import glob
import geemap
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

for year in tqdm(range(start_year, end_year + 1)):
    print(year)
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_Ecoregions = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0],
                                           latitude = 'LATITUDE',
                                           longitude = 'LONGITUDE')

    Ecoregion_bndr = gpd.read_file(filename = 'Source_data/Ecoregions/us_eco_l4_no_st.shp')[['US_L4CODE', 'US_L3CODE', 'NA_L3CODE', 'NA_L2CODE', 'NA_L1CODE', 'geometry']]
    Ecoregion_bndr = Ecoregion_bndr.to_crs(crs = 'EPSG:4326')

    FPA_FOD_Ecoregions = gpd.sjoin(left_df = FPA_FOD_Ecoregions, 
                                   right_df = Ecoregion_bndr, 
                                   how = 'left')

    FPA_FOD_Ecoregions = FPA_FOD_Ecoregions.drop(labels = ['geometry', 'index_right'], axis = 1)

    col = ['DISCOVERY_DATE', 'NWCG_GENERAL_CAUSE', 'FIRE_SIZE', 'LATITUDE', 'LONGITUDE', 'OWNER_DESCR', 'STATE', 'Year',
           'Ecoregion_US_L4CODE', 'Ecoregion_US_L3CODE', 'Ecoregion_NA_L3CODE', 'Ecoregion_NA_L2CODE', 'Ecoregion_NA_L1CODE']
    FPA_FOD_Ecoregions.columns = col
    FPA_FOD_Ecoregions.to_csv(path_or_buf = f'Ecoregions/{year}_FPA_FOD_Ecoregions.csv', sep = ',', index = False)

