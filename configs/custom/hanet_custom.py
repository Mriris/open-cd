_base_ = [
    '../_base_/models/hanet.py', 
    './custom_dataset_config.py']

# 内存优化配置 - 可根据GPU内存调整
# 选项1: 较小内存占用 (推荐用于内存不足时)
# crop_size = (256, 256)  # 减小图像尺寸以降低内存使用
# batch_size = 2  # 减小batch size

# 选项2: 中等内存占用 (注释掉选项1，启用此选项)
# crop_size = (384, 384)
# batch_size = 4

# 选项3: 原始配置 (最大内存占用，注释掉选项1，启用此选项)
crop_size = (512, 512)
batch_size = 2  # 即使512x512也需要减小batch_size

model = dict(
    decode_head=dict(num_classes=2),
    # test_cfg=dict(mode='slide', crop_size=crop_size, stride=(crop_size[0]//2, crop_size[1]//2)),
)

train_pipeline = [
    dict(type='MultiImgLoadImageFromFile'),
    dict(type='MultiImgLoadAnnotations'),
    dict(type='MultiImgRandomRotate', prob=0.5, degree=180),
    dict(type='MultiImgRandomCrop', crop_size=crop_size, cat_max_ratio=0.75),
    dict(type='MultiImgRandomFlip', prob=0.5, direction='horizontal'),
    dict(type='MultiImgRandomFlip', prob=0.5, direction='vertical'),
    dict(
        type='MultiImgPhotoMetricDistortion',
        brightness_delta=10,
        contrast_range=(0.8, 1.2),
        saturation_range=(0.8, 1.2),
        hue_delta=10),
    dict(type='MultiImgPackSegInputs')
]

# 重写数据加载器配置以使用优化的batch_size
train_dataloader = dict(
    batch_size=batch_size,
    dataset=dict(pipeline=train_pipeline))

# 优化器 - 根据batch_size调整学习率
base_lr = 0.01
adjusted_lr = base_lr * batch_size / 8  # 按batch_size比例调整学习率
optimizer = dict(
    type='SGD', lr=adjusted_lr, momentum=0.9, weight_decay=0.0005)
optim_wrapper = dict(
    _delete_=True,
    type='OptimWrapper',
    optimizer=optimizer)

# 添加GPU内存管理选项
# 如果仍然遇到内存问题，可以启用下面的设置
# import os
# os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True' 