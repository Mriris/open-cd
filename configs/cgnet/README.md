# CGNet

[变化引导网络：融合变化先验引导遥感图像变化检测](https://ieeexplore.ieee.org/document/10234560)

## 简介

[官方仓库](https://github.com/ChengxiHAN/CGNet-CD)

[代码片段](https://github.com/likyoo/open-cd/blob/main/opencd/models/backbones/cgnet.py)

## 摘要
自动化人工智能算法和遥感仪器的快速发展使变化检测（CD）任务受益。然而，精确检测仍有很大的研究空间，特别是变化特征的边缘完整性和内部空洞现象。为了解决这些问题，我们设计了变化引导网络（CGNet）来解决以往方法中采用的传统U-Net结构中变化特征表达不足的问题，这导致了不准确的边缘检测和内部空洞。从具有丰富语义信息的深层特征生成变化图，并将其用作先验信息来引导多尺度特征融合，从而提高变化特征的表达能力。同时，我们提出了一种名为变化引导模块的自注意力模块，它可以有效地捕捉像素之间的长距离依赖，有效克服了传统卷积神经网络感受野不足的问题。在四个主要的CD数据集上，我们验证了CGNet的有用性和效率，大量的实验和消融研究证明了CGNet的有效性。

<!-- [IMAGE] -->

<div align=center>
<img src="https://github.com/likyoo/open-cd/assets/44317497/d4f0e42e-8446-448f-8afa-d1ab4339283d" width="75%"/>
</div>



```bibtex
@ARTICLE{10234560,
  author={Han, Chengxi and Wu, Chen and Guo, Haonan and Hu, Meiqi and Li, Jiepan and Chen, Hongruixuan},
  journal={IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing}, 
  title={Change Guiding Network: Incorporating Change Prior to Guide Change Detection in Remote Sensing Imagery}, 
  year={2023},
  volume={16},
  number={},
  pages={8395-8407},
  keywords={Feature extraction;Transformers;Convolutional neural networks;Remote sensing;Deep learning;Decoding;Computational modeling;Artificial intelligence;Change detection (CD);change guide module (CGM);change guiding map;deep learning;high-resolution remote sensing (RS) image},
  doi={10.1109/JSTARS.2023.3310208}}
```

## 结果和模型

### LEVIR-CD-256

| 方法 | 图像尺寸 | 学习率调度 | 内存 (GB) | 精确率 | 召回率 | F1分数 |  IoU  |                            配置                            | 下载 |
| :----: | :--------: | :-----: | :------: | :-------: | :----: | :------: | :---: | :----------------------------------------------------------: | :------: |
| CGNet  |  256x256   |  100e   |    -     |   93.18   | 90.99  |  92.07   | 85.31 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/cgnet/cgnet_256x256_100e_levircd-256.py) |          |


- 所有指标均基于"变化"类别。
- 所有得分均在测试集上计算。


