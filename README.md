<div align="center">
  <img src="resources/opencd-logo.png" width="600"/>
</div>

------

<div align="center">
<a href="https://arxiv.org/abs/2407.15317"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Farxiv.org%2Fabs%2F2407.15317&count_bg=%23FF0000&title_bg=%23555555&icon=arxiv.svg&icon=&icon_color=%23E7E7E7&title=Technical+Report&edge_flat=false"/></a>
<a href="https://github.com/likyoo/open-cd"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Flikyoo%2Fopen-cdA&count_bg=%2379C83D&title_bg=%23555555&icon=github.svg&icon_color=%23E7E7E7&title=Github&edge_flat=false"/></a>
<a href="https://huggingface.co/likyoo/Open-CD_Model_Zoo"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fhuggingface.co%2Flikyoo%2FOpen-CD_Model_Zoo&count_bg=%23684BD3&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=%F0%9F%A4%97%20Hugging%20Face&edge_flat=false"/></a>
</div>

## 简介
Open-CD是一个基于一系列开源通用视觉任务工具的开源变化检测工具箱。

## 新闻
- 7/25/2025 - Open-CD Technical Report is accepted by ACMMM 2025. 🎉
- 2025/4/11 - 支持[MTKD](https://github.com/circleLZY/MTKD-CD)方法和[JL1-CD](https://github.com/circleLZY/MTKD-CD)数据集。Open-CD技术报告更新至v1.1版本。
- 2024/7/23 - **Open-CD技术报告v1.0已在[arXiv](https://arxiv.org/abs/2407.15317)发布，感谢所有贡献者！欢迎加入我们！** 💥💥💥
- 2024/6/29 - 支持[ChangeStar](https://github.com/Z-Zheng/ChangeStar)和[FarSeg](https://github.com/Z-Zheng/FarSeg)。
- 2024/6/20 - 我们启动**[Open-CD技术报告计划](https://github.com/likyoo/open-cd/tree/main/projects/open-cd_technical_report)**，欢迎加入我们！！！ 💥💥💥
- 2024/6/17 - 支持[CGNet](https://github.com/ChengxiHAN/CGNet-CD)。
- 2024/2/10 - Open-CD升级到v1.1.0版本。支持[BAN](https://github.com/likyoo/BAN)、[TTP](https://github.com/KyanChen/TTP)和[LightCDNet](https://github.com/NightSongs/LightCDNet)。添加了推理API。
- 2023/4/21 - Open-CD v1.0.0在1.x分支发布，基于OpenMMLab 2.0！同时支持PyTorch 2.0！
- 2023/3/14 - Open-CD升级到v0.0.3版本。支持语义变化检测（SCD）！
- 2022/11/17 - Open-CD升级到v0.0.2版本，需要更高版本的MMSegmentation依赖。
- 2022/9/28 - [ChangerEx](https://github.com/likyoo/open-cd/tree/main/configs/changer)的代码、预训练模型和日志可用。:yum:
- 2022/9/20 - 我们的论文[Changer: Feature Interaction is What You Need for Change Detection](https://arxiv.org/abs/2209.08290)已发布！
- 2022/7/30 - Open-CD正式公开发布！

## 基准和模型库

支持的工具箱：

- [x] [OpenMMLab工具包](https://github.com/open-mmlab)
- [x] [pytorch-image-models](https://github.com/rwightman/pytorch-image-models)
- [ ] ...

支持的变化检测模型：
（_部分模型代码直接借鉴自其官方仓库_）

- [x] [FC-EF (ICIP'2018)](configs/fcsn)
- [x] [FC-Siam-diff (ICIP'2018)](configs/fcsn)
- [x] [FC-Siam-conc (ICIP'2018)](configs/fcsn)
- [x] [STANet (RS'2020)](configs/stanet)
- [x] [IFN (ISPRS'2020)](configs/ifn)
- [x] [SNUNet (GRSL'2021)](configs/snunet)
- [x] [BiT (TGRS'2021)](configs/bit)
- [x] [ChangeStar (ICCV'2021)](configs/changestar)
- [x] [ChangeFormer (IGARSS'22)](configs/changeformer)
- [x] [TinyCD (NCA'2023)](configs/tinycd)
- [x] [Changer (TGRS'2023)](configs/changer)
- [x] [HANet (JSTARS'2023)](configs/hanet)
- [x] [TinyCDv2 (Under Review)](configs/tinycd_v2)
- [x] [LightCDNet (GRSL'2023)](configs/lightcdnet)
- [x] [CGNet (JSTARS'2023)](configs/cgnet)
- [x] [BAN (TGRS'2024)](configs/ban)
- [x] [TTP (arXiv'2023)](configs/ttp)
- [x] [MTKD (arXiv'2025)](configs/mtkd)
- [ ] ...

支持的数据集：| [描述](https://github.com/wenhwu/awesome-remote-sensing-change-detection)
- [x] [LEVIR-CD](https://justchenhao.github.io/LEVIR/)
- [x] [WHU-CD](https://study.rsgis.whu.edu.cn/pages/download/building_dataset.html)
- [x] [S2Looking](https://github.com/S2Looking/Dataset)
- [x] [SVCD](https://drive.google.com/file/d/1GX656JqqOyBi_Ef0w65kDGVto-nHrNs9/edit)
- [x] [DSIFN](https://github.com/GeoZcx/A-deeply-supervised-image-fusion-network-for-change-detection-in-remote-sensing-images/tree/master/dataset)
- [x] [CLCD](https://github.com/liumency/CropLand-CD)
- [x] [RSIPAC](https://engine.piesat.cn/ai/autolearning/index.html#/dataset/detail?key=8f6c7645-e60f-42ce-9af3-2c66e95cfa27)
- [x] [SECOND](https://captain-whu.github.io/SCD/)
- [x] [Landsat](https://figshare.com/articles/figure/Landsat-SCD_dataset_zip/19946135/1)
- [x] [BANDON](https://github.com/fitzpchao/BANDON)
- [x] [JL1-CD](https://github.com/circleLZY/MTKD-CD)
- [ ] ...

## 使用方法

[文档](https://github.com/open-mmlab/mmsegmentation/tree/master/docs)

请参考mmseg中的[get_started.md](https://github.com/open-mmlab/mmsegmentation/blob/master/docs/en/get_started.md#installation)。

也提供了Colab教程。您可以直接在[Colab](https://colab.research.google.com/drive/1puZY5R8fwlL6um6pHbgbM1NTYZUXdK2J?usp=sharing)上运行。（感谢[@Agustin](https://github.com/AgustinNormand)提供的演示）[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1puZY5R8fwlL6um6pHbgbM1NTYZUXdK2J?usp=sharing)

#### 安装

```
# 将OpenMMLab工具包作为Python包安装
pip install -U openmim
mim install mmengine
mim install "mmcv>=2.0.0"
mim install "mmpretrain>=1.0.0rc7"
pip install "mmsegmentation>=1.2.2"
pip install "mmdet>=3.0.0"
```
```
git clone https://github.com/likyoo/open-cd.git
cd open-cd
pip install -v -e .
```
更多详情，请参见[这里](https://github.com/likyoo/open-cd/blob/main/docs/install.md)。

#### 训练
```
python tools/train.py configs/changer/changer_ex_r18_512x512_40k_levircd.py --work-dir ./changer_r18_levir_workdir
```

#### 测试
```
# 获取.png结果
python tools/test.py configs/changer/changer_ex_r18_512x512_40k_levircd.py changer_r18_levir_workdir/latest.pth --show-dir tmp_infer
# 获取评估指标
python tools/test.py configs/changer/changer_ex_r18_512x512_40k_levircd.py changer_r18_levir_workdir/latest.pth
```

#### 推理
请参考[推理](https://github.com/likyoo/open-cd/blob/main/docs/inference.md)文档。

## 引用

如果您在研究中使用了这个项目，请引用：

```bibtex
@article{opencd,
  title   = {{Open-CD}: A Comprehensive Toolbox for Change Detection},
  author  = {Li, Kaiyu and Jiang, Jiawei and Codegoni, Andrea and Han, Chengxi and Deng, Yupeng and Chen, Keyan and Zheng, Zhuo and
             Chen, Hao and Liu, Ziyuan and Gu, Yuantao and Zou, Zhengxia and Shi, Zhenwei and Fang, Sheng and Meng, Deyu and Wang, Zhi and Cao, Xiangyong},
  journal= {arXiv preprint arXiv:2407.15317},
  year={2024}
}
```
您也可以考虑引用：

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

@ARTICLE{10129139,
  author={Fang, Sheng and Li, Kaiyu and Li, Zhe},
  journal={IEEE Transactions on Geoscience and Remote Sensing}, 
  title={Changer: Feature Interaction is What You Need for Change Detection}, 
  year={2023},
  volume={61},
  number={},
  pages={1-11},
  doi={10.1109/TGRS.2023.3277496}}
```

## 许可证

Open-CD 采用 Apache 2.0 许可证发布。
