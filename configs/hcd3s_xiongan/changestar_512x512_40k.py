# changestar - 继承官方 LEVIR config, 仅把数据集换为 HCD-3S(train)->雄安(val) 512 跨区域
_base_ = ['../changestar/changestar_farseg_1x96_512x512_40k_levircd.py']

data_root = '/mnt/data2/jingwei/yantingxuan/0Program/HeteCD2GOLD/datasets/data/rebuttal_splits/expB_xiongan_512'
crop_size = (512, 512)
train_pipeline = [
    dict(type='MultiImgLoadImageFromFile'),
    dict(type='MultiImgLoadAnnotations'),
    dict(type='MultiImgRandomRotate', prob=0.5, degree=180),
    dict(type='MultiImgRandomCrop', crop_size=crop_size, cat_max_ratio=0.75),
    dict(type='MultiImgRandomFlip', prob=0.5, direction='horizontal'),
    dict(type='MultiImgRandomFlip', prob=0.5, direction='vertical'),
    dict(type='MultiImgPhotoMetricDistortion', brightness_delta=10,
         contrast_range=(0.8, 1.2), saturation_range=(0.8, 1.2), hue_delta=10),
    dict(type='MultiImgPackSegInputs')
]
test_pipeline = [
    dict(type='MultiImgLoadImageFromFile'),
    dict(type='MultiImgLoadAnnotations'),
    dict(type='MultiImgPackSegInputs')
]
train_dataloader = dict(dataset=dict(type='LEVIR_CD_Dataset', data_root=data_root, pipeline=train_pipeline))
val_dataloader = dict(dataset=dict(type='LEVIR_CD_Dataset', data_root=data_root, pipeline=test_pipeline))
test_dataloader = dict(dataset=dict(type='LEVIR_CD_Dataset', data_root=data_root, pipeline=test_pipeline))
default_hooks = dict(visualization=dict(type='CDVisualizationHook', interval=1, img_shape=(512, 512, 3)))
# 单卡 DDP: 部分模型(IFN深监督/HANet/ChangeStar多任务等)有未参与loss的参数, 需开启
model_wrapper_cfg = dict(type='MMDistributedDataParallel', find_unused_parameters=True)
