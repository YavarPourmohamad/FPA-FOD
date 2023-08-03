import pandas as pd
import geopandas as gpd
import geemap
import glob
from tqdm.auto import tqdm

def feature_arash(yearInt):
    if yearInt <= 2009:
        COUNTY = 'COUNTY'
        TRACT = 'TRACT'
        RPL_THEMES = 'USTP' # SVI Overall Vulnerability
        RPL_THEME1 = 'USG1TP'
        EPL_POV = 'USG1V1P'
        EPL_UNEMP = 'USG1V2P'
        EPL_PCI = 'USG1V3P'
        EPL_NOHSDP = 'USG1V4P'
        RPL_THEME2 = 'USG2TP'
        EPL_AGE65 = 'USG2V1P'
        EPL_AGE17 = 'USG2V2P'
        EPL_DISABL = 'USG2V3P'
        EPL_SNGPNT = 'USG2V4P'
        RPL_THEME3 = 'USG3TP'
        EPL_MINRTY = 'USG3V1P'
        EPL_LIMENG = 'USG3V2P'
        RPL_THEME4 = 'USG4TP'
        EPL_MUNIT = 'USG4V1P'
        EPL_MOBILE = 'USG4V2P'
        EPL_CROWD = 'USG4V3P'
        EPL_NOVEH = 'USG4V4P'
        EPL_GROUPQ = 'USG4V5P'
        Themes = [COUNTY, TRACT, RPL_THEMES, RPL_THEME1, EPL_POV, EPL_UNEMP, EPL_PCI, EPL_NOHSDP, RPL_THEME2,
                  EPL_AGE65, EPL_AGE17, EPL_DISABL, EPL_SNGPNT, RPL_THEME3, EPL_MINRTY, EPL_LIMENG, RPL_THEME4,
                  EPL_MUNIT, EPL_MOBILE, EPL_CROWD, EPL_NOVEH, EPL_GROUPQ, 'geometry']  
    # Load SVI 2010 metadata    
    if yearInt > 2009 and yearInt <= 2013:
        COUNTY = 'COUNTY'
        TRACT = 'TRACT'
        RPL_THEMES = 'R_PL_THEME'
        RPL_THEME1 = 'R_PL_THE_1'
        EPL_POV = 'E_PL_POV'
        EPL_UNEMP = 'E_PL_UNEMP'
        EPL_PCI = 'E_PL_PCI'
        EPL_NOHSDP = 'E_PL_NOHSD'
        RPL_THEME2 = 'R_PL_THE_2'
        EPL_AGE65 = 'PL_AGE65'
        EPL_AGE17 = 'PL_AGE17'
