# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# --------------------------------------------------------
# References:
# DeiT: https://github.com/facebookresearch/deit
# BEiT: https://github.com/microsoft/unilm/tree/master/beit
# --------------------------------------------------------
import argparse
import datetime
import json
from random import sample
import numpy as np
import pandas as pd
import os
import time
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn
from torch.utils.tensorboard import SummaryWriter
import torchvision.transforms as transforms
from torchvision.transforms import InterpolationMode
import torchvision.datasets as datasets

import timm
assert timm.__version__ == "0.3.2"  # version check
import timm.optim.optim_factory as optim_factory

import util.misc as misc
from util.misc import NativeScalerWithGradNormCount as NativeScaler
from util.datasets import ImageDatasetFromFile

import models_mae_vsc

from engine_pretrain_vsc import train_one_epoch
import wandb

def get_args_parser():
    parser = argparse.ArgumentParser('MAE_VSC pre-training', add_help=False)
    parser.add_argument('--batch_size', default=64, type=int,
                        help='Batch size per GPU (effective batch size is batch_size * accum_iter * # gpus')
    parser.add_argument('--epochs', default=400, type=int)
    parser.add_argument('--accum_iter', default=1, type=int,
                        help='Accumulate gradient iterations (for increasing the effective batch size under memory constraints)')

    # Model parameterspip install wandb
    parser.add_argument('--model', default='mae_vit_large_patch16', type=str, metavar='MODEL',
                        help='Name of model to train')
    parser.add_argument('--input_size', default=224, type=int,
                        help='images input size')
    parser.add_argument('--mask_ratio', default=0.75, type=float,
                        help='Masking ratio (percentage of removed patches).')
    parser.add_argument('--norm_pix_loss', action='store_true',
                        help='Use (per-patch) normalized pixels as targets for computing loss')
    parser.set_defaults(norm_pix_loss=False)

    # Optimizer parameters
    parser.add_argument('--weight_decay', type=float, default=0.05,
                        help='weight decay (default: 0.05)')
    parser.add_argument('--lr', type=float, default=None, metavar='LR',
                        help='learning rate (absolute lr)')
    parser.add_argument('--blr', type=float, default=1.5e-5, metavar='LR',
                        help='base learning rate: absolute_lr = base_lr * total_batch_size / 256')
    parser.add_argument('--min_lr', type=float, default=0., metavar='LR',
                        help='lower lr bound for cyclic schedulers that hit 0')
    parser.add_argument('--warmup_epochs', type=int, default=40, metavar='N',
                        help='epochs to warmup LR')
    
    # Dataset parameters
    parser.add_argument('--data_path', default='/datasets01/imagenet_full_size/061417/', type=str,
                        help='dataset path')
    parser.add_argument('--output_dir', default='./output_dir',
                        help='path where to save, empty for no saving')
    parser.add_argument('--log_dir', default='./output_dir',
                        help='path where to tensorboard log')
    parser.add_argument('--data_files', default="log_mae_vsc.txt", type=str,
                    help='name of log files')
    parser.add_argument('--device', default='cuda',
                        help='device to use for training / testing')
    parser.add_argument('--seed', default=0, type=int)
    parser.add_argument('--resume', default='',
                        help='resume from checkpoint')

    parser.add_argument('--start_epoch', default=0, type=int, metavar='N',
                        help='start epoch')
    parser.add_argument('--num_workers', default=10, type=int)
    parser.add_argument('--pin_mem', action='store_true',
                        help='Pin CPU memory in DataLoader for more efficient (sometimes) transfer to GPU.')
    parser.add_argument('--no_pin_mem', action='store_false', dest='pin_mem')
    parser.set_defaults(pin_mem=True)

    # distributed training parameters
    parser.add_argument('--world_size', default=1, type=int,
                        help='number of distributed processes')
    parser.add_argument('--local_rank', default=-1, type=int)
    parser.add_argument('--dist_on_itp', action='store_true')
    parser.add_argument('--dist_url', default='env://',
                        help='url used to set up distributed training')
    parser.add_argument('--distributed', action='store_true')
    parser.add_argument('--amp', action='store_true', default=False)
    parser.add_argument('--clip_grad', default=None)
    
    # vsc parameters
    parser.add_argument('--alpha', type=float, default=1e-2, metavar='ALPHA',
                    help='Sparcity of latent space')
    # parser.add_argument('--weight_rec', type=float, default=1.0,
    #                 help='weigth of reconstruction loss')
    parser.add_argument('--weight_prior', type=float, default=5e-3,
                    help='weigth of prior loss')
    return parser


