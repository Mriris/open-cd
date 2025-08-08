_base_ = [
    '../_base_/models/mtkd/mtkd-changer_r18.py',
    './custom_dataset_config.py'
]

crop_size = (512, 512)

# MTKD多教师知识蒸馏框架需要按照以下三个步骤使用：
# 步骤1: 训练原始模型（得到checkpoint_student）
# 步骤2: 根据CAR训练教师模型（得到checkpoint_teacher_l, checkpoint_teacher_m, checkpoint_teacher_s）
# 步骤3: 知识蒸馏训练（本配置文件用于此步骤）
#
# 预训练模型检查点路径（在步骤3时需要设置为前两步训练得到的模型权重）：
# checkpoint_student = 'work_dirs/initial/latest.pth'      # 来自步骤1
# checkpoint_teacher_l = 'work_dirs/large/latest.pth'      # 来自步骤2
# checkpoint_teacher_m = 'work_dirs/medium/latest.pth'     # 来自步骤2  
# checkpoint_teacher_s = 'work_dirs/small/latest.pth'      # 来自步骤2

model = dict(
    # 注释掉预训练权重加载，如需使用请设置上面的检查点路径并取消注释
    # init_cfg=dict(type='Pretrained', checkpoint=checkpoint_student),
    # init_cfg_t_l = dict(type='Pretrained', checkpoint=checkpoint_teacher_l),
    # init_cfg_t_m = dict(type='Pretrained', checkpoint=checkpoint_teacher_m),
    # init_cfg_t_s = dict(type='Pretrained', checkpoint=checkpoint_teacher_s),
    
    backbone=dict(
        interaction_cfg=(
            None,
            dict(type='SpatialExchange', p=1/2),
            dict(type='ChannelExchange', p=1/2),
            dict(type='ChannelExchange', p=1/2))
    ),
    decode_head=dict(
        num_classes=2,
        sampler=dict(type='mmseg.OHEMPixelSampler', thresh=0.7, min_kept=100000)),
)

train_pipeline = [
    dict(type='MultiImgLoadImageFromFile'),
    dict(type='MultiImgLoadAnnotations'),
    dict(type='MultiImgRandomRotFlip', rotate_prob=0.5, flip_prob=0.5, degree=(-20, 20)),
    dict(type='MultiImgRandomCrop', crop_size=crop_size, cat_max_ratio=0.75),
    dict(type='MultiImgExchangeTime', prob=0.5),
    dict(
        type='MultiImgPhotoMetricDistortion',
        brightness_delta=10,
        contrast_range=(0.8, 1.2),
        saturation_range=(0.8, 1.2),
        hue_delta=10),
    dict(type='MultiImgPackSegInputs')
]

train_dataloader = dict(
    dataset=dict(pipeline=train_pipeline))

# 优化器
optimizer = dict(
    type='AdamW', lr=0.005, betas=(0.9, 0.999), weight_decay=0.05)
optim_wrapper = dict(
    _delete_=True,
    type='OptimWrapper',
    optimizer=optimizer) 