# JL1-CD

[JL1-CD：一个新的遥感变化检测基准和一个鲁棒的多教师知识蒸馏框架](https://arxiv.org/pdf/2502.13407)

## 简介

[官方仓库](https://github.com/circleLZY/MTKD-CD)

[代码片段](https://github.com/likyoo/opencd/models/change_detectors/mtkd.py)

## 摘要

深度学习在遥感图像变化检测(CD)领域取得了显著成功，但仍面临两个主要挑战：亚米级、全面开源CD数据集的稀缺性，以及在变化区域不同的图像上难以获得一致且令人满意的检测结果。为解决这些问题，我们引入了JL1-CD数据集，其包含5,000对512 x 512像素的图像，分辨率为0.5至0.75米。此外，我们提出了一个用于CD的多教师知识蒸馏(MTKD)框架。在JL1-CD和SYSU-CD数据集上的实验结果表明，MTKD框架显著提高了具有各种网络架构和参数规模的CD模型的性能，达到了新的最先进结果。代码可在此[链接](https://github.com/circleLZY/MTKD-CD)获取。

<!-- [IMAGE] -->

<div align=center>
<img src="https://github.com/user-attachments/assets/4a667426-bd45-442c-b4d4-890267cce483" width="90%"/>
</div>

```bibtex
@article{liu2025jl1,
  title={JL1-CD: A New Benchmark for Remote Sensing Change Detection and a Robust Multi-Teacher Knowledge Distillation Framework},
  author={Liu, Ziyuan and Zhu, Ruifei and Gao, Long and Zhou, Yuanxiu and Ma, Jingyu and Gu, Yuantao},
  journal={arXiv preprint arXiv:2502.13407},
  year={2025}
}
```

## 数据集
JL1-CD数据集现已公开可用。您可以从以下链接下载检查点文件：

- [Google Drive](https://drive.google.com/drive/folders/1ELoqx7J3GrEFMX5_rRynMjW9-Poxz3Uu?usp=sharing)
- [百度网盘](https://pan.baidu.com/s/1_vcO4c5DM5LDuOqLwLrWJg?pwd=5byn)
- [Hugging Face](https://huggingface.co/datasets/circleLZY/JL1-CD)

## 使用方法

### 训练

MTKD框架的训练过程包括三个步骤。下面，我们以**Changer-MiT-b0**模型为例：

#### 步骤1：训练原始模型

运行以下命令训练原始模型：

```bash
python tools/train.py configs/mtkd/step1/initial-changer_ex_mit-b0_512x512_200k_jl1cd.py --work-dir /path/to/save/models/Changer-mit-b0/initial
```

#### 步骤2：为不同变化区域比例(CAR)分区训练教师模型（例如，3个分区）

根据CAR分割数据：

```bash
python tools/dataset_converters/split_data_with_car.py
```

分别为小、中、大CAR分区训练教师模型：

```bash
python tools/train.py configs/mtkd/step2/small-changer_ex_mit-b0_512x512_200k_jl1cd.py --work-dir /path/to/save/models/Changer-mit-b0/small

python tools/train.py configs/mtkd/step2/medium-changer_ex_mit-b0_512x512_200k_jl1cd.py --work-dir /path/to/save/models/Changer-mit-b0/medium

python tools/train.py configs/mtkd/step2/large-changer_ex_mit-b0_512x512_200k_jl1cd.py --work-dir /path/to/save/models/Changer-mit-b0/large
```

在上述两个步骤中，您将有四个**Changer-MiT-b0**模型版本：原始模型和三个教师模型（小、中、大）。此时，O-P策略已经可以应用。

#### 步骤3：训练学生模型

在`configs/mtkd/step3/mtkd-changer_ex_mit-b0_512x512_200k_jl1cd.py`中为学生模型和教师模型初始化检查点路径：

- `checkpoint_student`
- `checkpoint_teacher_l`
- `checkpoint_teacher_m`
- `checkpoint_teacher_s`

然后，运行以下命令训练学生模型：

```bash
python tools/train.py configs/mtkd/step3/mtkd-changer_ex_mit-b0_512x512_200k_jl1cd.py --work-dir /path/to/save/models/Changer-mit-b0/distill
```

完成此步骤后，您将拥有在MTKD框架内训练的学生模型。

### 测试

测试用MTKD训练的学生模型很简单。运行以下命令：

```bash
python test.py <config-file> <checkpoint>
```

测试O-P策略更为复杂。您可以参考位于`tools/test_pipline/single-partition-3-test.py`的脚本了解更多细节。

#### 检查点

您可以从以下链接下载检查点文件：
- [百度网盘](https://pan.baidu.com/s/1F5MIGCCiNHFifNl_kDiklA?pwd=4tid)
- [Hugging Face](https://huggingface.co/circleLZY/MTKD)

