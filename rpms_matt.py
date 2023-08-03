import pandas as pd
import numpy as np
import geopandas as gpd
import xarray as xr
import geemap
import glob
import rioxarray
from osgeo import gdal
from tqdm.auto import tqdm

start_year = 1992
end_year = 2020

for year in tqdm(range(start_year, end_year + 1)):
    FPA_FOD_file_list = glob.glob(pathname = f'FPA_FOD/{year}_FPA_FOD.csv')
    FPA_FOD_rpms = pd.read_csv(FPA_FOD_file_list[0], low_memory = False)
    FPA_FOD_rpms = FPA_FOD_rpms[['DISCOVERY_DATE', 'NWCG_GENERAL_CAUSE', 'FIRE_SIZE', 'LATITUDE',	'LONGITUDE', 'OWNER_DESCR', 'STATE', 'Year']]
    FPA_FOD_rpms['rpms'] = None

    rpms = xr.open_rasterio(filename = f'Source_data/Matt_data/rpms_{year}.tif').drop('band')[0]

    rpms_pnt = rpms.sel(indexers={'y': xr.DataArray(FPA_FOD_rpms['LATITUDE']),
                                  'x': xr.DataArray(FPA_FOD_rpms['LONGITUDE'])}, method = 'nearest')
 
    FPA_FOD_rpms['rpms'] = rpms_pnt
    del rpms_pnt
 
    FPA_FOD_rpms.to_csv(path_or_buf = f'rpms/{year}_FPA_FOD_rpms_pt.csv', sep = ',', index = False)