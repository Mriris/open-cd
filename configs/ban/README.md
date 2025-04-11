# BAN

[基于基础模型的遥感变化检测新学习范式](https://arxiv.org/abs/2312.01163)

## 简介

[官方仓库](https://github.com/likyoo/BAN)

[代码片段](https://github.com/likyoo/open-cd/blob/main/opencd/models/decode_heads/ban_head.py)

## 摘要

变化检测（CD）是观察和分析土地覆盖动态过程的关键任务。尽管许多基于深度学习的CD模型表现出色，但它们的进一步性能提升受限于从给定标记数据中提取的有限知识。另一方面，最近出现的基础模型通过跨数据模态和代理任务的扩展包含了大量知识。在本文中，我们提出了双时态适配器网络（BAN），这是一个通用的基于基础模型的CD适配框架，旨在提取基础模型的知识用于CD任务。所提出的BAN包含三个部分，即冻结的基础模型（如CLIP）、双时态适配器分支（Bi-TAB）和它们之间的桥接模块。具体而言，Bi-TAB可以是现有的任意CD模型或一些手工设计的堆叠块。桥接模块旨在将通用特征与任务/领域特定特征对齐，并将选定的通用知识注入到Bi-TAB中。据我们所知，这是第一个将基础模型适配到CD任务的通用框架。大量实验表明，我们的BAN在改进现有CD方法性能方面的有效性（例如，IoU提高了高达4.08%），仅使用了少量额外的可学习参数。更重要的是，这些成功的实践向我们展示了基础模型在遥感CD中的潜力。代码可在https://github.com/likyoo/BAN 获取，并将在[Open-CD](https://github.com/likyoo/open-cd)中得到支持。

<!-- [IMAGE] -->

<div align=center>
<img src="https://github.com/likyoo/BAN/blob/main/resources/BAN.png" width="100%"/>
</div>




```bibtex
@ARTICLE{10438490,
  author={Li, Kaiyu and Cao, Xiangyong and Meng, Deyu},
  journal={IEEE Transactions on Geoscience and Remote Sensing}, 
  title={A New Learning Paradigm for Foundation Model-based Remote Sensing Change Detection}, 
  year={2024},
  volume={},
  number={},
  pages={1-1},
  keywords={Adaptation models;Task analysis;Data models;Computational modeling;Feature extraction;Transformers;Tuning;Change detection;foundation model;visual tuning;remote sensing image processing;deep learning},
  doi={10.1109/TGRS.2024.3365825}}

```

## 结果和模型

### LEVIR-CD

| 方法 |       预训练       |     Bi-TAB      | 裁剪尺寸 | 学习率调度 | 精确率 | 召回率 | F1分数 |  IoU  |                            配置                            |
| :----: | :------------------: | :-------------: | :-------: | :-----: | :-------: | :----: | :------: | :---: | :----------------------------------------------------------: |
|  BAN   |    ViT-L/14, CLIP    |       BiT       |  512x512  |  40000  |   92.83   | 90.89  |  91.85   | 84.93 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-l14-clip_bit_512x512_40k_levircd.py) |
|  BAN   |    ViT-B/16, CLIP    | ChangeFormer-b0 |  512x512  |  40000  |   93.25   | 90.21  |  91.71   | 84.68 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-b16-clip_mit-b0_512x512_40k_levircd.py) |
|  BAN   |    ViT-L/14, CLIP    | ChangeFormer-b0 |  512x512  |  40000  |   93.47   | 90.30  |  91.86   | 84.94 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-l14-clip_mit-b0_512x512_40k_levircd.py) |
|  BAN   |    ViT-L/14, CLIP    | ChangeFormer-b1 |  512x512  |  40000  |   93.48   | 90.76  |  92.10   | 85.36 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-l14-clip_mit-b1_512x512_40k_levircd.py) |
|  BAN   |    ViT-L/14, CLIP    | ChangeFormer-b2 |  512x512  |  40000  |   93.61   | 91.02  |  92.30   | 85.69 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-l14-clip_mit-b2_512x512_40k_levircd.py) |
|  BAN   | ViT-B/32, RemoteCLIP | ChangeFormer-b0 |  512x512  |  40000  |   93.28   | 90.26  |  91.75   | 84.75 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-b32-remoteclip_mit-b0_512x512_40k_levircd.py) |
|  BAN   | ViT-L/14, RemoteCLIP | ChangeFormer-b0 |  512x512  |  40000  |   93.44   | 90.46  |  91.92   | 85.05 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-l14-remoteclip_mit-b0_512x512_40k_levircd.py) |
|  BAN   | ViT-B/32, GeoRSCLIP  | ChangeFormer-b0 |  512x512  |  40000  |   93.35   | 90.24  |  91.77   | 84.79 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-b32-georsclip_mit-b0_512x512_40k_levircd.py) |
|  BAN   | ViT-L/14, GeoRSCLIP  | ChangeFormer-b0 |  512x512  |  40000  |   93.50   | 90.48  |  91.96   | 85.13 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-l14-georsclip_mit-b0_512x512_40k_levircd.py) |
|  BAN   |   ViT-B/16, IN-21K   | ChangeFormer-b0 |  512x512  |  40000  |   93.59   | 89.80  |  91.66   | 84.60 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-b16-in21k_mit-b2_512x512_40k_levircd.py) |
|  BAN   |   ViT-L/16, IN-21K   | ChangeFormer-b0 |  512x512  |  40000  |   93.27   | 90.11  |  91.67   | 84.61 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-l16-in21k_mit-b0_512x512_40k_levircd.py) |

### S2Looking

| 方法 |    预训练    |     Bi-TAB      | 裁剪尺寸 | 学习率调度 | 精确率 | 召回率 | F1分数 |  IoU  |                            配置                            |
| :----: | :------------: | :-------------: | :-------: | :-----: | :-------: | :----: | :------: | :---: | :----------------------------------------------------------: |
|  BAN   | ViT-L/14, CLIP |       BiT       |  512x512  |  80000  |   75.06   | 58.00  |  65.44   | 48.63 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-l14-clip_bit_512x512_80k_s2looking.py) |
|  BAN   | ViT-L/14, CLIP | ChangeFormer-b0 |  512x512  |  80000  |   74.63   | 60.30  |  66.70   | 50.04 | [配置](https://github.com/likyoo/open-cd/blob/main/configs/ban/ban_vit-l14-clip_mit-b0_512x512_80k_s2looking.py) |


- 您可以从[huggingface](https://huggingface.co/likyoo/BAN/tree/main/pretrain) | [百度网盘](https://pan.baidu.com/s/1RkIGsOB3XBi7Oi6mKIpZ2w?pwd=kfp9)下载预训练的ViT模型用于训练。
- 您可以从[huggingface](https://huggingface.co/likyoo/BAN/tree/main/checkpoint) | [百度网盘](https://pan.baidu.com/s/1RkIGsOB3XBi7Oi6mKIpZ2w?pwd=kfp9)下载检查点文件用于评估。
- 所有指标均基于"变化"类别。
- 所有得分均在测试集上计算。
