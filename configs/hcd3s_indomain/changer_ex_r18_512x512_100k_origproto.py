# 诊断实验：在 Split45 上复刻主表原始实验(2025-09-12)的训练协议。
#
# 背景：附录表 III 的重训值 Changer 61.11 低于主表 62.30。原归因为"open-cd 环境重建"，
# 但残留的原始配置 work_dirs/custom15/changer/changer_custom.py 显示训练协议本身就不同：
#   原始: max_iters=100000, LinearLR warmup(0->1000) + PolyLR(power=1.0, eta_min=0.0)
#   重训: max_iters=40000,  无 warmup, PolyLR(power=0.9, eta_min=1e-4)
# 本配置只把训练量与调度对齐到原始协议，数据集仍用 Split45、仍在 val 上评测，
# 以隔离"训练协议"这一个变量。若 IoU 由 61.11 升到 62.3x，则差异主因是训练协议而非环境。
#
# 其余(batch_size=8、AdamW lr=0.005 wd=0.05、增强管线)原本就与原始配置一致，不改。
_base_ = './changer_ex_r18_512x512_40k.py'

param_scheduler = [
    dict(type='LinearLR', start_factor=1e-6, by_epoch=False, begin=0, end=1000),
    dict(
        type='PolyLR',
        eta_min=0.0,
        power=1.0,
        begin=1000,
        end=100000,
        by_epoch=False),
]

train_cfg = dict(type='IterBasedTrainLoop', max_iters=100000, val_interval=4000)

default_hooks = dict(
    checkpoint=dict(
        type='CheckpointHook', by_epoch=False, interval=4000, save_best='mIoU'))
