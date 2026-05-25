#!/usr/bin/env bash
# 在项目内独立 conda 环境 .conda_opencd 安装 open-cd(OpenMMLab) 栈
# 镜像：pip 全局已配置清华 (~/.config/pip/pip.conf)；mmcv 用 openmmlab 预编译轮
set -e
ROOT=/mnt/data2/jingwei/yantingxuan/0Program/HeteCD2GOLD
PY=$ROOT/.conda_opencd/bin/python
PIP="$PY -m pip"

echo "=== [0] python ==="; $PY --version
echo "=== [1] upgrade pip ==="
$PIP install --upgrade pip setuptools wheel

echo "=== [2] torch 2.1.0 (cu121, 清华 PyPI) ==="
$PIP install "torch==2.1.0" "torchvision==0.16.0" "torchaudio==2.1.0"
$PIP install "numpy<2"   # mmcv2.1/mmseg1.2 era 需 numpy<2

echo "=== [3] openmim ==="
$PIP install -U openmim

echo "=== [4] mmengine 0.10.4 ==="
$PY -m mim install "mmengine==0.10.4"

echo "=== [5] mmcv 2.1.0 (openmmlab 预编译轮 cu121/torch2.1) ==="
$PIP install "mmcv==2.1.0" -f https://download.openmmlab.com/mmcv/dist/cu121/torch2.1.0/index.html

echo "=== [6] mmpretrain 1.2.0 ==="
$PY -m mim install "mmpretrain==1.2.0"

echo "=== [7] mmseg 1.2.2 + mmdet 3.3.0 ==="
$PIP install "mmsegmentation==1.2.2" "mmdet==3.3.0"

echo "=== [8] open-cd 可编辑安装 ==="
cd $ROOT/open-cd && $PIP install -v -e .

echo "=== [9] 其它依赖 ==="
$PIP install ftfy regex einops prettytable

echo "=== [10] 自检 ==="
$PY - <<'PYEOF'
import torch, mmcv, mmengine, mmseg, mmdet
print("torch", torch.__version__, "cuda", torch.version.cuda, "avail", torch.cuda.is_available(), "ngpu", torch.cuda.device_count())
print("mmcv", mmcv.__version__, "mmengine", mmengine.__version__, "mmseg", mmseg.__version__, "mmdet", mmdet.__version__)
import opencd
print("opencd", getattr(opencd, "__version__", "?"))
PYEOF
echo "=== DONE ==="