#         EPL_DISABL = 'EPL_DISABL'# Not availabe
        EPL_SNGPNT = 'PL_SNGPRNT'
        RPL_THEME3 = 'R_PL_THE_3'
        EPL_MINRTY = 'PL_MINORIT'
        EPL_LIMENG = 'E_PL_LIMEN'
        RPL_THEME4 = 'R_PL_THE_4'
        EPL_MUNIT = 'E_PL_MUNIT'
        EPL_MOBILE = 'E_PL_MOBIL'
        EPL_CROWD = 'E_PL_CROWD'
        EPL_NOVEH = 'E_PL_NOVEH'
        EPL_GROUPQ = 'PL_GROUPQ'
        Themes = [COUNTY, TRACT, RPL_THEMES, RPL_THEME1, EPL_POV, EPL_UNEMP, EPL_PCI, EPL_NOHSDP, RPL_THEME2,
                  EPL_AGE65, EPL_AGE17, EPL_SNGPNT, RPL_THEME3, EPL_MINRTY, EPL_LIMENG, RPL_THEME4,
                  EPL_MUNIT, EPL_MOBILE, EPL_CROWD, EPL_NOVEH, EPL_GROUPQ, 'geometry'] 
   
    # Load SVI 2014 and after metadata    
    if yearInt > 2013:
        RPL_THEMES = 'RPL_THEMES'
        RPL_THEME1 = 'RPL_THEME1'
        EPL_POV = 'EPL_POV'
        EPL_UNEMP = 'EPL_UNEMP'
        EPL_PCI = 'EPL_PCI'
        EPL_NOHSDP = 'EPL_NOHSDP'
        RPL_THEME2 = 'RPL_THEME2'
        EPL_AGE65 = 'EPL_AGE65'
        EPL_AGE17 = 'EPL_AGE17'
        EPL_DISABL = 'EPL_DISABL'
        EPL_SNGPNT = 'EPL_SNGPNT'
        RPL_THEME3 = 'RPL_THEME3'
        EPL_MINRTY = 'EPL_MINRTY'
        EPL_LIMENG = 'EPL_LIMENG'
        RPL_THEME4 = 'RPL_THEME4'
        EPL_MUNIT = 'EPL_MUNIT'
        EPL_MOBILE = 'EPL_MOBILE'
        EPL_CROWD = 'EPL_CROWD'
        EPL_NOVEH = 'EPL_NOVEH'
        EPL_GROUPQ = 'EPL_GROUPQ'
        Themes = ['COUNTY', 'TRACT', RPL_THEMES, RPL_THEME1, EPL_POV, EPL_UNEMP, EPL_PCI, EPL_NOHSDP, RPL_THEME2, EPL_AGE65,
                  EPL_AGE17, EPL_DISABL, EPL_SNGPNT, RPL_THEME3, EPL_MINRTY, EPL_LIMENG, RPL_THEME4,
                  EPL_MUNIT, EPL_MOBILE, EPL_CROWD, EPL_NOVEH, EPL_GROUPQ, 'geometry']
        if yearInt >= 2020:
            RPL_THEMES = 'RPL_THEMES'
            RPL_THEME1 = 'RPL_THEME1'
            EPL_POV = 'EPL_POV150'
            EPL_UNEMP = 'EPL_UNEMP'
            # EPL_PCI = 'EPL_PCI' # Not Available
            EPL_NOHSDP = 'EPL_NOHSDP'
            RPL_THEME2 = 'RPL_THEME2'
            EPL_AGE65 = 'EPL_AGE65'
            EPL_AGE17 = 'EPL_AGE17'
            EPL_DISABL = 'EPL_DISABL'
            EPL_SNGPNT = 'EPL_SNGPNT'
            RPL_THEME3 = 'RPL_THEME3'
            EPL_MINRTY = 'EPL_MINRTY'
            EPL_LIMENG = 'EPL_LIMENG'
            RPL_THEME4 = 'RPL_THEME4'
            EPL_MUNIT = 'EPL_MUNIT'
            EPL_MOBILE = 'EPL_MOBILE'
            EPL_CROWD = 'EPL_CROWD'
            EPL_NOVEH = 'EPL_NOVEH'
            EPL_GROUPQ = 'EPL_GROUPQ'
            Themes = ['COUNTY', 'TRACT', RPL_THEMES, RPL_THEME1, EPL_POV, EPL_UNEMP, EPL_NOHSDP, RPL_THEME2, EPL_AGE65,
                    EPL_AGE17, EPL_DISABL, EPL_SNGPNT, RPL_THEME3, EPL_MINRTY, EPL_LIMENG, RPL_THEME4,
                    EPL_MUNIT, EPL_MOBILE, EPL_CROWD, EPL_NOVEH, EPL_GROUPQ, 'geometry']  
    return Themes

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 1992
end_year = 2020

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/FPA_FOD/{year}_FPA_FOD.csv')

    FPA_FOD_SVI = geemap.csv_to_gdf(in_csv = FPA_FOD_file_list[0],
                                    latitude = 'LATITUDE',
                                    longitude = 'LONGITUDE')
    if year < 2010:
        SVI_data = gpd.read_file(filename = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/SVI/SVI2000_US/SVI2000_US.shp')[feature_arash(year)]
        SVI_data = SVI_data.to_crs('EPSG:4326')
        FPA_FOD_SVI = gpd.sjoin(left_df = FPA_FOD_SVI, right_df = SVI_data, how = 'left')
        FPA_FOD_SVI = FPA_FOD_SVI.rename(columns = {'USTP': 'RPL_THEMES', 'USG1TP': 'RPL_THEME1', 'USG1V1P': 'EPL_POV',
                                                    'USG1V2P': 'EPL_UNEMP', 'USG1V3P': 'EPL_PCI', 'USG1V4P': 'EPL_NOHSDP',
                                                    'USG2TP': 'RPL_THEME2', 'USG2V1P': 'EPL_AGE65', 'USG2V2P': 'EPL_AGE17', 
                                                    'USG2V3P': 'EPL_DISABL', 'USG2V4P': 'EPL_SNGPNT', 'USG3TP': 'RPL_THEME3',
                                                    'USG3V1P': 'EPL_MINRTY', 'USG3V2P': 'EPL_LIMENG', 'USG4TP': 'RPL_THEME4',
                                                    'USG4V1P': 'EPL_MUNIT', 'USG4V2P': 'EPL_MOBILE', 'USG4V3P': 'EPL_CROWD',
                                                    'USG4V4P': 'EPL_NOVEH', 'USG4V5P': 'EPL_GROUPQ'})
        FPA_FOD_SVI = FPA_FOD_SVI.drop(labels = ['geometry', 'index_right', 'COUNTY_left'], axis = 1)
        FPA_FOD_SVI = FPA_FOD_SVI.rename(columns = {'COUNTY_right': 'COUNTY'})

    if (year >= 2010) & (year < 2014):
        SVI_data = gpd.read_file(filename = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/SVI/SVI2010_US/SVI2010_US.shp')[feature_arash(year)]
        SVI_data = SVI_data.to_crs('EPSG:4326')
        FPA_FOD_SVI = gpd.sjoin(left_df = FPA_FOD_SVI, right_df = SVI_data, how = 'left')
        FPA_FOD_SVI = FPA_FOD_SVI.rename(columns = {'R_PL_THEME': 'RPL_THEMES', 'R_PL_THE_1': 'RPL_THEME1',
                                                    'E_PL_POV': 'EPL_POV', 'E_PL_UNEMP': 'EPL_UNEMP', 'E_PL_PCI': 'EPL_PCI',
                                                    'E_PL_NOHSD': 'EPL_NOHSDP', 'R_PL_THE_2': 'RPL_THEME2',
                                                    'PL_AGE65': 'EPL_AGE65', 'PL_AGE17': 'EPL_AGE17', 'PL_SNGPRNT': 'EPL_SNGPNT',
                                                    'R_PL_THE_3': 'RPL_THEME3', 'PL_MINORIT': 'EPL_MINRTY',
                                                    'E_PL_LIMEN': 'EPL_LIMENG', 'R_PL_THE_4': 'RPL_THEME4',
                                                    'E_PL_MUNIT': 'EPL_MUNIT', 'E_PL_MOBIL': 'EPL_MOBILE',
                                                    'E_PL_CROWD': 'EPL_CROWD', 'E_PL_NOVEH': 'EPL_NOVEH',
                                                    'PL_GROUPQ': 'EPL_GROUPQ'})
        FPA_FOD_SVI['EPL_DISABL'] = None
        FPA_FOD_SVI = FPA_FOD_SVI.drop(labels = ['geometry', 'index_right', 'COUNTY_left'], axis = 1)
        FPA_FOD_SVI = FPA_FOD_SVI.rename(columns = {'COUNTY_right': 'COUNTY'})

    if (year >= 2014) & (year < 2016):
        SVI_data = gpd.read_file(filename = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/SVI/SVI2014_US/SVI2014_US.shp')
        SVI_data = SVI_data.rename(columns = {'TRACTCE': 'TRACT'})[feature_arash(year)]
        SVI_data = SVI_data.to_crs('EPSG:4326')
        FPA_FOD_SVI = gpd.sjoin(left_df = FPA_FOD_SVI, right_df = SVI_data, how = 'left')
        FPA_FOD_SVI = FPA_FOD_SVI.rename(columns = {'R_PL_THEMES': 'RPL_THEMES', 'R_PL_THEME1': 'RPL_THEME1',
                                                    'E_PL_POV': 'EPL_POV', 'E_PL_UNEMP': 'EPL_UNEMP', 'E_PL_PCI': 'EPL_PCI',
                                                    'E_PL_NOHSDIP': 'EPL_NOHSDP', 'R_PL_THEME2': 'RPL_THEME2',
                                                    'PL_AGE65': 'EPL_AGE65', 'PL_AGE17': 'EPL_AGE17', 'PL_SNGPRNT': 'EPL_SNGPNT',
                                                    'R_PL_THEME3': 'RPL_THEME3', 'PL_MINORITY': 'EPL_MINRTY',
                                                    'E_PL_LIMENG': 'EPL_LIMENG', 'R_PL_THEME4': 'RPL_THEME4',
                                                    'E_PL_MUNIT': 'EPL_MUNIT', 'E_PL_MOBILE': 'EPL_MOBILE',
                                                    'E_PL_CROWD': 'EPL_CROWD', 'E_PL_NOVEH': 'EPL_NOVEH',
                                                    'PL_GROUPQ': 'EPL_GROUPQ', 'TRACTCE': 'TRACT'})
        FPA_FOD_SVI = FPA_FOD_SVI.drop(labels = ['geometry', 'index_right', 'COUNTY_left'], axis = 1)
        FPA_FOD_SVI = FPA_FOD_SVI.rename(columns = {'COUNTY_right': 'COUNTY'})

    if (year >= 2016) & (year < 2018):
        SVI_data = gpd.read_file(filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/SVI/SVI2016_US/SVI2016_US.shp')
        SVI_data['TRACT'] = SVI_data.apply(lambda row : row['FIPS'].replace(str(row['STCNTY']), ''), axis=1)
        SVI_data = SVI_data[feature_arash(year)]
        SVI_data = SVI_data.to_crs('EPSG:4326')
        FPA_FOD_SVI = gpd.sjoin(left_df = FPA_FOD_SVI, right_df = SVI_data, how = 'left')
        FPA_FOD_SVI = FPA_FOD_SVI.rename(columns = {'R_PL_THEMES': 'RPL_THEMES', 'R_PL_THEME1': 'RPL_THEME1',
                                                    'E_PL_POV': 'EPL_POV', 'E_PL_UNEMP': 'EPL_UNEMP', 'E_PL_PCI': 'EPL_PCI',
                                                    'E_PL_NOHSDIP': 'EPL_NOHSDP', 'R_PL_THEME2': 'RPL_THEME2',
                                                    'PL_AGE65': 'EPL_AGE65', 'PL_AGE17': 'EPL_AGE17', 'PL_SNGPRNT': 'EPL_SNGPNT',
                                                    'R_PL_THEME3': 'RPL_THEME3', 'PL_MINORITY': 'EPL_MINRTY',
                                                    'E_PL_LIMENG': 'EPL_LIMENG', 'R_PL_THEME4': 'RPL_THEME4',
                                                    'E_PL_MUNIT': 'EPL_MUNIT', 'E_PL_MOBILE': 'EPL_MOBILE',
                                                    'E_PL_CROWD': 'EPL_CROWD', 'E_PL_NOVEH': 'EPL_NOVEH',
                                                    'PL_GROUPQ': 'EPL_GROUPQ'})
        FPA_FOD_SVI = FPA_FOD_SVI.drop(labels = ['geometry', 'index_right', 'COUNTY_left'], axis = 1)
        FPA_FOD_SVI = FPA_FOD_SVI.rename(columns = {'COUNTY_right': 'COUNTY'})

    if (year >= 2018) & (year < 2020):
        SVI_data = gpd.read_file(filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/SVI/SVI2018_US/SVI2018_US_tract.shp')
        SVI_data['TRACT'] = SVI_data.apply(lambda row : row['FIPS'].replace(str(row['STCNTY']), ''), axis=1)
        SVI_data = SVI_data[feature_arash(year)]
        SVI_data = SVI_data.to_crs('EPSG:4326')
        FPA_FOD_SVI = gpd.sjoin(left_df = FPA_FOD_SVI, right_df = SVI_data, how = 'left')
        FPA_FOD_SVI = FPA_FOD_SVI.rename(columns = {'R_PL_THEMES': 'RPL_THEMES', 'R_PL_THEME1': 'RPL_THEME1',
                                                    'E_PL_POV': 'EPL_POV', 'E_PL_UNEMP': 'EPL_UNEMP', 'E_PL_PCI': 'EPL_PCI',
                                                    'E_PL_NOHSDIP': 'EPL_NOHSDP', 'R_PL_THEME2': 'RPL_THEME2',
                                                    'PL_AGE65': 'EPL_AGE65', 'PL_AGE17': 'EPL_AGE17', 'PL_SNGPRNT': 'EPL_SNGPNT',
                                                    'R_PL_THEME3': 'RPL_THEME3', 'PL_MINORITY': 'EPL_MINRTY',
                                                    'E_PL_LIMENG': 'EPL_LIMENG', 'R_PL_THEME4': 'RPL_THEME4',
                                                    'E_PL_MUNIT': 'EPL_MUNIT', 'E_PL_MOBILE': 'EPL_MOBILE',
                                                    'E_PL_CROWD': 'EPL_CROWD', 'E_PL_NOVEH': 'EPL_NOVEH',
                                                    'PL_GROUPQ': 'EPL_GROUPQ'})
        FPA_FOD_SVI = FPA_FOD_SVI.drop(labels = ['geometry', 'index_right', 'COUNTY_left'], axis = 1)
        FPA_FOD_SVI = FPA_FOD_SVI.rename(columns = {'COUNTY_right': 'COUNTY'})
    
    if year >= 2020:
        SVI_data = gpd.read_file(filename = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/SVI/SVI2020_US/SVI2020_US.shp')
        SVI_data['TRACT'] = SVI_data.apply(lambda row : row['FIPS'].replace(str(row['STCNTY']), ''), axis=1)
        SVI_data = SVI_data[feature_arash(year)]
        SVI_data = SVI_data.to_crs('EPSG:4326')
        FPA_FOD_SVI = gpd.sjoin(left_df = FPA_FOD_SVI, right_df = SVI_data, how = 'left')
        FPA_FOD_SVI['E_PL_PCI'] = None
        FPA_FOD_SVI = FPA_FOD_SVI.rename(columns = {'R_PL_THEMES': 'RPL_THEMES', 'R_PL_THEME1': 'RPL_THEME1',
                                                    'EPL_POV150': 'EPL_POV', 'E_PL_UNEMP': 'EPL_UNEMP', 'E_PL_PCI': 'EPL_PCI',
                                                    'E_PL_NOHSDIP': 'EPL_NOHSDP', 'R_PL_THEME2': 'RPL_THEME2',
                                                    'PL_AGE65': 'EPL_AGE65', 'PL_AGE17': 'EPL_AGE17', 'PL_SNGPRNT': 'EPL_SNGPNT',
                                                    'R_PL_THEME3': 'RPL_THEME3', 'PL_MINORITY': 'EPL_MINRTY',
                                                    'E_PL_LIMENG': 'EPL_LIMENG', 'R_PL_THEME4': 'RPL_THEME4',
                                                    'E_PL_MUNIT': 'EPL_MUNIT', 'E_PL_MOBILE': 'EPL_MOBILE',
                                                    'E_PL_CROWD': 'EPL_CROWD', 'E_PL_NOVEH': 'EPL_NOVEH',
                                                    'PL_GROUPQ': 'EPL_GROUPQ'})
        FPA_FOD_SVI = FPA_FOD_SVI.drop(labels = ['geometry', 'index_right', 'COUNTY_left'], axis = 1)
        FPA_FOD_SVI = FPA_FOD_SVI.rename(columns = {'COUNTY_right': 'COUNTY'})
    
    FPA_FOD_SVI = FPA_FOD_SVI[['FOD_ID', 'FPA_ID', 'SOURCE_SYSTEM_TYPE', 'SOURCE_SYSTEM', 'NWCG_REPORTING_AGENCY',
                               'NWCG_REPORTING_UNIT_ID', 'NWCG_REPORTING_UNIT_NAME', 'SOURCE_REPORTING_UNIT',
                               'SOURCE_REPORTING_UNIT_NAME', 'LOCAL_FIRE_REPORT_ID', 'LOCAL_INCIDENT_ID', 'FIRE_CODE',
                               'FIRE_NAME', 'ICS_209_PLUS_INCIDENT_JOIN_ID', 'ICS_209_PLUS_COMPLEX_JOIN_ID', 'MTBS_ID',
                               'MTBS_FIRE_NAME', 'COMPLEX_NAME', 'FIRE_YEAR', 'DISCOVERY_DATE', 'DISCOVERY_DOY',
                               'DISCOVERY_TIME', 'NWCG_CAUSE_CLASSIFICATION', 'NWCG_GENERAL_CAUSE', 'NWCG_CAUSE_AGE_CATEGORY',
                               'CONT_DATE', 'CONT_DOY', 'CONT_TIME', 'FIRE_SIZE', 'FIRE_SIZE_CLASS', 'LATITUDE',
                               'LONGITUDE', 'OWNER_DESCR', 'STATE', 'COUNTY', 'FIPS_CODE', 'FIPS_NAME', 'Year',
                               'TRACT', 'RPL_THEMES', 'RPL_THEME1', 'EPL_POV', 'EPL_UNEMP', 'EPL_PCI',
                               'EPL_NOHSDP', 'RPL_THEME2', 'EPL_AGE65', 'EPL_AGE17', 'EPL_DISABL', 'EPL_SNGPNT',
                               'RPL_THEME3', 'EPL_MINRTY', 'EPL_LIMENG', 'RPL_THEME4', 'EPL_MUNIT', 'EPL_MOBILE',
                               'EPL_CROWD', 'EPL_NOVEH', 'EPL_GROUPQ']]
    FPA_FOD_SVI.to_csv(path_or_buf = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/SVI/{year}_FPA_FOD_SVI.csv', sep = ',', index = False)