_base_ = [
    '../_base_/models/fc_siam_conc.py',
    './custom_dataset_config.py'
]

crop_size = (256, 256)

# 优化器
optimizer = dict(
    type='AdamW', lr=0.001, betas=(0.9, 0.999), weight_decay=0.05)
optim_wrapper = dict(
    _delete_=True,
    type='OptimWrapper',
    optimizer=optimizer) 