# SNUNet

[SNUNet-CD：用于高分辨率图像变化检测的密集连接孪生网络](https://ieeexplore.ieee.org/document/9355573)

## 简介

[官方仓库](https://github.com/likyoo/Siam-NestedUNet)

[代码片段](https://github.com/likyoo/open-cd/blob/main/opencd/models/backbones/snunet.py)

## 摘要
变化检测是遥感图像分析中的一项重要任务。它广泛应用于自然灾害监测和评估、土地资源规划和其他领域。作为一种像素到像素的预测任务，变化检测对原始位置信息的利用非常敏感。最近的变化检测方法总是专注于深层变化语义特征的提取，但忽略了包含高分辨率和细粒度特征的浅层信息的重要性，这往往导致变化目标边缘像素的不确定性和小目标的判断遗漏。在本文中，我们提出了一种用于变化检测的密集连接孪生网络，即SNUNet-CD（孪生网络和NestedUNet的组合）。SNUNet-CD通过编码器和解码器之间以及解码器和解码器之间的紧凑信息传输，减轻了神经网络深层中定位信息的丢失。此外，我们还提出了集成通道注意力模块（ECAM）用于深度监督。通过ECAM，可以提炼不同语义层次的最具代表性特征并用于最终分类。实验结果表明，我们的方法在许多评估标准上都有很大改进，并且在准确性和计算量之间有着比其他最先进的变化检测方法更好的权衡。

<!-- [IMAGE] -->

<div align=center>
<img src="https://user-images.githubusercontent.com/44317497/201501845-da98c364-e0fe-4c75-be8b-f9d207e993f5.png" width="90%"/>
</div>

```bibtex
@ARTICLE{9355573,
  author={S. {Fang} and K. {Li} and J. {Shao} and Z. {Li}},
  journal={IEEE Geoscience and Remote Sensing Letters}, 
  title={SNUNet-CD: A Densely Connected Siamese Network for Change Detection of VHR Images}, 
  year={2021},
  volume={},
  number={},
  pages={1-5},
  doi={10.1109/LGRS.2021.3056416}}
```

## 结果和模型

### LEVIR-CD

| 方法 | 基础通道数 | 裁剪尺寸 | 学习率调度 | 内存 (GB) | 精确率 | 召回率 | F1分数 |  IoU  |                            配置                            | 下载 |
| :----: | :----------: | :-------: | :-----: | :------: | :-------: | :----: | :------: | :---: | :----------------------------------------------------------: | :------: |
| SNUNet |      16      |  256x256  |  40000  |    -     |   92.70   | 90.04  |  91.35   | 84.08 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/snunet/snunet_c16_256x256_40k_levircd.py) |          |


### SVCD

| 方法 | 基础通道数 | 裁剪尺寸 | 学习率调度 | 内存 (GB) | 精确率 | 召回率 | F1分数 |  IoU  |                            配置                            | 下载 |
| :----: | :----------: | :-------: | :-----: | :------: | :-------: | :----: | :------: | :---: | :----------------------------------------------------------: | :------: |
| SNUNet |      16      |  256x256  |  120000  |    -     |   94.69   | 91.90  |  93.27   | 87.40 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/snunet/snunet_c16_256x256_120k_svcd.py) |          |


- 所有指标均基于"变化"类别。
- 所有得分均在测试集上计算。
- 120000次迭代 ~ SVCD数据集中的100个周期
