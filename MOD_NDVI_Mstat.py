import pandas as pd
import numpy as np
import xarray as xr
import rioxarray as rxr
import calendar
import datetime
import glob
from tqdm.auto import tqdm
from dateutil.relativedelta import relativedelta

#start_year = int(input('Select the start year: '))
#end_year = int(input('Select the end year: '))
start_year = 1992
end_year = 2020

for year in tqdm(range(start_year, end_year + 1)):
    print(year)
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')

    FPA_FOD_MOD_NDVI = pd.read_csv(filepath_or_buffer = FPA_FOD_file_list[0], sep = ',')
    FPA_FOD_MOD_NDVI['Month'] = pd.DatetimeIndex(FPA_FOD_MOD_NDVI['DISCOVERY_DATE']).month
    FPA_FOD_MOD_NDVI[['MOD_NDVI_12m', 'MOD_EVI_12m']] = None

    start_date = datetime.datetime.strptime(str(year), '%Y')
    if year <= 1999:
        FPA_FOD_MOD_NDVI.to_csv(path_or_buf = f'MOD_NDVI/{year}_FPA_FOD_MOD_NDVI.csv', sep = ',', index = False)
        continue

#2---------------------------------------
    while 1:
        try:
            month = start_date.month
            year = start_date.year
            points = FPA_FOD_MOD_NDVI[(FPA_FOD_MOD_NDVI['Year'] == year) & (FPA_FOD_MOD_NDVI['Month'] == month)]
            if points.empty == True:
                break
            NDVI_12m, EVI_12m = np.empty(len(points)), np.empty(len(points))
#3---------------------------------------
            for i in range(1, 13):
                try:
                    start_date_L = start_date - relativedelta(months = i)
                    doy = start_date_L.timetuple().tm_yday
                    year_L = start_date_L.strftime('%Y')
                    nc_files = glob.glob(pathname = f'/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/MODIS_NDVI_EVI/MOD13C2.A{year_L}*{doy}.061.*.hd')
                    DS = rxr.open_rasterio(filename = nc_files[0])
                    DA = DS.sel(indexers = {'y': xr.DataArray(points['LATITUDE']),
                                            'x': xr.DataArray(points['LONGITUDE'])}, method = 'nearest')
                    
                    DA['CMG 0.05 Deg Monthly NDVI'] = DA['CMG 0.05 Deg Monthly NDVI'] * 0.0001 # scale factor provided by Modis = 0.0001
                    DA['CMG 0.05 Deg Monthly EVI'] = DA['CMG 0.05 Deg Monthly EVI'] * 0.0001 # scale factor provided by Modis = 0.0001
                    
                    DA['CMG 0.05 Deg Monthly NDVI'] = DA['CMG 0.05 Deg Monthly NDVI'].round(2)
                    DA['CMG 0.05 Deg Monthly EVI'] = DA['CMG 0.05 Deg Monthly EVI'].round(2)

                    NDVI_12m = np.column_stack((NDVI_12m, DA['CMG 0.05 Deg Monthly NDVI'][0].astype(str)))
                    EVI_12m = np.column_stack((EVI_12m, DA['CMG 0.05 Deg Monthly EVI'][0].astype(str)))
                except:
                    pass
#3---------------------------------------

            NDVI_12m = np.delete(NDVI_12m, 0, axis = 1)
            NDVI_12m = np.char.replace(np.array([str(l).strip("[]") for l in NDVI_12m]), '\n', '')

            EVI_12m = np.delete(EVI_12m, 0, axis = 1)
            EVI_12m = np.char.replace(np.array([str(l).strip("[]") for l in EVI_12m]), '\n', '')

            FPA_FOD_MOD_NDVI.loc[(FPA_FOD_MOD_NDVI['Year'] == year) & (FPA_FOD_MOD_NDVI['Month'] == month), 'MOD_NDVI_12m'] = NDVI_12m
            FPA_FOD_MOD_NDVI.loc[(FPA_FOD_MOD_NDVI['Year'] == year) & (FPA_FOD_MOD_NDVI['Month'] == month), 'MOD_EVI_12m'] = EVI_12m
            start_date = start_date + relativedelta(months = 1)
        except:
            start_date = start_date + relativedelta(months = 1)
            pass
#2---------------------------------------

    FPA_FOD_MOD_NDVI.to_csv(path_or_buf = f'MOD_NDVI/{year - 1}_FPA_FOD_MOD_NDVI.csv', sep = ',', index = False)

