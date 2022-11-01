
### Ｋey Modify Point:
- MAE(2022.03)
  - Modigy from multi node, gpu to single node/gpu
    - Turn off "distributed computing"  
  - Launching amp(Automatic Mixed Precision) on pretrain 
    - Turn on "gradient clipping" to prevent gradient vanishing and exploding (i.e. Loss NaN)
- MAE_VSC(Masked Autoencoders with Variational Sparse Coding, 2022.09)
  - Add restrictions on the distribution of latent vectors (Sparse Coding)
  - `models_mae_vsc.py`, `main_pretrain_vsc.py`, `engine_pretrain_vsc.py`

### Model
#### Masked Autoencoders
- [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377)
- [MAE Github](https://github.com/facebookresearch/mae)


### Training log
- MAE
  - MAE修改與訓練筆記
    - Training Note : [Masked Autoencoders(MAE) Model Training Notes](https://hackmd.io/@YungHuiHsu/BJFcW5L49)
  - 論文閱讀筆記 
    - Paper Note : [Masked Autoencoders(MAE) paper reading note](https://hackmd.io/@YungHuiHsu/HJB2yXV75)\
- MAE_VSC
  - MAE_VSC修改與訓練筆記
    - Training Note : Training log of MAE_VSC(Masked Autoencoders with Variational Sparse Coding) ](https://hackmd.io/@YungHuiHsu/ByIooeufi)
  - 論文閱讀筆記 
    - Paper Note : [Variational Sparse Coding (VSC)論文筆記](https://hackmd.io/@YungHuiHsu/HJN5IL2gs)
  - 訓練紀錄(使用Wandb平台) 
    - [Training log on Wandb](https://wandb.ai/yunghui/MAE_VSC_eBird)


### Visualization & Exploring
- Note
  - 利用eBird資料探討全球鳥類功能性特徵與型態多樣性(with MAE Model)
    - [Using Ebird data to explore the functional characteristics and morphological diversity of birds worldwide(with MAE Model)](https://hackmd.io/@YungHuiHsu/Hycb0ScU9)
- Notebook for visualiztion in : [`mae/embed_explore.ipynb`](https://github.com/YunghuiHsu/ebird_project/blob/main/mae/embed_explore.ipynb)

#### Confirm model focus areas
- XAI for Vision Transormer `MAE_explainability.ipynb`
- Attribute(LPR) x Graidient approach
  - reference : [CVPR 2021] [Official PyTorch implementation for Transformer Interpretability Beyond Attention Visualization, a novel method to visualize classifications by Transformer based networks.](https://arxiv.org/abs/2012.09838)

#### Explore the relationship between appearance features and family
- Training simple linear classifier `train_family_classifier.ipynb` 
  ##### Graidient approach 
  - `findKeyFeatures.ipynb`
  ##### Attribute(LPR) x Graidient approach 
  - `findKeyFeatures_Relevance_Grad.ipynb`
    
 
