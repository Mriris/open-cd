#!/usr/bin/env bash
# HCD-3S 域内多 seed baseline 队列（回应第二轮审稿意见 2）
# 3 个最强 baseline × 3 seed = 9 job，分配到 2 张空闲卡串行跑。
# 用法: bash run_indomain_seeds.sh
set -u
OPENCD=/data01/jingwei/yantingxuan/0Program/GOLD_new/open-cd
PY=/data01/jingwei/yantingxuan/0Program/GOLD_new/.conda_opencd/bin/python
CFGDIR=configs/hcd3s_indomain
WORKROOT=$OPENCD/work_dirs/hcd3s_indomain
LOGDIR=$OPENCD/logs_indomain
mkdir -p "$LOGDIR" "$WORKROOT"
cd "$OPENCD"

# 每张卡一条串行队列（同卡内顺序执行，避免显存争抢）
queue_gpu () {
  local gpu=$1; shift
  for spec in "$@"; do
    local name=${spec%%:*}; local rest=${spec#*:}
    local cfg=${rest%%:*}; local seed=${rest##*:}
    local wd=$WORKROOT/${name}_seed${seed}
    local log=$LOGDIR/${name}_seed${seed}.log
    if [ -f "$wd/.done" ]; then
      echo "[skip] $name seed$seed already done"; continue
    fi
    echo "[run] $name seed$seed on GPU$gpu -> $wd"
    CUDA_VISIBLE_DEVICES=$gpu "$PY" tools/train.py "$cfg" \
      --work-dir "$wd" --cfg-options randomness.seed=$seed > "$log" 2>&1 \
      && touch "$wd/.done" \
      || echo "[FAIL] $name seed$seed (see $log)"
  done
  echo "[queue done] GPU$gpu"
}

CH=$CFGDIR/changer_ex_r18_512x512_40k.py
IFN=$CFGDIR/ifn_512x512_40k.py
SNU=$CFGDIR/snunet_c16_512x512_40k.py

# GPU3 队列: changer×3 + snunet 前 1
queue_gpu 3 \
  "changer:$CH:222" "changer:$CH:444" "changer:$CH:777" \
  "snunet:$SNU:222" "snunet:$SNU:444" &

# GPU5 队列: ifn×3 + snunet 余 1
queue_gpu 5 \
  "ifn:$IFN:222" "ifn:$IFN:444" "ifn:$IFN:777" \
  "snunet:$SNU:777" &

wait
echo "ALL_QUEUES_COMPLETE"
