# HCD-3S(train) -> 雄安 XiongAn(val/test) 跨区域泛化 common 配置
# 复用 LEVIR 二值 CD 数据集类 (label {0,255} -> {0,1}); A=光学T1, B=SAR-T2 当双时相 6 通道输入
# 训练沿用 open-cd 512x512 40k 标准增广/schedule; 评测在原生 512 整图(去掉 LEVIR 的 1024 resize)
_base_ = './standard_512x512_40k_levircd.py'

dataset_type = 'LEVIR_CD_Dataset'
data_root = '/mnt/data2/jingwei/yantingxuan/0Program/HeteCD2GOLD/datasets/data/rebuttal_splits/expB_xiongan_512'

# 评测: 原生 512, 不做任何 resize (LEVIR 默认 resize 到 1024 会放大我们的 512 切片)
test_pipeline = [
    dict(type='MultiImgLoadImageFromFile'),
    dict(type='MultiImgLoadAnnotations'),
    dict(type='MultiImgPackSegInputs')
]

train_dataloader = dict(
    dataset=dict(type=dataset_type, data_root=data_root))
val_dataloader = dict(
    dataset=dict(type=dataset_type, data_root=data_root, pipeline=test_pipeline))
test_dataloader = dict(
    dataset=dict(type=dataset_type, data_root=data_root, pipeline=test_pipeline))

# 可视化 hook 的画布尺寸对齐到 512(原默认 1024 针对 LEVIR)
default_hooks = dict(
    visualization=dict(type='CDVisualizationHook', interval=1,
                       img_shape=(512, 512, 3)))
