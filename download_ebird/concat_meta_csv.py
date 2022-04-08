import sys
import os
import requests
import pandas as pd
import numpy as np
import time
from pathlib import Path
import argparse

#########################################################################################################################
# concat all meta data in downloaded/csv/*/*.csv
#########################################################################################################################

# ======================================================================================================================================================
# 從命令列讀參數，指定 csv 檔的 parent dir
# 執行命令如下，選定裝有下載物種 csv 的目錄，即會讀取 csv 內容並下載照片
# python 01_get_photos.py --csvdir="./downloaded/csv/Furnariidae"
parser = argparse.ArgumentParser()
# parser.add_argument('--csvdir', default="./downloaded/csv", type=str, help='path to csv files')
parser.add_argument('--start_idx', '-s', default=0, type=int,
                    help="Manual epoch number (useful on restarts)")
parser.add_argument('--end_idx', '-e', default=-1, type=int,
                    help="Manual epoch number (useful on restarts)")
parser.add_argument('--metadir', default="meta", type=str,
                    help='path to save output meta file')
opt = parser.parse_args()


# ======================================================================================================================================================
dir_csv = Path('downloaded/csv')
path_csv = [path for path in dir_csv.glob('**/*.csv')]
path_csv.sort()
print(f'There are {len(path_csv):,d} csv files in "downloaded/csv/"')

start = opt.start_idx
end = len(path_csv) if opt.end_idx == -1 else opt.end_idx
print(f'\tslice from [{start} : {end}]')

dir_meta = Path(opt.metadir)
# path_meta_save = dir_meta.joinpath(f'meta_all_{start}_{end}.csv')
path_meta_save = dir_meta.joinpath(f'meta_all.csv')
print(f'\tMeta file save at {path_meta_save}')

def save_meta():
    with open(path_meta_save, 'a') as f:
        with open(path, mode='r', encoding='utf-8-sig') as meta_:   # utf-8-sig: 可以讀取有 BOM 的 csv
            lines = meta_.readlines()
            lines = lines  if idx==0 else lines[1:]    # if idx==0, retain columns
            
            for l, line_ in enumerate(lines):
                if (idx==0 and l==0):                   # if idx==0, insert column to columns
                    line_ = f',Parent_Dir,Sci_N,{line_}'
                else:
                    line_ = f'{l},{ parent_dir},{sci_n},{line_}'
                f.write(line_)
            

start_time = time.time()
for idx, path in enumerate(path_csv[start: end]):
    parent_dir = path.parent.stem
    sci_n = path.stem
    
    save_meta()

    time_cost = time.time()-start_time
    info = f"====> Progress: [{idx}]/[{len(path_csv)}] | {100*idx/len(path_csv):.2f}%"
    info += f"| time: {time_cost//(60*60):2.0f}h{time_cost//60%60:2.0f}m{time_cost%60:2.0f}s"
    info += f"| {parent_dir:15s}, {sci_n:15s}\t\t\t\t"
    print(info, end='\r')

