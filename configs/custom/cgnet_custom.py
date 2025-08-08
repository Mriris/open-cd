_base_ = [
    '../_base_/models/cgnet.py',
    './custom_dataset_config.py'
]

crop_size = (256, 256)

model = dict(
    test_cfg=dict(mode='slide', crop_size=crop_size, stride=(crop_size[0]//2, crop_size[1]//2)),
)

# 优化器
optimizer = dict(
    type='AdamW', lr=5e-4, betas=(0.9, 0.999), weight_decay=0.0025)
optim_wrapper = dict(
    _delete_=True,
    type='OptimWrapper',
    optimizer=optimizer) 