# 引入 requests 模組
import requests
import json
import pandas as pd
import numpy as np
from io import StringIO
import os
from touch_dir import touch_dir

import argparse
# 從命令列讀參數，指定 target 類群下載對應的 csv
# 執行命令如下，選定裝有科屬種的 txt，即會下載物種的 csv
# 亞階層會由 ebird api 自動回傳，txt 中請勿列出亞種，才不會造成資料重複
# python 00_get_target_csv.py --target_file="./target_list/Tyrannidae.txt"

parser = argparse.ArgumentParser()
parser.add_argument('--target_file', default="./target_list/Thraupidae.txt", type=str, help='target data to be fetched')
opt = parser.parse_args()

target_file = opt.target_file
assert(os.path.isfile(target_file))

def enum_target_species(target_file):
    target = os.path.splitext(os.path.basename(target_file))[0]
    touch_dir('./downloaded/csv/%s' % target)
    csv_data = pd.read_csv(target_file, header=None)
    csv_data.rename({0: 'name'}, axis=1, inplace=True)
    for name in csv_data.name.values:
        name_parts = name.strip().split(' ')
        if len(name_parts) > 1:
            if name_parts[0] == 'Family':
                target = name_parts[1]
                touch_dir('./downloaded/csv/%s' % target)
                continue
            else:
                yield target, name
        else:
            continue
    yield None, None

# 使用 GET 方式下載普通網頁
# 自訂表頭
# my_headers = {'user-agent': 'my-app/0.0.1'}
targets = []
mcllib_cookies = dict(PIZOTE_SESSIONID='A2738B1C866B03C3C071F7A214D9C95C')
for target, name in enum_target_species(target_file):

    if name is not None:
        print([target, name])
        targets.append(target)
        # 查詢參數
        # 這邊 key 是直接從瀏覽器端幹來的，有可能會 expired
        ebird_api_params = dict(
            q = name,
            key = 'jfekjedvescr')

        # 將 params and headers 加入 GET 請求中 (using 'data' for POST method; using tuples instead of dict for duplicated vars)
        r = requests.get('https://ebird.org/ws2.0/ref/taxon/find', params=ebird_api_params)#, headers = my_headers, auth=('user', 'pass'))
        if r.status_code == requests.codes.ok:
            
            print("OK")

            intermed = json.loads(r.text)

            for i in range(len(intermed)):
                params_for_csv = dict(taxonCode=intermed[i]['code'], q=intermed[i]['name'], mediaType='p')
                r_csv = requests.get('https://search.macaulaylibrary.org/catalog.csv', params=params_for_csv, cookies=mcllib_cookies)
                #r_csv.text
                with open('./downloaded/csv/%s/%s_%d.csv' % (target, name.replace(' ', '_'), i), 'w', encoding='utf-8') as sp_csv:
                    sp_csv.write(r_csv.text)

        else:
            print(r.status_code)
            print(r.text)

    else:
        print('Finished')


# unique_targets = np.unique(targets)
# total_sum = 0
# # calc num of photos of picked target
# for target in unique_targets:
#     print(target)
#     num_of_photos = 0
#     for target_sp_file in os.listdir('./downloaded/csv/%s' % target):
#         if not target_sp_file.endswith('.csv'):
#             continue
#         sp_df = pd.read_csv('./downloaded/csv/%s/%s' % (target, target_sp_file))
#         sp_df_photo = sp_df[sp_df.Format == 'Photo']
#         num_of_photos += sp_df_photo.shape[0]

#     print ('Num of photos in %s: %d' % (target, num_of_photos))
#     total_sum += num_of_photos

# print ('Total num of photos : %d' % (total_sum))