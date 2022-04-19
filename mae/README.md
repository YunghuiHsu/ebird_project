
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
- https://hackmd.io/@YungHuiHsu/BJFcW5L49
