# HANet

[HANet: 一种用于双时相超高分辨率遥感图像变化检测的层次注意力网络](https://ieeexplore.ieee.org/abstract/document/10093022)

## 简介

[官方仓库](https://github.com/ChengxiHAN/HANet-CD)

[代码片段](https://github.com/likyoo/open-cd/blob/main/opencd/models/backbones/hanet.py)

## 摘要
得益于深度学习技术的发展，采用自动特征提取的基于深度学习的算法在变化检测（CD）任务上取得了显著的性能。然而，现有基于深度学习的CD方法的性能受到变化和未变化像素之间不平衡的阻碍。为了解决这个问题，本文在不添加变化信息的基础上提出了一种渐进式前景平衡采样策略，帮助模型在早期训练过程中准确学习变化像素的特征，从而提高检测性能。此外，我们设计了一种判别性孪生网络，层次注意力网络（HANet），它可以集成多尺度特征并细化详细特征。HANet的主要部分是HAN模块，它是一种轻量级且有效的自注意力机制。在两个具有极度不平衡标签的CD数据集上进行的广泛实验和消融研究验证了所提出方法的有效性和效率。

<!-- [IMAGE] -->

<div align=center>
<img src="https://github.com/likyoo/open-cd/assets/44317497/3b2d139e-35db-4691-87da-a1bb87819454" width="90%"/>
</div>

```bibtex
@ARTICLE{10093022,
  author={Han, Chengxi and Wu, Chen and Guo, Haonan and Hu, Meiqi and Chen, Hongruixuan},
  journal={IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing}, 
  title={HANet: A Hierarchical Attention Network for Change Detection With Bitemporal Very-High-Resolution Remote Sensing Images}, 
  year={2023},
  volume={16},
  number={},
  pages={3867-3878},
  doi={10.1109/JSTARS.2023.3264802}}

```

## 结果和模型

### LEVIR-CD

| 方法 | PFBS | 裁剪尺寸 | 学习率调度 | 内存 (GB) | 精确率 | 召回率 | F1分数 |  IoU  |                            配置                            | 下载 |
| :----: | :--: | :-------: | :-----: | :------: | :-------: | :----: | :------: | :---: | :----------------------------------------------------------: | :------: |
| HANet  | 不使用  |  256x256  |  40000  |    -     |   91.73   | 90.06  |  90.89   | 83.29 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/hanet/hanet_256x256_40k_levircd.py) |          |


- 所有指标均基于"变化"类别。
- 所有得分均在测试集上计算。
- `PFBS`表示渐进式前景平衡采样。
