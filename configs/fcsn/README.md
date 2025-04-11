# FCSN

[用于变化检测的全卷积孪生网络](https://arxiv.org/abs/1810.08462)

## 简介

[代码片段](https://github.com/likyoo/open-cd/blob/main/opencd/models/backbones/siamunet_diff.py)

## 摘要
本文提出了三种全卷积神经网络架构，用于使用一对配准图像进行变化检测。最值得注意的是，我们提出了两种全卷积网络的孪生扩展，它们利用关于当前问题的启发式方法在我们对两个开放变化检测数据集的测试中取得了最佳结果，同时使用了RGB和多光谱图像。我们展示了我们的系统能够使用带注释的变化检测图像从头开始学习。我们的架构比先前提出的方法取得了更好的性能，同时比相关系统至少快500倍。这项工作是朝着高效处理来自大规模地球观测系统（如Copernicus或Landsat）的数据迈出的一步。

<!-- [IMAGE] -->

<div align=center>
<img src="https://user-images.githubusercontent.com/44317497/201501311-a5782a63-cf41-4ac3-bcc3-bcdc2612fc69.png" width="90%"/>
</div>

```bibtex
@inproceedings{daudt2018fully,
  title={Fully convolutional siamese networks for change detection},
  author={Daudt, Rodrigo Caye and Le Saux, Bertr and Boulch, Alexandre},
  booktitle={2018 25th IEEE International Conference on Image Processing (ICIP)},
  pages={4063--4067},
  year={2018},
  organization={IEEE}
}
```

## 结果和模型

### LEVIR-CD

|    方法    | 裁剪尺寸 | 学习率调度 | 内存 (GB) | 精确率 | 召回率 | F1分数 |  IoU  |                            配置                            | 下载 |
| :----------: | :-------: | :-----: | :------: | :-------: | :----: | :------: | :---: | :----------------------------------------------------------: | :------: |
|    FC-EF     |  256x256  |  40000  |    -     |   87.47   | 84.28  |  85.84   | 75.20 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/fcsn/fc_ef_256x256_40k_levircd.py) |          |
| FC-Siam-Diff |  256x256  |  40000  |    -     |   91.14   | 83.78  |  87.31   | 77.47 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/fcsn/fc_siam_diff_256x256_40k_levircd.py) |          |
| FC-Siam-Conc |  256x256  |  40000  |    -     |   88.08   | 88.95  |  88.51   | 79.39 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/fcsn/fc_siam_conc_256x256_40k_levircd.py) |          |


- 所有指标均基于"变化"类别。
- 所有得分均在测试集上计算。
