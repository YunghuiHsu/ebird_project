
### Modify point:
- Modigy from multi node,gpu to single node/gpu
  - Turn off "distributed computing"  
- Launching amp(Automatic Mixed Precision) on pretrain 
  - Turn on "gradient clipping" to prevent gradient vanishing and exploding (i.e. Loss NaN)
- Add restrictions on the distribution of latent vectors (Sparse Coding)
  - 2022.09
  - refer : 
    - [Variational Sparse Coding (VSC)論文筆記](https://hackmd.io/@YungHuiHsu/HJN5IL2gs)
    - [Training log of MAE_VSC(Masked Autoencoders with Variational Sparse Coding) 修改與訓練筆記](https://hackmd.io/@YungHuiHsu/ByIooeufi)
  - `models_mae_vsc.py`, `main_pretrain_vsc.py`, `engine_pretrain_vsc.py`

### Model
#### Masked Autoencoders
- [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377)
- [MAE Github](https://github.com/facebookresearch/mae)


### Training log
- Note
  - Training Note : [Masked Autoencoders(MAE) Model Training Notes](https://hackmd.io/@YungHuiHsu/BJFcW5L49)
  - Paper Note : [Masked Autoencoders(MAE) paper reading note](https://hackmd.io/@YungHuiHsu/HJB2yXV75)
- Web 
  - [Training log on Wandb](https://wandb.ai/yunghui/MAE_VSC_eBird)


### Visualization & Exploring
- Note
  - [Using Ebird data to explore the functional characteristics and morphological diversity of birds worldwide](https://hackmd.io/@YungHuiHsu/Hycb0ScU9)
- Notebook for visualiztion in : [`mae/embed_explore.ipynb`](https://github.com/YunghuiHsu/ebird_project/blob/main/mae/embed_explore.ipynb)

#### Confirm model focus areas
- XAI for Transormer `MAE_explainability.ipynb`
- Attribute(LPR) x Graidient approach
  - reference : [CVPR 2021] [Official PyTorch implementation for Transformer Interpretability Beyond Attention Visualization, a novel method to visualize classifications by Transformer based networks.](https://arxiv.org/abs/2012.09838)

#### Explore the relationship between appearance features and family
- Training simple linear classifier `train_family_classifier.ipynb` 
  ##### Graidient approach 
  - `findKeyFeatures.ipynb`
  ##### Attribute(LPR) x Graidient approach 
  - `findKeyFeatures_Relevance_Grad.ipynb`
    
 
