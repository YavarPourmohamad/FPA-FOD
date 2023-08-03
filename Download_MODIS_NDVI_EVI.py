import requests
import wget
from tqdm.auto import tqdm

nc_files = open('/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/MODIS_NDVI_EVI/3122694244-download.txt').readlines()
for i in range(len(nc_files)):
    nc_files[i] = nc_files[i].split('\t')[0].replace('\n', '')
    username = 'yavar_pm'
    password = 'Naughtyboy_2053'
    filename = nc_files[i][-38:-1]
    r = requests.get(nc_files[i], auth = (username, password), stream = True)
    with open(file = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/MODIS_NDVI_EVI/' + filename, mode = 'wb') as out:
        out.write(r.content)


# for i in tqdm(nc_files[0:1]):
#     print(i)
#     wget.download(url = i, out = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Source_data/MODIS_NDVI_EVI/')