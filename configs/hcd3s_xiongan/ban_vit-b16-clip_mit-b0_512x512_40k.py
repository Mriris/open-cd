# BAN (CLIP ViT-B16 + MiT-b0) - 继承官方 LEVIR 40k config, 仅换数据集为 HCD-3S->雄安 512
_base_ = ['../ban/ban_vit-b16-clip_mit-b0_512x512_40k_levircd.py']

data_root = '/mnt/data2/jingwei/yantingxuan/0Program/HeteCD2GOLD/datasets/data/rebuttal_splits/expB_xiongan_512'
test_pipeline = [
    dict(type='MultiImgLoadImageFromFile'),
    dict(type='MultiImgLoadAnnotations'),
    dict(type='MultiImgPackSegInputs')
]
train_dataloader = dict(dataset=dict(type='LEVIR_CD_Dataset', data_root=data_root))
val_dataloader = dict(dataset=dict(type='LEVIR_CD_Dataset', data_root=data_root, pipeline=test_pipeline))
test_dataloader = dict(dataset=dict(type='LEVIR_CD_Dataset', data_root=data_root, pipeline=test_pipeline))
default_hooks = dict(visualization=dict(type='CDVisualizationHook', interval=1, img_shape=(512, 512, 3)))
# BAN 冻结 CLIP 图像编码器, 单卡 DDP 需开启
model_wrapper_cfg = dict(type='MMDistributedDataParallel', find_unused_parameters=True)
