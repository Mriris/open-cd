# MTKD step3: 多教师蒸馏 -> 最终 Changer-mit-b0 学生 (全量 HCD-3S train -> 雄安 val)
# 4 个 checkpoint 路径由 run_mtkd.sh 在 step1/step2 完成后用 --cfg-options 注入
_base_ = ['../../_base_/models/mtkd/mtkd-changer_mit-b0.py',
          '../../common/standard_512x512_40k_hcd3s_xiongan.py']

crop_size = (512, 512)
# 占位, 运行时由 --cfg-options 覆盖
checkpoint_student = 'PLACEHOLDER_STUDENT'
checkpoint_teacher_l = 'PLACEHOLDER_TEACHER_L'
checkpoint_teacher_m = 'PLACEHOLDER_TEACHER_M'
checkpoint_teacher_s = 'PLACEHOLDER_TEACHER_S'

model = dict(
    init_cfg=dict(type='Pretrained', checkpoint=checkpoint_student),
    init_cfg_t_l=dict(type='Pretrained', checkpoint=checkpoint_teacher_l),
    init_cfg_t_m=dict(type='Pretrained', checkpoint=checkpoint_teacher_m),
    init_cfg_t_s=dict(type='Pretrained', checkpoint=checkpoint_teacher_s),
    backbone=dict(interaction_cfg=(
        None,
        dict(type='SpatialExchange', p=1 / 2),
        dict(type='ChannelExchange', p=1 / 2),
        dict(type='ChannelExchange', p=1 / 2))),
    decode_head=dict(num_classes=2,
        sampler=dict(type='mmseg.OHEMPixelSampler', thresh=0.7, min_kept=100000)))

train_pipeline = [
    dict(type='MultiImgLoadImageFromFile'),
    dict(type='MultiImgLoadAnnotations'),
    dict(type='MultiImgRandomRotFlip', rotate_prob=0.5, flip_prob=0.5, degree=(-20, 20)),
    dict(type='MultiImgRandomCrop', crop_size=crop_size, cat_max_ratio=0.75),
    dict(type='MultiImgExchangeTime', prob=0.5),
    dict(type='MultiImgPhotoMetricDistortion', brightness_delta=10,
         contrast_range=(0.8, 1.2), saturation_range=(0.8, 1.2), hue_delta=10),
    dict(type='MultiImgPackSegInputs')
]
train_dataloader = dict(dataset=dict(pipeline=train_pipeline))
optimizer = dict(type='AdamW', lr=0.0001, betas=(0.9, 0.999), weight_decay=0.01)
optim_wrapper = dict(_delete_=True, type='OptimWrapper', optimizer=optimizer,
    paramwise_cfg=dict(custom_keys={'pos_block': dict(decay_mult=0.),
        'norm': dict(decay_mult=0.), 'head': dict(lr_mult=10.)}))
# 蒸馏含3个冻结教师, 单卡 DDP 需开启
model_wrapper_cfg = dict(type='MMDistributedDataParallel', find_unused_parameters=True)
