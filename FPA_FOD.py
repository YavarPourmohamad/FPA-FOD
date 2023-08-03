import pandas as pd
import sqlite3

start_year = int(input('Select the start year: '))
end_year = int(input('Select the end year: '))

FPA_FOD = sqlite3.connect("FPA_FOD/FPA_FOD_20210617.sqlite")
FPA_FOD = pd.read_sql_query(sql = "SELECT * FROM Fires", con = FPA_FOD)
FPA_FOD['DISCOVERY_DATE'] = pd.to_datetime(FPA_FOD['DISCOVERY_DATE'], format = '%m/%d/%Y %H:%M')
FPA_FOD = FPA_FOD[['DISCOVERY_DATE', 'NWCG_GENERAL_CAUSE', 'FIRE_SIZE', 'LATITUDE',	'LONGITUDE', 'OWNER_DESCR', 'STATE']]
FPA_FOD['DISCOVERY_DATE'] = pd.to_datetime(FPA_FOD['DISCOVERY_DATE'])
FPA_FOD = FPA_FOD.sort_values(by = 'DISCOVERY_DATE')
FPA_FOD['Year'] = pd.DatetimeIndex(data = FPA_FOD['DISCOVERY_DATE']).year
#FPA_FOD = FPA_FOD.loc[FPA_FOD['STATE'].isin(['WA', 'ID', 'OR', 'MT', 'WY', 'CA', 'NV', 'UT', 'CO', 'AZ', 'NM'])]

for i in range(start_year, end_year + 1):
    FPA_FOD[FPA_FOD['Year'] == i].to_csv(path_or_buf = f'FPA_FOD/{i}_FPA_FOD.csv', sep = ',', index = False)
del FPA_FOD

