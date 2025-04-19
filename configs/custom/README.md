# 遥感图像异源变化检测自定义配置

本目录包含为自定义数据集配置的变化检测模型。数据集结构应如下所示：

```
data/custom_dataset/
├── train/
│   ├── A/         # 时相1图像
│   ├── B/         # 时相2图像
│   └── label/     # 标签图像
└── test/
    ├── A/         # 时相1图像
    ├── B/         # 时相2图像
    └── label/     # 标签图像
```

## 数据集格式

- 所有图像都应为512x512大小的PNG格式
- A目录：时相1图像
- B目录：时相2图像
- label目录：二值化标签图像（0为未变化，1或255为变化区域）

## 配置文件说明

- `custom_dataset_config.py`：数据集基础配置
- `changer_custom.py`：Changer模型配置（使用ResNet-18作为主干网络）
- `snunet_custom.py`：SNUNet模型配置
- `bit_custom.py`：BIT模型配置（使用ResNet-18作为主干网络）
- `fcef_custom.py`：FC-EF模型配置

## 训练模型

### 单个模型训练

```bash
# 训练Changer模型
python tools/train.py configs/custom/changer_custom.py --work-dir ./work_dirs/custom/changer

# 训练SNUNet模型
python tools/train.py configs/custom/snunet_custom.py --work-dir ./work_dirs/custom/snunet

# 训练BIT模型
python tools/train.py configs/custom/bit_custom.py --work-dir ./work_dirs/custom/bit

# 训练FC-EF模型
python tools/train.py configs/custom/fcef_custom.py --work-dir ./work_dirs/custom/fcef
```

### 批量训练所有模型

```bash
# 赋予执行权限
chmod +x tools/train_custom_models.sh

# 执行训练脚本
./tools/train_custom_models.sh
```

## 测试模型

### 单个模型测试

```bash
# 测试Changer模型并获取评估指标
python tools/test.py configs/custom/changer_custom.py work_dirs/custom/changer/latest.pth

# 测试Changer模型并保存可视化结果
python tools/test.py configs/custom/changer_custom.py work_dirs/custom/changer/latest.pth --show-dir results/custom/changer
```

### 批量测试所有模型

```bash
# 赋予执行权限
chmod +x tools/test_custom_models.sh

# 执行测试脚本
./tools/test_custom_models.sh
```

## 评估指标

默认评估指标包括：
- mIoU (平均交并比)
- mFscore (平均F1分数)

测试结果将输出在控制台，可视化结果将保存在指定的目录中。

## 注意事项

- 训练过程中会自动在指定工作目录保存检查点
- 测试时使用的是最新的检查点（latest.pth），您也可以指定其他检查点
- 如需使用分布式训练，请参考Open-CD文档中的分布式训练指南 