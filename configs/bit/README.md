# BiT

[利用Transformer进行遥感图像变化检测](https://arxiv.org/abs/2103.00208)

## 简介

[官方仓库](https://github.com/justchenhao/BIT_CD)

[代码片段](https://github.com/likyoo/open-cd/blob/main/opencd/models/decode_heads/bit_head.py)

## 摘要
现代变化检测（CD）通过深度卷积的强大判别能力取得了显著的成功。然而，高分辨率遥感CD仍然具有挑战性，因为场景中物体的复杂性。具有相同语义概念的物体在不同时间和空间位置可能表现出不同的光谱特性。大多数使用纯卷积的最新CD流程仍然难以关联时空中的长距离概念。非局部自注意力方法通过对像素之间的密集关系建模显示出有希望的性能，但计算效率低下。在这里，我们提出了一种双时态图像transformer（BIT）来高效且有效地在时空域内建模上下文。我们的直觉是，感兴趣的变化的高级概念可以由几个视觉词，即语义标记来表示。为了实现这一点，我们将双时态图像表示为几个标记，并使用transformer编码器在紧凑的基于标记的时空中建模上下文。学习到的丰富上下文的标记随后被反馈到像素空间，通过transformer解码器细化原始特征。我们将BIT纳入基于深度特征差分的CD框架中。在三个CD数据集上的广泛实验证明了所提出方法的有效性和效率。值得注意的是，我们基于BIT的模型明显优于纯卷积基线，仅使用三倍以下的计算成本和模型参数。基于一个简单的骨干网络（ResNet18）而没有复杂的结构（例如，特征金字塔网络（FPN）和UNet），我们的模型超过了几种最先进的CD方法，包括在效率和准确性方面优于四种最近的基于注意力的方法。我们的代码可在 https://github.com/justchenhao/BIT_CD 获取。

<!-- [IMAGE] -->

<div align=center>
<img src="https://user-images.githubusercontent.com/44317497/201470502-b50219fa-0b54-479e-9be1-836b5a5026c8.png" width="90%"/>
</div>

```bibtex
@Article{chen2021a,
    title={Remote Sensing Image Change Detection with Transformers},
    author={Hao Chen, Zipeng Qi and Zhenwei Shi},
    year={2021},
    journal={IEEE Transactions on Geoscience and Remote Sensing},
    volume={},
    number={},
    pages={1-14},
    doi={10.1109/TGRS.2021.3095166}
}
```

## 结果和模型

### LEVIR-CD

| 方法 | 骨干网络 | 裁剪尺寸 | 学习率调度 | 内存 (GB) | 精确率 | 召回率 | F1分数 |  IoU  |                            配置                            | 下载 |
| :----: | :------: | :-------: | :-----: | :------: | :-------: | :----: | :------: | :---: | :----------------------------------------------------------: | :------: |
|  BiT   |   r18    |  256x256  |  40000  |    -     |   91.97   | 88.62  |  90.26   | 82.25 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/bit/bit_r18_256x256_40k_levircd.py) |          |


- 所有指标均基于"变化"类别。
- 所有得分均在测试集上计算。
- resnet-18的stage4被移除。

