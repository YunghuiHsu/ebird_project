# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# --------------------------------------------------------
# References:
# DeiT: https://github.com/facebookresearch/deit
# BEiT: https://github.com/microsoft/unilm/tree/master/beit
# --------------------------------------------------------
import math
import sys
from typing import Iterable

import torch

import util.misc as misc
import util.lr_sched as lr_sched

def train_one_epoch(model: torch.nn.Module,
                    data_loader: Iterable, optimizer: torch.optim.Optimizer,
                    device: torch.device, epoch: int, loss_scaler,
                    log_writer=None,
                    args=None):
    model.train(True)
    metric_logger = misc.MetricLogger(delimiter="  ")
    metric_logger.add_meter('lr', misc.SmoothedValue(window_size=1, fmt='{value:.6f}'))
    metric_logger.add_meter('w_rec', misc.SmoothedValue(window_size=1, fmt='{value:.1f}'))
    metric_logger.add_meter('w_prior', misc.SmoothedValue(window_size=1, fmt='{value:.3f}'))
    # metric_logger.add_meter('loss_total', misc.SmoothedValue(window_size=1, fmt='{value:.6f}'))
    # metric_logger.add_meter('loss_rec', misc.SmoothedValue(window_size=1, fmt='{value:.6f}'))
    # metric_logger.add_meter('loss_prior', misc.SmoothedValue(window_size=1, fmt='{value:.6f}'))

    header = 'Epoch: [{}]'.format(epoch)
    
    print_freq = args.accum_iter
    accum_iter = args.accum_iter

    optimizer.zero_grad()

    if log_writer is not None:
        print('log_dir: {}'.format(log_writer.log_dir))
        
    print(epoch, args.start_epoch)
    is_resume = False
    if epoch == args.start_epoch:
        is_resume = True

    for data_iter_step, (samples, _) in enumerate(metric_logger.log_every(data_loader, print_freq, header)):

        # we use a per iteration (instead of per epoch) lr scheduler
        if (data_iter_step % accum_iter == 0) or is_resume:
            lr_sched.adjust_learning_rate(optimizer, data_iter_step / len(data_loader) + epoch, args)

        samples = samples.to(device, non_blocking=True)

        with torch.cuda.amp.autocast():
            loss_rec, loss_prior, *_ = model(samples, mask_ratio=args.mask_ratio)

        if not math.isfinite(loss_rec.item()):
            print("Loss_rec is {}, stopping training".format(loss_rec.item()))
            sys.exit(1)
        if not math.isfinite(loss_prior.item()):
            print("Loss_prior is {}, stopping training".format(loss_prior.item()))
            sys.exit(1)

        loss_rec /= accum_iter
        loss_prior /= accum_iter
        # loss /= accum_iter
        if epoch <= args.warmup_epochs:
            loss_prior = loss_prior * ((epoch + 1e-7) /  args.warmup_epochs)                      # 0.0 --> 1.0 
            # clip loss_prior to less than loss_rec
            while loss_rec*args.weight_rec < loss_prior*args.weight_prior:
                loss_prior *= 0.1
            
        loss = loss_rec*args.weight_rec + loss_prior*args.weight_prior
            
        loss_scaler(loss, optimizer, parameters=model.parameters(), clip_grad=args.clip_grad,
                    update_grad=(data_iter_step + 1) % accum_iter == 0)
        if (data_iter_step + 1) % accum_iter == 0:
            optimizer.zero_grad()

        torch.cuda.synchronize()
        
        metric_logger.update(w_rec=args.weight_rec)
        metric_logger.update(w_prior=args.weight_prior)
        metric_logger.update(loss_total=loss.item())
        metric_logger.update(loss_rec=loss_rec.item()*args.weight_rec)
        metric_logger.update(loss_prior=loss_prior.item()*args.weight_prior)


        lr = optimizer.param_groups[0]["lr"]
        metric_logger.update(lr=lr)

        loss_value_reduce = misc.all_reduce_mean(loss.item())
        if log_writer is not None and (data_iter_step + 1) % accum_iter == 0:
            """ We use epoch_1000x as the x-axis in tensorboard.
            This calibrates different curves when batch size changes.
            """
            epoch_1000x = int((data_iter_step / len(data_loader) + epoch) * 1000)
            log_writer.add_scalar('train_loss', loss_value_reduce, epoch_1000x)
            log_writer.add_scalar('lr', lr, epoch_1000x)


    # gather the stats from all processes
    metric_logger.synchronize_between_processes()
    print("Averaged stats:", metric_logger)
    return {k: meter.global_avg for k, meter in metric_logger.meters.items()}