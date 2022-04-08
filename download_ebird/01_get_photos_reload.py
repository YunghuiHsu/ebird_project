# 引入 requests 模組
import requests
import pandas as pd
import os
import sys
import time
from PIL import Image
from pathlib import Path
# from touch_dir import touch_dir
import argparse

# ======================================================================================================================================================
# 從命令列讀參數，指定 csv 檔的 parent dir
# 執行命令如下，選定裝有下載物種 csv 的目錄，即會讀取 csv 內容並下載照片
# python 01_get_photos.py --csvdir="./downloaded/csv/Furnariidae"
parser = argparse.ArgumentParser()
parser.add_argument('--csvdir', default="./downloaded/csv", type=str, help='path to csv files')
parser.add_argument('--start_idx', '-s', default=0, type=int,
                    help="Manual epoch number (useful on restarts)")
parser.add_argument('--end_idx', '-e', default=-1, type=int,
                    help="Manual epoch number (useful on restarts)")
opt = parser.parse_args()
# ======================================================================================================================================================
csvdir = Path(opt.csvdir)
jpgdir = Path(opt.csvdir.replace('csv', 'jpg_reload'))
# jpgdir_loaded = Path(opt.csvdir.replace('csv', 'jpg100'))


if jpgdir == csvdir:
    jpgdir = csvdir.joinpath('jpg_reload')

jpgdir.mkdir(exist_ok=True, parents=True)
print(f'"{jpgdir}" maked')

top_limit = 10000

csvfiles = list(csvdir.glob('*.csv'))

# print(f'There are {len(csvfiles):,d} csv files in "{csvdir}"')

# ======================================================================================================================================================
# Load Problemed img list
print('Loading Problemed img list')


df_problemed = pd.read_csv('meta/problemed.csv', index_col=0)
df_problemed

print(f'\t{len(df_problemed):4,d}')

start = opt.start_idx
end = len(df_problemed) if opt.end_idx == -1 else opt.end_idx
print(f'\tslice from [{start} : {end}]')

# df_problemed = df_problemed.iloc[start: end]


# ======================================================================================================================================================
# Download images

def download_imgs(family, sciname, ml_cn):
    
    success = False
    loop_cnt = 0

    dir_to_save = Path('downloaded', 'jpg_reloaded', family)
    if not dir_to_save.exists():
        dir_to_save.mkdir(parents=True)
    img_to_save = dir_to_save.joinpath(sciname + f'_{ml_cn}.jpg')
    print(f'Loading {img_to_save}')
    
    # 略過已存在照片
    if os.path.isfile(img_to_save):
        success = True
        print(f'\tIgnoring "{img_to_save.name}"')

    max_loop = 5

    while (not success) and (loop_cnt < max_loop) :
        try:
            print(f'\tDownloading {img_to_save} ({loop_cnt+1:d}/{max_loop:d})')
            r_photo = requests.get(f'https://cdn.download.ams.birds.cornell.edu/api/v1/asset/{ml_cn}/1200')

            with open(img_to_save, 'wb') as img_buff:
                img_buff.write(r_photo.content)
            print(f'\t{img_to_save.name} loaded')
            success = True
        except:
            loop_cnt += 1

start_time = time.time()
for idx, rows in df_problemed.iloc[start: end].iterrows():
    family, sciname, ml_cn, *_ = rows

    # print(f'[{i:7,d} ({i/len(df_problemed):5.2f}%) ]  |   {family:15s}, {sciname:15s}, {ml_cn:10d}', end='\r')
    time_cost = time.time()-start_time
    info = f"====> Progress: [{idx}]/[{len(df_problemed)}] | {100*idx/len(df_problemed):.2f}%"
    info += f"| time: {time_cost//(60*60):2.0f}h{time_cost//60%60:2.0f}m{time_cost%60:2.0f}s"
    info += f"| {family:15s}, {sciname:15s}, {ml_cn:10d}\t\t\t\t"
    print(info)

    download_imgs(family, sciname, ml_cn)