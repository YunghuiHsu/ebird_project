# 引入 requests 模組
import requests
import pandas as pd
import os
from touch_dir import touch_dir
import argparse

# 從命令列讀參數，指定 csv 檔的 parent dir
# 執行命令如下，選定裝有下載物種 csv 的目錄，即會讀取 csv 內容並下載照片
# python 01_get_photos.py --csvdir="./downloaded/csv/Furnariidae"
parser = argparse.ArgumentParser()
parser.add_argument('--csvdir', default="./downloaded/csv/Accipitridae", type=str, help='path to csv files')
opt = parser.parse_args()

csvdir = opt.csvdir
jpgdir = csvdir.replace('csv', 'jpg')

if jpgdir == csvdir:
    jpgdir = csvdir + '/jpg'

touch_dir(jpgdir)

top_limit = 10000

# download images
for target_sp_file in os.listdir(csvdir):

    if not target_sp_file.endswith('.csv'):
        continue

    sp_df_photo = pd.read_csv('%s/%s' % (csvdir, target_sp_file))
    sp_df_photo_sorted = sp_df_photo.sort_values(['Average Community Rating', 'Number of Ratings'], ascending=False)
    #sp_df_photo_sorted[['Average Community Rating', 'Number of Ratings']]
    #sp_df_photo = sp_df[sp_df.Format == 'Photo']
    ml_cns = sp_df_photo_sorted[['ML Catalog Number']].values.reshape(-1)[:top_limit]

    for ml_cn in ml_cns:

        success = False
        loop_cnt = 0
        img_to_save = '%s/%s' % (jpgdir, target_sp_file.replace('.csv', '_%s.jpg' % ml_cn))

        # 略過已存在照片
        if os.path.isfile(img_to_save):
            success = True
            print('Ignoring %s' % img_to_save)

        max_loop = 5

        while (not success) and (loop_cnt < max_loop) :
            try:
                print('Downloading %s (%d/%d)' % (img_to_save, loop_cnt+1, max_loop))
                r_photo = requests.get('https://cdn.download.ams.birds.cornell.edu/api/v1/asset/%s/1200' % ml_cn)

                with open(img_to_save, 'wb') as img_buff:
                    img_buff.write(r_photo.content)
                print('Success.')
                success = True
            except:
                loop_cnt += 1

