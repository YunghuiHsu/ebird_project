import os
import sys 
import requests
import time
import pandas as pd
import numpy as np
from pathlib import Path 
from PIL import Image
from skimage import io
import shutil
import argparse

# ======================================================================================================================================================
parser = argparse.ArgumentParser(
    description='Copy imgs from jpg100_1M by img list :"meta/jpg100_1M_filtered.csv"'
    )
parser.add_argument('--imgfile', default="meta/jpg100_1M_filtered.csv", type=str, help='files to be copyed')
parser.add_argument('--csvdir', default="downloaded/csv", type=str, help='path to csv files')
parser.add_argument('--start_idx', '-s', default=0, type=int,
                    help="Manual epoch number (useful on restarts)")
parser.add_argument('--end_idx', '-e', default=-1, type=int,
                    help="Manual epoch number (useful on restarts)")
opt = parser.parse_args()
# ======================================================================================================================================================
# Load img list
print('Loading img list')

# csvdir = Path(opt.csvdir)
# csvfiles = list(csvdir.glob('*.csv'))

dir_load = Path('downloaded/jpg100_1M')
dir_save_ = Path('downloaded/jpg_top100')
dir_save_.mkdir(exist_ok=True, parents=True)

df = pd.read_csv(opt.imgfile, index_col=0) 
print(f'\tData Size : {len(df):6,d}')

start = opt.start_idx
end = len(df) if opt.end_idx == -1 else opt.end_idx
print(f'\tslice from [{start} : {end}]')

# ======================================================================================================================================================
# Copy imgs
error_log =  dir_save_.joinpath(f'log_copy .txt')
df_ = df.iloc[start: end]

start_time = time.time()
for idx, (id, rows) in enumerate(df_.iterrows()):
    family, sciname, ml_cn, filename, *_ = rows
    
    dir_save_family = dir_save_.joinpath(family)
    if not dir_save_family.exists():
        dir_save_family.mkdir(parents=True, exist_ok=True)
    
    try:
        load_path = dir_load.joinpath(family, filename + '.jpg')
        save_path = dir_save_family.joinpath(filename + '.jpg')
        
        # 略過已存在照片
        if os.path.isfile(save_path):
            print(f'\tIgnoring "{save_path.name}"')
            continue

        shutil.copyfile(load_path, save_path)

        time_cost = time.time()-start_time
        info = f"====> Progress: [{idx}]/[{len(df_)}] | {100*idx/len(df_):.2f}%"
        info += f"| time: {time_cost//(60*60):2.0f}h{time_cost//60%60:2.0f}m{time_cost%60:2.0f}s"
        info += f"| {family:s}/{filename:30s}"
        print(info, end='\r')
    except Exception as err:
        print(f'\t{err}')
        with open(error_log, 'a') as file:
            file.write(f'{id:d}, {family:s}, {filename:s}\n')