def main(args):
    
    if not args.amp:
        args.batch_size = 200
        args.accum_iter = 21
    
    misc.init_distributed_mode(args)
    
    v_model = f'MAE_VSC'
    v_model += f'(A{args.alpha}_Wp{str(args.weight_prior)}_Lr{str(args.blr)})'
    v_model += f'_Npl({str(args.norm_pix_loss)[0]})_Amp({str(args.amp)[0]})'
    print(v_model)

    print('job dir: {}'.format(os.path.dirname(os.path.realpath(__file__))))
    print("{}".format(args).replace(', ', ',\n'))

    device = torch.device(args.device)

    # fix the seed for reproducibility
    seed = args.seed + misc.get_rank()
    torch.manual_seed(seed)
    np.random.seed(seed)

    cudnn.benchmark = True
    
    
    # --------------Initialize logging------------
    wandb_logger = wandb.init(
        project='MAE_VSC_eBird', resume='allow')
    argparse_log = vars(args)    # save argparse.Namespace into dictionary
    wandb_logger.config.update(argparse_log)
    # --------------Initialize logging------------

    # simple augmentation
    transform_train = transforms.Compose([
            transforms.RandomResizedCrop(args.input_size, scale=(0.2, 1.0), interpolation=3),  # 3 is bicubic
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    #dataset_train = datasets.ImageFolder(os.path.join(args.data_path), transform=transform_train)
    if args.data_path.endswith('csv') :
        df = pd.read_csv(args.data_path)
        file_paths = [v for (i, v) in df.itertuples()]
        labels = [Path(path).parent.name for path in file_paths]
        dataset_train = ImageDatasetFromFile(file_paths, labels=labels, transform=transform_train)
    else:
        dataset_train = datasets.ImageFolder(os.path.join(args.data_path, 'train'), transform=transform_train)
    print(dataset_train)

    if args.distributed:
        num_tasks = misc.get_world_size()
        global_rank = misc.get_rank()
        sampler_train = torch.utils.data.DistributedSampler(
            dataset_train, num_replicas=num_tasks, rank=global_rank, shuffle=True
        )
        print("Sampler_train = %s" % str(sampler_train))
    else:
        sampler_train = torch.utils.data.RandomSampler(dataset_train)
        global_rank = 0

    if global_rank == 0 and args.log_dir is not None:
        os.makedirs(args.log_dir, exist_ok=True)
        log_writer = SummaryWriter(log_dir=args.log_dir)
    else:
        log_writer = None

    data_loader_train = torch.utils.data.DataLoader(
        dataset_train, sampler=sampler_train,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        pin_memory=args.pin_mem,
        drop_last=True,
    )
    
    # Validate Reconstruction Imgs(optional)----------------
    dir_valid = Path('valid_benchmarks')
    dir_valid.mkdir(parents=True, exist_ok=True)
    valid_list = [str(path) for path in dir_valid.glob('*.jpg')]
    try:
        assert valid_list != [], f'Check whether {dir_valid} has imgs'
    except:
        print(f'If you want check Reconstruction imgs, Plz put benchmark imgs in {dir_valid}')
    
    transform_val = transforms.Compose([
        transforms.Resize(256, interpolation=InterpolationMode.BILINEAR),
        transforms.CenterCrop((224,224)),
        transforms.ToTensor()])
    dataset_val = ImageDatasetFromFile(valid_list, transform=transform_val)
    data_loader_val = torch.utils.data.DataLoader(dataset_val, 
                                                  batch_size=len(dataset_val), shuffle=False, drop_last=False, pin_memory=True)
    val_imgs = next(iter(data_loader_val)).to(device)
    
    root_rec = args.output_dir/Path('rec_results')
    root_rec.mkdir(parents=True, exist_ok=True)
        # ----------------
    
    # define the model
    model = models_mae_vsc.__dict__[args.model](norm_pix_loss=args.norm_pix_loss, alpha=args.alpha)

    model.to(device)

    model_without_ddp = model
    # print("Model = %s" % str(model_without_ddp))

    eff_batch_size = args.batch_size * args.accum_iter * misc.get_world_size()
    
    if args.lr is None:  # only base_lr is specified
        args.lr = args.blr * eff_batch_size / 256

    print("base lr: %.2e" % (args.lr * 256 / eff_batch_size))
    print("actual lr: %.2e" % args.lr)

    print("accumulate grad iterations: %d" % args.accum_iter)
    print("effective batch size: %d" % eff_batch_size)

    if args.distributed:
        model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[args.gpu], find_unused_parameters=True)
        model_without_ddp = model.module
    
    # following timm: set wd as 0 for bias and norm layers
    param_groups = optim_factory.add_weight_decay(model_without_ddp, args.weight_decay)
    optimizer = torch.optim.AdamW(param_groups, lr=args.lr, betas=(0.9, 0.95))#, eps=1e-4)
    loss_scaler = NativeScaler(init_scale=65536.0, growth_factor=2, growth_interval=2000)

    misc.load_model(args=args, model_without_ddp=model_without_ddp, optimizer=optimizer, loss_scaler=loss_scaler)
    print(optimizer)
    
    print(f"Start training for {args.epochs} epochs")
    start_time = time.time()
    for epoch in range(args.start_epoch, args.epochs):
        model.train()
        model.c = 50 + epoch * model.c_delta
        if args.distributed:
            data_loader_train.sampler.set_epoch(epoch)
        rec_save_path = root_rec/f'Rec_{v_model}_E{epoch:04d}.jpg'
        train_stats = train_one_epoch(
            model, data_loader_train,
            optimizer, device, epoch, loss_scaler,
            log_writer=log_writer,
            val_imgs=val_imgs, wandb_logger=wandb_logger, rec_save_path=rec_save_path,
            args=args
        )
        if args.output_dir and (epoch % 1 == 0 or epoch + 1 == args.epochs):
            misc.save_model(
                args=args, model=model, model_without_ddp=model_without_ddp, optimizer=optimizer,
                loss_scaler=loss_scaler, epoch=epoch)

        log_stats = {**{f'train_{k}': v for k, v in train_stats.items()},
                        'epoch': epoch,}

        if args.output_dir and misc.is_main_process():
            if log_writer is not None:
                log_writer.flush()
            with open(os.path.join(args.output_dir, args.data_files), mode="a", encoding="utf-8") as f:
                f.write(json.dumps(log_stats) + "\n")
               

        # --------------Store parameters to wandb histograms-----
        if epoch % 10 == 0:
            histograms = {}
            for tag, value in model.named_parameters():
                tag = tag.replace('/', '.')
                histograms['Weights/' + tag] = wandb.Histogram(value.data.cpu())
                # histograms['Gradients/' + tag] = wandb.Histogram(value.grad.data.cpu())
            wandb_logger.log({**histograms}, commit=False)
                # save logs
                
        wandb_logger.log({
            'epoch': epoch,
            'loss_rec':  train_stats['loss_rec'],
            'loss_prior': train_stats['loss_prior'],
            'learning rate_Encoder': optimizer.param_groups[0]['lr'],
            # 'images': wandb.Image(rec_imgs_train, caption="1st row: Real, 2nd row: Rec, 3nd row: Fake"),
            # **histograms
        })
        
    total_time = time.time() - start_time
    total_time_str = str(datetime.timedelta(seconds=int(total_time)))
    print('Training time {}'.format(total_time_str))


if __name__ == '__main__':
    args = get_args_parser()
    args = args.parse_args()
    if args.output_dir:
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    main(args)
