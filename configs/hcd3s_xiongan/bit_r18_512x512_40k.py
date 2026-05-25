# BiT (ResNet18) - 复刻 bit_r18_256x256_40k_levircd, 训练分辨率提到 512, 数据换为 HCD-3S->雄安跨区域
_base_ = [
    '../_base_/models/bit_r18.py',
    '../common/standard_512x512_40k_hcd3s_xiongan.py']
