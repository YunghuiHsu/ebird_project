# eBird_project

### Project Objective
透過深度學習演算法萃取出鳥類型態的高階抽象特徵，探討鳥類功能性特徵與環境(緯度、海拔)的關聯性  

Extracting high-level abstract features of bird through deep learning algorithms to explore the correlation between functional traits of birds and environment (latitude, altitude)

### Model 
#### Masked Autoencoders
- [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377)
- [Github](https://github.com/facebookresearch/mae)

### Dataset:
- Training dataset:
  - ebird
    - web scrape from [ebird](https://ebird.org)
    - select top 100 by user ratineg per species
    - total species:  
    - total imgs:
- Finetune and linprobe dataset:
  - [iNaturelist 2021](https://github.com/visipedia/inat_comp/tree/master/2021)
- Note   
  - [Ebird Data Processing Notes](https://hackmd.io/@YungHuiHsu/ryAfJpDN5)

### Visualization & Exploring
- Note
  - [Using Ebird data to explore the functional characteristics and morphological diversity of birds worldwide](https://hackmd.io/@YungHuiHsu/Hycb0ScU9)
- Notebook for visualiztion in : [`mae/visual_mae.ipynb`](https://github.com/YunghuiHsu/ebird_project/blob/main/mae/visual_mae.ipynb)
- [Traning log Visualization on Wandb](https://wandb.ai/yunghui/MAE_VSC_eBird)
