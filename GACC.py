import pandas as pd
import geopandas as gpd
import glob
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

GACC_shts = ['AICC', 'GBCC', 'EACC', 'NRCC', 'NWCC', 'ONCC', 'OSCC', 'RMCC', 'SACC', 'SWCC']
GACC_data = pd.read_excel(io = 'Source_data/GACC/2007-2021 PLs by Erin.xlsx', 
                          sheet_name = GACC_shts)

GACC_bndr = gpd.read_file(filename = 'Source_data/GACC/National_GACC_Current.shp')[['GACCAbbrev', 'geometry']]

GACC = gpd.GeoDataFrame()

for i in GACC_shts:
    GACC_data[i]['GACCAbbrev'] = i
    temp = pd.merge(GACC_bndr, GACC_data[i], on = 'GACCAbbrev')
    GACC = pd.concat([GACC, temp])

GACC.columns = ['GACCAbbrev', 'geometry', 'Date', 'GACC_PL', 'GACC_New fire', 'GACC_New LF', 'GACC_Uncont LF',
                'GACC_Type 1 IMTs', 'GACC_Type 2 IMTs', 'GACC_NIMO Teams', 'GACC_Area Command Teams',
                'GACC_Fire Use Teams', 'GACC_NICC priority', 'Area ']

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_GACC = pd.read_csv(filepath_or_buffer = FPA_FOD_file_list[0], sep = ',')
    FPA_FOD_GACC = gpd.GeoDataFrame(data = FPA_FOD_GACC, 
                                    crs = 'EPSG:4326',
                                    geometry = gpd.points_from_xy(x = FPA_FOD_GACC['LONGITUDE'], 
                                                                  y = FPA_FOD_GACC['LATITUDE']))
    temp = pd.DataFrame()
    for i in tqdm(range(len(FPA_FOD_GACC))):
        point = FPA_FOD_GACC.iloc[[i]]
        mutual = GACC[GACC['Date'] == point['DISCOVERY_DATE'].iloc[0]]
        if mutual.shape[0] == 0:
            mutual = point
            mutual[['index_right', 'GACCAbbrev', 'Date', 'GACC_PL', 'GACC_New fire', 'GACC_New LF', 'GACC_Uncont LF',
                    'GACC_Type 1 IMTs', 'GACC_Type 2 IMTs', 'GACC_NIMO Teams', 'GACC_Area Command Teams',
                    'GACC_Fire Use Teams', 'GACC_NICC priority', 'Area ']] = None
        else:
            mutual = gpd.sjoin(point, mutual, how = 'left')
            if mutual.shape[0] == 2:
                if (mutual['LATITUDE'].iloc[0] < 42.0 and mutual['LONGITUDE'].iloc[0] < -114.0):
                    mutual = mutual[mutual['Area '] == 'Western']
                else:
                    mutual = mutual[mutual['Area '] == 'Eastern']
                    
        temp = pd.concat(objs = [mutual, temp])
    
    FPA_FOD_GACC = temp.drop(labels = ['geometry', 'index_right', 'Date', 'Area ', 'GACC_NICC priority'], axis = 1)
    FPA_FOD_GACC = FPA_FOD_GACC.fillna(method = 'ffill')
    FPA_FOD_GACC.to_csv(path_or_buf = f'GACC/{year}_FPA_FOD_GACC.csv', sep = ',', index = False)

