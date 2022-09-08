
### Modify point:
- Modigy from multi node,gpu to single node/gpu
  - Turn off "distributed computing"  
- Launching amp(Automatic Mixed Precision) on pretrain 
  - Turn on "gradient clipping" to prevent gradient vanishing and exploding (i.e. Loss NaN)

### Model
#### Masked Autoencoders
- [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377)
- [MAE Github](https://github.com/facebookresearch/mae)


### Training log
- Note
  - Training Note : [Masked Autoencoders(MAE) Model Training Notes](https://hackmd.io/@YungHuiHsu/BJFcW5L49)
  - Paper Note : [Masked Autoencoders(MAE) paper reading note](https://hackmd.io/@YungHuiHsu/HJB2yXV75)


### Visualization & Exploring
- Note
  - [Using Ebird data to explore the functional characteristics and morphological diversity of birds worldwide](https://hackmd.io/@YungHuiHsu/Hycb0ScU9)
- Notebook for visualiztion in : [`mae/visual_mae.ipynb`](https://github.com/YunghuiHsu/ebird_project/blob/main/mae/visual_mae.ipynb)

#### Confirm model focus areas
- XAI for Transormer
- Attribute(LPR) x Graidient approach
  - [CVPR 2021] [Official PyTorch implementation for Transformer Interpretability Beyond Attention Visualization, a novel method to visualize classifications by Transformer based networks.](https://arxiv.org/abs/2012.09838)

#### Explore the relationship between appearance features and family
- Training simple linear classifier `train_family_classifier.ipynb` 
  ##### Graidient approach 
  - `findKeyFeatures.ipynb`
  ##### Attribute(LPR) x Graidient approach 
  - `findKeyFeatures_Relevance_Grad.ipynb`
    
 
