import pandas as pd
import glob
from tqdm.auto import tqdm

start_year = 1992
end_year = 2020

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD = pd.read_csv(filepath_or_buffer = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/FPA_FOD/{year}_FPA_FOD.csv', sep = ',', low_memory = False)
    FPA_FOD_list = glob.glob(pathname = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/Results/**/{year}_FPA_FOD_*.csv')
    for file in tqdm(FPA_FOD_list):
        temp = pd.read_csv(filepath_or_buffer = file, sep = ',', low_memory = False)
        if 'Year' in temp:
            temp = temp.drop(labels = ['FIRE_SIZE', 'LONGITUDE', 'Year'], axis = 1)
        else:
            temp = temp.drop(labels = ['FIRE_SIZE', 'LONGITUDE'], axis = 1)

        if 'FPA_FOD_MOD_NDVI' in file:
            FPA_FOD = pd.merge(left = FPA_FOD,
                               right = temp[['FOD_ID', 'FPA_ID', 'MOD_NDVI_12m', 'MOD_EVI_12m']],
                               how = 'inner',
                               on = ['FOD_ID', 'FPA_ID'])
        elif 'SVI' in file:
            FPA_FOD = pd.merge(left = FPA_FOD,
                               right = temp[['FOD_ID', 'FPA_ID', 'TRACT', 'RPL_THEMES', 'RPL_THEME1',
                                             'EPL_POV', 'EPL_UNEMP', 'EPL_PCI', 'EPL_NOHSDP', 'RPL_THEME2',
                                             'EPL_AGE65', 'EPL_AGE17', 'EPL_DISABL', 'EPL_SNGPNT', 'RPL_THEME3',
                                             'EPL_MINRTY', 'EPL_LIMENG', 'RPL_THEME4', 'EPL_MUNIT', 'EPL_MOBILE',
                                             'EPL_CROWD', 'EPL_NOVEH', 'EPL_GROUPQ']],
                               how = 'inner',
                               on = ['FOD_ID', 'FPA_ID'])
        else:
            FPA_FOD = pd.merge(left = FPA_FOD,
                               right = temp,
                               how = 'inner',
                               on = ['DISCOVERY_DATE', 'LATITUDE', 'STATE', 'OWNER_DESCR', 'NWCG_GENERAL_CAUSE'])

        FPA_FOD = FPA_FOD.drop_duplicates(subset = ['FOD_ID', 'FPA_ID'])
        FPA_FOD['Year'] = FPA_FOD['FIRE_YEAR']
        del temp
    FPA_FOD.to_csv(path_or_buf = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/Aggregated/{year}_FPA_FOD_Agg.csv', sep = ',', index = False)
    del FPA_FOD

FPA_FOD_list = glob.glob(pathname = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/Aggregated/*.csv')
for file in tqdm(FPA_FOD_list):
    FPA_FOD = pd.read_csv(file, sep = ',', low_memory = False)

    # Corrections
    if 'Month_x' in FPA_FOD.columns:
        FPA_FOD = FPA_FOD.drop(labels = ['Month_x', 'Month_y'], axis = 1)
    
    if 'COUNTY_y' in FPA_FOD.columns:
        FPA_FOD = FPA_FOD.drop(labels = 'COUNTY_y', axis = 1)
        FPA_FOD = FPA_FOD.rename(columns = {'COUNTY_x':'COUNTY'})

    if 'Unnamed: 0' in FPA_FOD.columns:
        FPA_FOD = FPA_FOD.drop(labels = 'Unnamed: 0', axis = 1)
    
    if 'Land_cover' in FPA_FOD.columns:
        FPA_FOD = FPA_FOD.rename(columns = {'Land_cover': 'Land_Cover'})
    
    FPA_FOD = FPA_FOD.round({'HSEF': 2, 'pr_Normal': 2, 'rmin_Normal': 1, 'rmax_Normal': 1, 'sph_Normal': 4,
                             'fm100_Normal': 1, 'fm1000_Normal':1, 'vpd_Normal': 2, 'vs': 2, 'etr': 2, 'fm100': 1,
                             'fm1000': 1, 'vpd': 2, 'pr_5D_mean': 2, 'rmin_5D_mean': 1, 'rmax_5D_mean': 1, 'vs_5D_mean': 2,
                             'etr_5D_mean': 2, 'fm100_5D_mean': 1, 'fm1000_5D_mean': 1, 'vpd_5D_mean': 2, 'pr_5D_min': 2,
                             'pr_5D_max': 2, 'rmin_5D_min': 1, 'rmin_5D_max': 1, 'vs_5D_max': 2, 'etr_5D_max': 2,
                             'fm100_5D_min': 1, 'fm1000_5D_min': 1, 'vpd_5D_max': 2, 'GHM': 2, 'NDVI-1day': 2, 'Popo_1km': 4,
                             'Population': 4, 'road_county_dis': 1, 'road_interstate_dis': 1, 'road_common_name_dis': 1,
                             'road_other_dis':1, 'road_state_dis': 1, 'road_US_dis': 1, 'TPI_1km': 2, 'TRI_1km': 3, 'TRI': 3})

    cols = ['tmmn_Normal', 'tmmx_Normal', 'bi_Normal', 'srad', 'bi', 'tmmn_5D_mean', 'tmmx_5D_mean', 'srad_5D_mean',
            'bi_5D_mean', 'srad_5D_max', 'bi_5D_max', 'Aspect_1km', 'Elevation_1km', 'Slope_1km', 'EVC_1km', 'EVH_1km', 'GDP']

    FPA_FOD[cols] = FPA_FOD[cols].astype(int, errors = 'ignore')
    FPA_FOD.to_csv(path_or_buf = file, sep = ',', index = False)
    
del FPA_FOD

FPA_FOD_list = glob.glob(pathname = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/Aggregated/*.csv')

FPA_FOD = pd.concat(map(pd.read_csv, FPA_FOD_list), ignore_index = True)

FPA_FOD.to_csv(path_or_buf = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Aggregated/FPA_FOD_Plus.csv', sep = ',', index = False)

del FPA_FOD