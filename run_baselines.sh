#!/usr/bin/env bash
# 并发训练 open-cd baseline (HCD-3S 训练 -> 雄安跨区域评测)
# 用法:
#   bash run_baselines.sh sanity              # 只跑 changer 20 iter 验证链路
#   bash run_baselines.sh all                 # GPU0-3 并发4 跑全部 40k
set -u
ROOT=/mnt/data2/jingwei/yantingxuan/0Program/HeteCD2GOLD
OPENCD=$ROOT/open-cd
PY=$ROOT/.conda_opencd/bin/python
CFGDIR=configs/hcd3s_xiongan
WORKROOT=$OPENCD/work_dirs/hcd3s_xiongan
LOGDIR=/tmp/opencd_train
mkdir -p "$LOGDIR" "$WORKROOT"
cd "$OPENCD"

# name:config:gpu:port
JOBS=(
  "changer:$CFGDIR/changer_ex_r18_512x512_40k.py:0:29611"
  "bit:$CFGDIR/bit_r18_512x512_40k.py:1:29612"
  "changeformer:$CFGDIR/changeformer_mit-b0_512x512_40k.py:2:29613"
  "snunet:$CFGDIR/snunet_c16_512x512_40k.py:3:29614"
)

launch () {
  local name=$1 cfg=$2 gpu=$3 port=$4; shift 4
  local extra="$*"
  local wd=$WORKROOT/$name
  echo "[launch] $name on GPU$gpu port$port -> $wd ; extra: $extra"
  # 显式用 conda env 的 python+torch.distributed.run(避免裸 torchrun 解析到 .venv)
  CUDA_VISIBLE_DEVICES=$gpu nohup "$PY" -m torch.distributed.run --nproc_per_node=1 --master_port=$port \
    "$OPENCD/tools/train.py" "$cfg" --work-dir "$wd" --launcher pytorch $extra \
    > "$LOGDIR/$name.log" 2>&1 &
  echo "  pid $!"
}

case "${1:-all}" in
  sanity)
    # 只用 changer, 20 iter, 立即验证 val 评测能产出 per-class IoU
    launch changer_sanity "$CFGDIR/changer_ex_r18_512x512_40k.py" 0 29610 \
      --cfg-options train_cfg.max_iters=20 train_cfg.val_interval=20 \
      default_hooks.logger.interval=5 default_hooks.checkpoint.interval=20
    ;;
  all)
    for j in "${JOBS[@]}"; do
      IFS=':' read -r name cfg gpu port <<< "$j"
      launch "$name" "$cfg" "$gpu" "$port"
      sleep 8   # 错开预训练权重下载/端口绑定
    done
    ;;
  *) echo "unknown mode $1"; exit 1;;
esac
echo "done launching; logs in $LOGDIR"
