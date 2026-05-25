# TTP (SAM ViT-L tuning) - 继承官方 LEVIR config, 换数据集为 HCD-3S->雄安 512,
# 并把官方 300 epoch 改为 40k iteration (与其它 baseline 对齐, 控成本)
_base_ = ['../ttp/ttp_vit-sam-l_512x512_300e_levircd.py']

data_root = '/mnt/data2/jingwei/yantingxuan/0Program/HeteCD2GOLD/datasets/data/rebuttal_splits/expB_xiongan_512'
test_pipeline = [
    dict(type='MultiImgLoadImageFromFile'),
    dict(type='MultiImgLoadAnnotations'),
    dict(type='MultiImgPackSegInputs')
]
# 保留 TTP 的 bs2 与其 train_pipeline(已是512), 仅换 data_root
train_dataloader = dict(dataset=dict(type='LEVIR_CD_Dataset', data_root=data_root))
val_dataloader = dict(batch_size=1, num_workers=2,
    dataset=dict(type='LEVIR_CD_Dataset', data_root=data_root, pipeline=test_pipeline))
test_dataloader = dict(batch_size=1, num_workers=2,
    dataset=dict(type='LEVIR_CD_Dataset', data_root=data_root, pipeline=test_pipeline))

# 300 epoch -> 40k iteration
train_cfg = dict(_delete_=True, type='IterBasedTrainLoop', max_iters=40000, val_interval=4000)
param_scheduler = [
    dict(type='LinearLR', start_factor=1e-4, by_epoch=False, begin=0, end=1000),
    dict(type='PolyLR', power=1.0, begin=1000, end=40000, eta_min=0.0, by_epoch=False),
]
val_evaluator = dict(type='mmseg.IoUMetric', iou_metrics=['mFscore', 'mIoU'])
test_evaluator = val_evaluator
default_hooks = dict(
    timer=dict(type='IterTimerHook'),
    logger=dict(type='LoggerHook', interval=50, log_metric_by_epoch=False),
    param_scheduler=dict(type='ParamSchedulerHook'),
    checkpoint=dict(type='CheckpointHook', by_epoch=False, interval=4000, save_best='mIoU'),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    visualization=dict(type='CDVisualizationHook', interval=1, img_shape=(512, 512, 3)))
# TTP 冻结 SAM 编码器, 单卡 DDP 需开启
model_wrapper_cfg = dict(type='MMDistributedDataParallel', find_unused_parameters=True)
