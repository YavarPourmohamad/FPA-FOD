import pandas as pd
import glob
from tqdm.auto import tqdm

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 2019
end_year = 2020

sheets = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
NPL_raw = pd.read_excel(io = 'Source_data/NPL/PreparednessLevels_adj.xlsx', sheet_name = sheets)

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_NPL = pd.read_csv(filepath_or_buffer = FPA_FOD_file_list[0], sep = ',')
    FPA_FOD_NPL['DISCOVERY_DATE'] = pd.to_datetime(FPA_FOD_NPL['DISCOVERY_DATE'])

    NPL = pd.DataFrame()
    NPL_raw_ = {}

    for i in tqdm(sheets):
        NPL_raw_[i] = pd.melt(NPL_raw[i], id_vars = 'Day', value_vars = NPL_raw[i].columns[1:])
        NPL_raw_[i].columns = ['Day', 'Year', 'NPL']
        NPL_raw_[i]['Month'] = i
        NPL_raw_[i] = NPL_raw_[i].dropna()
        NPL_raw_[i]['DISCOVERY_DATE'] = pd.to_datetime(NPL_raw_[i][['Year', 'Month', 'Day']])
        NPL_raw_[i] = NPL_raw_[i].drop(labels = ['Year', 'Month', 'Day'], axis = 1)
        NPL = pd.concat(objs = [NPL, NPL_raw_[i]])
    FPA_FOD_NPL = FPA_FOD_NPL.merge(right = NPL, on = 'DISCOVERY_DATE')
    FPA_FOD_NPL.to_csv(path_or_buf = f'NPL/{year}_FPA_FOD_NPL.csv', sep = ',', index = False)

