# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# --------------------------------------------------------
# References:
# DeiT: https://github.com/facebookresearch/deit
# --------------------------------------------------------

import os
import PIL
import pandas as pd
from torchvision import datasets, transforms
import torch.utils.data as data

from timm.data import create_transform
from timm.data.constants import IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD


def build_dataset(is_train, args):
    transform = build_transform(is_train, args)

    if args.metafile is not None:
        dir_ =  'train' if is_train else 'val'
        df = pd.read_csv(args.metafile, index_col=0)
        print(f'Load "{args.metafile}". Read Labels')
        mask = df.Path.str.startswith(dir_)
        path =  list(args.data_path + '/' + df[mask].Path)
        label_list = list(df[mask].Label)
        dataset = ImageDatasetFromFile(path, label_list, transform=transform)
    else:
        root = os.path.join(args.data_path, 'train' if is_train else 'val')
        dataset = datasets.ImageFolder(root, transform=transform)

    print(dataset)

    return dataset


def build_transform(is_train, args):
    mean = IMAGENET_DEFAULT_MEAN
    std = IMAGENET_DEFAULT_STD
    # train transform
    if is_train:
        # this should always dispatch to transforms_imagenet_train
        transform = create_transform(
            input_size=args.input_size,
            is_training=True,
            color_jitter=args.color_jitter,
            auto_augment=args.aa,
            interpolation='bicubic',
            re_prob=args.reprob,
            re_mode=args.remode,
            re_count=args.recount,
            mean=mean,
            std=std,
        )
        return transform

    # eval transform
    t = []
    if args.input_size <= 224:
        crop_pct = 224 / 256
    else:
        crop_pct = 1.0
    size = int(args.input_size / crop_pct)
    t.append(
        transforms.Resize(size, interpolation=PIL.Image.BICUBIC),  # to maintain same ratio w.r.t. 224 images
    )
    t.append(transforms.CenterCrop(args.input_size))

    t.append(transforms.ToTensor())
    t.append(transforms.Normalize(mean, std))
    return transforms.Compose(t)


class ImageDatasetFromFile(data.Dataset):
    def __init__(self, image_path:list, labels:list,
                input_height=256, input_width=256, output_height=256, output_width=256, transform=None):
        
        super(ImageDatasetFromFile, self).__init__()
                
        self.image_path = image_path
        self.labels = labels
        self.transform = transform
        self.toTensor = transforms.Compose([transforms.ToTensor()])

    def __getitem__(self, index):
        img_ = PIL.Image.open(self.image_path[index]).convert('RGB')
        img = self.toTensor(img_) if self.transform is None else self.transform(img_) 
        label = self.labels[index]
        return img, label 

    def __len__(self):
        return len(self.image_filenames)