
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


#### Explore the relationship between appearance features and family
  - `findKeyFeatures.ipynb`
    - `train_family_classifier.ipynb`
 
