import pandas as pd
import geopandas as gpd
import glob
from tqdm.auto import tqdm

# start_year = int(input('Select the start year: '))
# end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

Evac = gpd.read_file(filename = 'Source_data/Evac/WFDSS_EstimatedGroundEvacTime.shp').to_crs('EPSG:4326')

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_Evac = pd.read_csv(filepath_or_buffer = FPA_FOD_file_list[0], sep = ',')
    FPA_FOD_Evac = gpd.GeoDataFrame(data = FPA_FOD_Evac,
                                    crs = 'EPSG:4326',
                                    geometry = gpd.points_from_xy(x = FPA_FOD_Evac['LONGITUDE'],
                                                                  y = FPA_FOD_Evac['LATITUDE']))
    FPA_FOD_Evac['Evacuation'] = None
    FPA_FOD_Evac['Evacuation'] = gpd.sjoin(left_df = FPA_FOD_Evac,
                                           right_df = Evac,
                                           how = 'left')['grid_code']
    
    FPA_FOD_Evac = FPA_FOD_Evac.drop(labels = 'geometry', axis = 1)
    FPA_FOD_Evac.to_csv(path_or_buf = f'Evac/{year}_FPA_FOD_Evac.csv', sep = ',', index = False)

