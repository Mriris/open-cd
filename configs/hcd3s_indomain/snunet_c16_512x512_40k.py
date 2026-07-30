# SNUNet (c16) - 复刻 snunet_c16_256x256_40k_levircd, 训练分辨率提到 512, 数据换为 HCD-3S 域内(Split45)多 seed
_base_ = [
    '../_base_/models/snunet_c16.py',
    '../common/standard_512x512_40k_hcd3s_indomain.py']
