# HCD-3S 域内(in-domain)多 seed 方差评测 common 配置
# 回应第二轮审稿意见 2：在主 HCD-3S 划分上报告多随机种子的 mean±std。
# 与跨区域配置(standard_512x512_40k_hcd3s_xiongan.py)的唯一区别是 data_root
# 指向主表所用的 Split45（train/val/test 同 GOLD），其余协议完全一致。
# A=光学 T1, B=SAR T2 当双时相输入；label {0,255} -> {0,1}；评测在原生 512 整图。
_base_ = './standard_512x512_40k_levircd.py'

dataset_type = 'LEVIR_CD_Dataset'
data_root = '/data/jingwei/yantingxuan/Datasets/CityCN/Split45'

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
