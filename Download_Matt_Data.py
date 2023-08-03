import pandas as pd
from tqdm.auto import tqdm
import wget

URL_list = pd.read_csv(filepath_or_buffer = 'Matt_data/urls.txt', sep = ',')
for i in tqdm(range(len(URL_list))):
    wget.download(url = URL_list.loc[i, 'Signed URL'], out = 'Matt_data/')