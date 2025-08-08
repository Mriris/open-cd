#!/bin/bash

# 配置模型训练开关（true代表训练，false代表不训练）
TRAIN_CHANGER=true
TRAIN_SNUNET=true
TRAIN_BIT=true
TRAIN_FCEF=true
TRAIN_STANET=true
TRAIN_TINYCD=true
TRAIN_CHANGESTAR=true
TRAIN_IFN=true
TRAIN_CHANGEFORMER=true
TRAIN_LIGHTCDNET=true
TRAIN_BAN=true
TRAIN_HANET=true
# 新增的6个模型
TRAIN_FC_SIAM_DIFF=true
TRAIN_FC_SIAM_CONC=true
TRAIN_TINYCD_V2=true
TRAIN_CGNET=true
TRAIN_TTP=true
TRAIN_MTKD=true

# 设置模型训练的工作目录
WORK_DIR="./work_dirs/custom3"
mkdir -p $WORK_DIR

# 训练Changer模型
if [ "$TRAIN_CHANGER" = true ]; then
  echo "开始训练Changer模型..."
  python tools/train.py configs/custom/changer_custom.py --work-dir $WORK_DIR/changer
fi

# 训练SNUNet模型
if [ "$TRAIN_SNUNET" = true ]; then
  echo "开始训练SNUNet模型..."
  python tools/train.py configs/custom/snunet_custom.py --work-dir $WORK_DIR/snunet
fi

# 训练BIT模型
if [ "$TRAIN_BIT" = true ]; then
  echo "开始训练BIT模型..."
  python tools/train.py configs/custom/bit_custom.py --work-dir $WORK_DIR/bit
fi

# 训练FC-EF模型
if [ "$TRAIN_FCEF" = true ]; then
  echo "开始训练FC-EF模型..."
  python tools/train.py configs/custom/fcef_custom.py --work-dir $WORK_DIR/fcef
fi

# 训练STANet模型
if [ "$TRAIN_STANET" = true ]; then
  echo "开始训练STANet模型..."
  python tools/train.py configs/custom/stanet_custom.py --work-dir $WORK_DIR/stanet
fi

# 训练TinyCD模型
if [ "$TRAIN_TINYCD" = true ]; then
  echo "开始训练TinyCD模型..."
  python tools/train.py configs/custom/tinycd_custom.py --work-dir $WORK_DIR/tinycd
fi

# 训练ChangeStar模型
if [ "$TRAIN_CHANGESTAR" = true ]; then
  echo "开始训练ChangeStar模型..."
  python tools/train.py configs/custom/changestar_custom.py --work-dir $WORK_DIR/changestar
fi

# 训练IFN模型
if [ "$TRAIN_IFN" = true ]; then
  echo "开始训练IFN模型..."
  python tools/train.py configs/custom/ifn_custom.py --work-dir $WORK_DIR/ifn
fi

# 训练ChangeFormer模型
if [ "$TRAIN_CHANGEFORMER" = true ]; then
  echo "开始训练ChangeFormer模型..."
  python tools/train.py configs/custom/changeformer_custom.py --work-dir $WORK_DIR/changeformer
fi

# 训练LightCDNet模型
if [ "$TRAIN_LIGHTCDNET" = true ]; then
  echo "开始训练LightCDNet模型..."
  python tools/train.py configs/custom/lightcdnet_custom.py --work-dir $WORK_DIR/lightcdnet
fi

# 训练BAN模型
if [ "$TRAIN_BAN" = true ]; then
  echo "开始训练BAN模型..."
  python tools/train.py configs/custom/ban_custom.py --work-dir $WORK_DIR/ban
fi

# 训练HANet模型
if [ "$TRAIN_HANET" = true ]; then
  echo "开始训练HANet模型..."
  python tools/train.py configs/custom/hanet_custom.py --work-dir $WORK_DIR/hanet
fi

# 训练FC-Siam-diff模型
if [ "$TRAIN_FC_SIAM_DIFF" = true ]; then
  echo "开始训练FC-Siam-diff模型..."
  python tools/train.py configs/custom/fc_siam_diff_custom.py --work-dir $WORK_DIR/fc_siam_diff
fi

# 训练FC-Siam-conc模型
if [ "$TRAIN_FC_SIAM_CONC" = true ]; then
  echo "开始训练FC-Siam-conc模型..."
  python tools/train.py configs/custom/fc_siam_conc_custom.py --work-dir $WORK_DIR/fc_siam_conc
fi

# 训练TinyCDv2模型
if [ "$TRAIN_TINYCD_V2" = true ]; then
  echo "开始训练TinyCDv2模型..."
  python tools/train.py configs/custom/tinycd_v2_custom.py --work-dir $WORK_DIR/tinycd_v2
fi

# 训练CGNet模型
if [ "$TRAIN_CGNET" = true ]; then
  echo "开始训练CGNet模型..."
  python tools/train.py configs/custom/cgnet_custom.py --work-dir $WORK_DIR/cgnet
fi

# 训练TTP模型
if [ "$TRAIN_TTP" = true ]; then
  echo "开始训练TTP模型..."
  python tools/train.py configs/custom/ttp_custom.py --work-dir $WORK_DIR/ttp
fi

# 训练MTKD模型
if [ "$TRAIN_MTKD" = true ]; then
  echo "开始训练MTKD模型..."
  python tools/train.py configs/custom/mtkd_custom.py --work-dir $WORK_DIR/mtkd
fi

echo "所有模型训练完成" 