import datetime
import wget
from tqdm.auto import tqdm

nc_files = open('Source_data/NOAA_NDVI/nc_files_1991.txt').readlines()
for i in range(len(nc_files)):
    nc_files[i] = nc_files[i].split('\t')[0]
    year = nc_files[i].split('_')[-2][0:4]
    nc_files[i] = f'https://www.ncei.noaa.gov/data/land-normalized-difference-vegetation-index/access/{year}/' + nc_files[i]

for i in tqdm(nc_files):
    wget.download(url = i, out = 'Source_data/NOAA_NDVI/')

