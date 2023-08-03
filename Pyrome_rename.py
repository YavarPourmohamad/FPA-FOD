import pandas as pd
import glob

files = glob.glob(pathname = '/bsuhome/yavarpourmohamad/scratch/Summer_2022/Aggregated/*.csv')

for file in files[0:1]:
    FPA_FOD = pd.read_csv(filepath_or_buffer = file,
                          sep = ',',
                          low_memory = False)
    FPA_FOD = FPA_FOD.rename(columns = {'NAME': 'Pyrome_name'})
    FPA_FOD.to_csv(path_or_buf = file, sep = ',')