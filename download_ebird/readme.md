
- process to download ebirds imgs
- process to clean ebird meta data

# ebird資料處理筆記
###### tags: `ebird` `data` `data_clearing` `data_alignment` `Log`

---
## 資料位置

- [A40]內資料夾路徑: 
    - AI_projects/shared/eBird/download_ebird
        - 目前使用的資料 downloaded/jpg_top100
        - ebird 資料的meta data
            - 完整資料按類群分別放在 downloaded/csv內
                - '學名_編碼'為分類單位
                    - eg : Acanthisitta_chloris_0
                - 約7G、1.82萬份
            - 合併後存放於`meta/meta_all.cs`
            - 與jpg_top100的89萬筆資料關聯(join)後的存放路徑 
                - `AI_projects/shared/eBird/download_ebird/meta/jpg_top100_meta3.csv`
            

## 處理記錄
1. 各分類單位根據使用者排名抓取top100的影像
    - 用者排名依據ebird csv檔裡面的meta資料
        - 'Average Community Rating', 'Number of Ratings'
    - 見`01_get_photos.py`檔
    - 資料存放在downloaded/jpg_100
2. 檢視jpg_100目錄內資料時，發現許多檔案大小小於1kb的資料
    - 在linux terminal 使用以下指令輸出目錄內檔案清單
        - `find downloaded/jpg_top100 -name "*.jpg" -type f -exec ls -l {} \; > jpg_top100.txt`
    - size == 919 byte: 
        - 被伺服器檔下未抓取到
    - 其他size < 1kb:
        - 經檢視後可能因為連結失效而載不到
    - 資料篩選檢視的相關檔案見 `check_problemed.ipynb`
3. 整理出有問題的小檔清單重新抓取資料
    - 篩選標準 size < 1kb 
    - 建立清單後重新抓取，建立資料夾`jpg_reloaded`
        - 見`01_get_photos_reload.py`
        - 抓取時忘了設每個物種抓取排名100張的上限....
    - 合併`jpg_reloaded`與`jpg_100`為`jpg100_1M`
    - 將檔案小於1kb的資料結尾加上`.err` 避免模型訓練時讀入

4. 根據分類單位讀取meta內的使用者排名重新抓取排名前100的照片
    - 見copy_jpg_top100.py
    - 檢視`jpg100_1M`內的資料發現'ML Catalog Number'欄位有重疊
        - 不同物種 
            - 可能物種類群有變更
        - 同一物種但不同流水號編號
            - 可能分屬不同族群與亞種
    - '學名_編碼'為單位選取排名前100的種類
        - 保留重複('ML Catalog Number'數字相同)的照片
    - 建立`jpg_top100`檔案夾
5. 將所有csv格式的meta資料合併為一份，存放於meta/meta_all.csv
    - 單檔7.2G
    - 見`concat_meta_csv.py` 
6. 依目前資料與ebird meta data合併，建立成一份meta data清單
    - 見`get_ebird_meta.ipynb`

7.  參照iNaturalist 2021資料集格式，建立`iNaturalist_2021/val_ebir`資料夾
    - 處理筆記：見`prepare_val_ebird_as_iNat.ipynb`
    - 來源資料集：`/eBird/download_ebird/downloaded/jpg_top10` 的89萬筆資料
    - 探索Embedding時，與iNaturalist 資料比對的eBird驗證資料集
    - n_class = 1486
    - data_size = 1486x10 =14,860

8.  使用eBird資料建立測試資料集`/eBird/download_ebird/downloaded/ebird_testing`
    - 處理筆記：見`establish_Testing_Dataset.ipynb`
    - 來源資料集：`/eBird/download_ebird/downloaded/jpg_top10` 的89萬筆資料
    - Stratified Random Sampling 分層隨機抽樣
        - 每個物種單元按 6:2:2 切分給train, validation, test
    - 資料目錄結構
    ```
    --- ebird_testing
        |___ train/
        |___ val/
        |___ test/
    ```
    - n_class = 9484
    - data_size

        | dir   | data_size | n_class |
        | ----- |:---------:|:-------:|
        | train |  517,894  |  9484   |
        | val   |  172,006  |  9484   |
        | test  |  173,936  |  9484   |
