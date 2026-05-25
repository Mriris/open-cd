# SNUNet (c16) - 复刻 snunet_c16_256x256_40k_levircd, 训练分辨率提到 512, 数据换为 HCD-3S->雄安跨区域
_base_ = [
    '../_base_/models/snunet_c16.py',
    '../common/standard_512x512_40k_hcd3s_xiongan.py']
