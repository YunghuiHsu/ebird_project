- Pipeline to get and preprocess 'iNaturalist_2021_dataset'


- Data Source
  - [iNaturalist 2021 Dataset](https://github.com/visipedia/inat_comp/tree/master/2021)  

  - There is a total of 10,000 species in the dataset. The full training dataset contains nearly 2.7M images.  
  - To make the dataset more accessible we have also created a "mini" training dataset with 50 examples per species for a total of 500K images.
      - Each species has 10 validation images. There are a total of 500,000 test images.
  - For bird:
    - 1486 sp.
      - 1486 x10 imgs/per sp in val dataset

- Data Storage
  - server : A40
  - AI_projects/shared/iNaturalist_2021/
  - `wget ${file link}`

## Untar(filter) bird imgs
### check data structure in compressed Directory
- Untaring the images creates a directory structure like train/category/image.jpg.
- Untaring imgs by (birds) directory
    - filter directory name include "aves", then untar it by keywaord

    - Check how many files contains "Aves"
        - `tar -tvf file.tar.gz |grep Aves`
    - Check how many directory contains "Aves"
        - `tar -tvf file.tar.gz |grep Aves | grep -vc jpg`

    - untar specific files
        - `tar -zxvf file.tar.gz --wildcards "*Aves*"`
    - [UNIX/Linux 檔案壓縮與備份工具 tar 指令使用教學與範例（一）：tar 檔案](https://blog.gtwang.org/linux/tar-command-examples-in-linux-1/)

- if moving bigfiles between server needed:
  - tar-split, then concat-untar
    - tar big files and split into small files
      - `tar -zcvf -  big_demo | split -b 4G -d -a 2 - big_demo.tar.gz_part`
    - concat small files to original big files and untar it
      -  `cat big_demo.tar.gz_part* | tar -zxvf - `
  - [[Linux] tar/gzip 檔案壓縮與解壓縮、split/cat檔案分割與合併的實務應用](https://www.jinnsblog.com/2018/03/linux-tar-and-split-cat-example.html)


---
## Convert the json files to easy-to-use csv files

### 1. Check data structure in jason files
- 'info',  'licenses', is removable
- 'categories' is repeated/sharable
- 'annotations' 
    - Provides information about 'image_id' linked to 'category_id' (which contain taxon information)
    - 'annotations' is lack of in 'public_test.json'
        - public test image don't have taxon information

### 2. Establish a shared 'categories' dataframe/csv file
- all sps
- only avian

### 3. Establish the Avian metadata
- join 'images' and 'categories' by 'annotations'
- include: 'train.json', 'train_mini.json', 'val.json'
