#!/bin/bash

# 配置模型测试开关（true代表测试，false代表不测试）
TEST_CHANGER=true
TEST_SNUNET=true
TEST_BIT=true
TEST_FCEF=true
TEST_STANET=true
TEST_TINYCD=true
TEST_CHANGESTAR=true
TEST_IFN=true
TEST_CHANGEFORMER=true
TEST_LIGHTCDNET=true
TEST_BAN=true
TEST_HANET=true

# 设置模型测试的工作目录
WORK_DIR="./work_dirs/custom2"

# 创建结果目录
RESULT_DIR="./results/custom3"
mkdir -p $RESULT_DIR

# 测试Changer模型
if [ "$TEST_CHANGER" = true ]; then
  # 测试Changer模型性能指标
  echo "测试Changer模型性能..."
  python tools/test.py configs/custom/changer_custom.py $WORK_DIR/changer/latest.pth

  # 测试Changer模型并生成可视化结果
  echo "生成Changer模型预测结果..."
  python tools/test.py configs/custom/changer_custom.py $WORK_DIR/changer/latest.pth --show-dir $RESULT_DIR/changer
fi

# 测试SNUNet模型
if [ "$TEST_SNUNET" = true ]; then
  # 测试SNUNet模型性能指标
  echo "测试SNUNet模型性能..."
  python tools/test.py configs/custom/snunet_custom.py $WORK_DIR/snunet/latest.pth

  # 测试SNUNet模型并生成可视化结果
  echo "生成SNUNet模型预测结果..."
  python tools/test.py configs/custom/snunet_custom.py $WORK_DIR/snunet/latest.pth --show-dir $RESULT_DIR/snunet
fi

# 测试BIT模型
if [ "$TEST_BIT" = true ]; then
  # 测试BIT模型性能指标
  echo "测试BIT模型性能..."
  python tools/test.py configs/custom/bit_custom.py $WORK_DIR/bit/latest.pth

  # 测试BIT模型并生成可视化结果
  echo "生成BIT模型预测结果..."
  python tools/test.py configs/custom/bit_custom.py $WORK_DIR/bit/latest.pth --show-dir $RESULT_DIR/bit
fi

# 测试FC-EF模型
if [ "$TEST_FCEF" = true ]; then
  # 测试FC-EF模型性能指标
  echo "测试FC-EF模型性能..."
  python tools/test.py configs/custom/fcef_custom.py $WORK_DIR/fcef/latest.pth

  # 测试FC-EF模型并生成可视化结果
  echo "生成FC-EF模型预测结果..."
  python tools/test.py configs/custom/fcef_custom.py $WORK_DIR/fcef/latest.pth --show-dir $RESULT_DIR/fcef
fi

# 测试STANet模型
if [ "$TEST_STANET" = true ]; then
  # 测试STANet模型性能指标
  echo "测试STANet模型性能..."
  python tools/test.py configs/custom/stanet_custom.py $WORK_DIR/stanet/latest.pth

  # 测试STANet模型并生成可视化结果
  echo "生成STANet模型预测结果..."
  python tools/test.py configs/custom/stanet_custom.py $WORK_DIR/stanet/latest.pth --show-dir $RESULT_DIR/stanet
fi

# 测试TinyCD模型
if [ "$TEST_TINYCD" = true ]; then
  # 测试TinyCD模型性能指标
  echo "测试TinyCD模型性能..."
  python tools/test.py configs/custom/tinycd_custom.py $WORK_DIR/tinycd/latest.pth

  # 测试TinyCD模型并生成可视化结果
  echo "生成TinyCD模型预测结果..."
  python tools/test.py configs/custom/tinycd_custom.py $WORK_DIR/tinycd/latest.pth --show-dir $RESULT_DIR/tinycd
fi

# 测试ChangeStar模型
if [ "$TEST_CHANGESTAR" = true ]; then
  # 测试ChangeStar模型性能指标
  echo "测试ChangeStar模型性能..."
  python tools/test.py configs/custom/changestar_custom.py $WORK_DIR/changestar/latest.pth

  # 测试ChangeStar模型并生成可视化结果
  echo "生成ChangeStar模型预测结果..."
  python tools/test.py configs/custom/changestar_custom.py $WORK_DIR/changestar/latest.pth --show-dir $RESULT_DIR/changestar
fi

# 测试IFN模型
if [ "$TEST_IFN" = true ]; then
  # 测试IFN模型性能指标
  echo "测试IFN模型性能..."
  python tools/test.py configs/custom/ifn_custom.py $WORK_DIR/ifn/latest.pth

  # 测试IFN模型并生成可视化结果
  echo "生成IFN模型预测结果..."
  python tools/test.py configs/custom/ifn_custom.py $WORK_DIR/ifn/latest.pth --show-dir $RESULT_DIR/ifn
fi

# 测试ChangeFormer模型
if [ "$TEST_CHANGEFORMER" = true ]; then
  # 测试ChangeFormer模型性能指标
  echo "测试ChangeFormer模型性能..."
  python tools/test.py configs/custom/changeformer_custom.py $WORK_DIR/changeformer/latest.pth

  # 测试ChangeFormer模型并生成可视化结果
  echo "生成ChangeFormer模型预测结果..."
  python tools/test.py configs/custom/changeformer_custom.py $WORK_DIR/changeformer/latest.pth --show-dir $RESULT_DIR/changeformer
fi

# 测试LightCDNet模型
if [ "$TEST_LIGHTCDNET" = true ]; then
  # 测试LightCDNet模型性能指标
  echo "测试LightCDNet模型性能..."
  python tools/test.py configs/custom/lightcdnet_custom.py $WORK_DIR/lightcdnet/latest.pth

  # 测试LightCDNet模型并生成可视化结果
  echo "生成LightCDNet模型预测结果..."
  python tools/test.py configs/custom/lightcdnet_custom.py $WORK_DIR/lightcdnet/latest.pth --show-dir $RESULT_DIR/lightcdnet
fi

# 测试BAN模型
if [ "$TEST_BAN" = true ]; then
  # 测试BAN模型性能指标
  echo "测试BAN模型性能..."
  python tools/test.py configs/custom/ban_custom.py $WORK_DIR/ban/latest.pth

  # 测试BAN模型并生成可视化结果
  echo "生成BAN模型预测结果..."
  python tools/test.py configs/custom/ban_custom.py $WORK_DIR/ban/latest.pth --show-dir $RESULT_DIR/ban
fi

# 测试HANet模型
if [ "$TEST_HANET" = true ]; then
  # 测试HANet模型性能指标
  echo "测试HANet模型性能..."
  python tools/test.py configs/custom/hanet_custom.py $WORK_DIR/hanet/latest.pth

  # 测试HANet模型并生成可视化结果
  echo "生成HANet模型预测结果..."
  python tools/test.py configs/custom/hanet_custom.py $WORK_DIR/hanet/latest.pth --show-dir $RESULT_DIR/hanet
fi

echo "所有模型测试完成" 