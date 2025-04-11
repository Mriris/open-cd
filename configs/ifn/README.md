# IFN

[一种用于高分辨率双时相遥感图像变化检测的深度监督图像融合网络](https://www.sciencedirect.com/science/article/pii/S0924271620301532)

## 简介

[官方仓库](https://github.com/GeoZcx/A-deeply-supervised-image-fusion-network-for-change-detection-in-remote-sensing-images)

[代码片段](https://github.com/likyoo/open-cd/blob/main/opencd/models/backbones/ifn.py)

## 摘要
高分辨率遥感图像的变化检测对于理解地表变化至关重要。由于传统的变化检测方法不适用于这项任务，考虑到高分辨率图像中所传达的精细图像细节和复杂纹理特征带来的挑战，已经提出了许多基于深度学习的变化检测方法来提高变化检测性能。虽然最先进的基于深度特征的方法优于所有其他基于深度学习的变化检测方法，但现有基于深度特征方法中的网络大多是从最初为单图像语义分割提出的架构修改而来。将这些网络用于变化检测任务仍然存在一些关键问题。在本文中，我们提出了一种用于高分辨率双时相遥感图像变化检测的深度监督图像融合网络（IFN）。具体来说，首先通过全卷积双流架构提取双时相图像的高度代表性深度特征。然后，将提取的深度特征输入到深度监督差异判别网络（DDN）中进行变化检测。为了提高输出变化图中物体的边界完整性和内部紧凑性，通过注意力模块将原始图像的多级深度特征与图像差异特征融合，用于变化图重建。通过直接将变化图损失引入网络的中间层来进一步增强DDN，整个网络以端到端的方式进行训练。IFN应用于一个公开可用的数据集，以及一个由来自Google Earth覆盖中国不同城市的多源双时相图像组成的具有挑战性的数据集。视觉解释和定量评估都证实，与最先进的方法相比，IFN通过返回具有完整边界和高内部紧凑性的变化区域，优于四种从文献中得出的基准方法。

<!-- [IMAGE] -->

<div align=center>
<img src="https://user-images.githubusercontent.com/44317497/215308284-cafb5fa7-0c1f-404e-804b-71dff28e1b63.png" width="90%"/>
</div>

```bibtex
@article{zhang2020deeply,
  title={A deeply supervised image fusion network for change detection in high resolution bi-temporal remote sensing images},
  author={Zhang, Chenxiao and Yue, Peng and Tapete, Deodato and Jiang, Liangcun and Shangguan, Boyi and Huang, Li and Liu, Guangchao},
  journal={ISPRS Journal of Photogrammetry and Remote Sensing},
  volume={166},
  pages={183--200},
  year={2020},
  publisher={Elsevier}
}
```

## 结果和模型

### LEVIR-CD

| 方法 | 骨干网络 | 裁剪尺寸 | 学习率调度 | 内存 (GB) | 精确率 | 召回率 | F1分数 |  IoU  |                            配置                            | 下载 |
| :----: | :------: | :-------: | :-----: | :------: | :-------: | :----: | :------: | :---: | :----------------------------------------------------------: | :------: |
|  IFN   |  vgg16   |  256x256  |  40000  |    -     |   91.17   | 90.51  |  90.83   | 83.21 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ifn/ifn_256x256_40k_levircd.py) |          |


- 所有指标均基于"变化"类别。
- 所有得分均在测试集上计算。
