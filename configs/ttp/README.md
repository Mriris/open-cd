# TTP

[时间旅行像素：基于基础模型的双时相特征集成用于遥感图像变化检测](https://arxiv.org/abs/2312.16202)

## 简介

[官方仓库](https://github.com/KyanChen/TTP)

[代码片段](https://github.com/likyoo/open-cd/blob/main/opencd/models/change_detectors/ttp.py)



## 摘要

变化检测作为遥感领域的一个突出研究方向，在观察和分析地表变化中起着关键作用。尽管通过基于深度学习的方法取得了显著进展，但在时空复杂的遥感场景中执行高精度变化检测仍然是一个巨大挑战。最近涌现的基础模型，凭借其强大的通用性和泛化能力，提供了潜在的解决方案。然而，跨越数据和任务之间的差距仍然是一个重要障碍。在本文中，我们引入时间旅行像素（TTP），这是一种将SAM基础模型的潜在知识集成到变化检测中的新方法。这种方法有效解决了通用知识迁移中的领域偏移问题，以及表达多时相图像同质和异质特性的挑战。在LEVIR-CD上获得的最先进结果凸显了TTP的有效性。代码可在https://kychen.me/TTP获取。

<!-- [IMAGE] -->

<div align=center>
<img src="https://github.com/likyoo/open-cd/assets/44317497/a61cd241-f9fb-4fd8-82c8-a20633222db5" width="100%"/>
</div>


```bibtex
@article{chen2023time,
  title={Time Travelling Pixels: Bitemporal Features Integration with Foundation Model for Remote Sensing Image Change Detection},
  author={Chen, Keyan and Liu, Chengyang and Li, Wenyuan and Liu, Zili and Chen, Hao and Zhang, Haotian and Zou, Zhengxia and Shi, Zhenwei},
  journal={arXiv preprint arXiv:2312.16202},
  year={2023}
}
```

## 依赖

```
pip install peft
```

## 结果和模型

### LEVIR-CD

| 方法 | 骨干网络  | 裁剪尺寸 | 学习率调度 | 精确率 | 召回率 | F1分数 | IoU  |                            配置                            |
| :----: | --------- | :-------: | :-----: | :-------: | :----: | :------: | :--: | :----------------------------------------------------------: |
|  TTP   | ViT-SAM-L |  512x512  |  300e   |   93.0    |  91.7  |   92.1   | 85.6 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ttp/ttp_vit-sam-l_512x512_300e_levircd.py) |


- 所有指标均基于"变化"类别。
- 所有得分均在测试集上计算。
