from tqdm.auto import tqdm
import wget

start_year = int(input('Select the start year: '))
end_year = int(input('Select the end year: '))

variables = ['pr', 'tmmn', 'tmmx', 'rmin', 'rmax', 'sph', 'vs', 'th', 'srad', 'etr', 'fm100', 'fm1000', 'bi', 'vpd', 'erc']

for i in tqdm(variables):
  print(f'Variable = {i} for years = {start_year} to {end_year}\n')
  for year in tqdm(range(start_year, end_year + 2)):
        wget.download(url = f'http://www.northwestknowledge.net/metdata/data/{i}_{year}.nc', 
                      out = 'Source_data/GRIDMET/')

