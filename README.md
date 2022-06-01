# ebird_project

### Project Objective
透過深度學習演算法萃取出鳥類型態的高階抽象特徵，探討鳥類功能性特徵與環境(緯度、海拔)的關聯性  

Extracting high-level abstract features of bird through deep learning algorithms to explore the correlation between functional traits of birds and environment (latitude, altitude)

### Model 
#### Masked Autoencoders
- [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377)
- [Github](https://github.com/facebookresearch/mae)
- Note
  - Training Note : [Masked Autoencoders(MAE) Model Training Notes](https://hackmd.io/@YungHuiHsu/BJFcW5L49)
  - Paper Note : [Masked Autoencoders(MAE) paper reading note](https://hackmd.io/@YungHuiHsu/HJB2yXV75)


### Dataset:
- Training dataset:
  - ebird
    - web scrape from [ebird](https://ebird.org)
    - ranked top 100 from user per species
    - total species:  
    - total imgs:
- Finetune and linprobe dataset:
  - [iNaturelist 2021](https://github.com/visipedia/inat_comp/tree/master/2021)
- Note   
  - [Ebird Data Processing Notes](https://hackmd.io/@YungHuiHsu/ryAfJpDN5)

### Visualization & Exploring
- Note
  - [Using Ebird data to explore the functional characteristics and morphological diversity of birds worldwide](https://hackmd.io/@YungHuiHsu/Hycb0ScU9)
- Notebook for visualiztion in : `visual_mae.ipynb`
