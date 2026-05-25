#!/usr/bin/env bash
# 分波训练 open-cd 其余轻量 CD 方法 (HCD-3S 训练 -> 雄安跨区域), 每波4个并发(GPU0-3), 波间 wait
set -u
ROOT=/mnt/data2/jingwei/yantingxuan/0Program/HeteCD2GOLD
OPENCD=$ROOT/open-cd
PY=$ROOT/.conda_opencd/bin/python
CFGDIR=configs/hcd3s_xiongan
WORKROOT=$OPENCD/work_dirs/hcd3s_xiongan
LOGDIR=/tmp/opencd_train
mkdir -p "$LOGDIR" "$WORKROOT"
cd "$OPENCD"

METHODS=(cgnet hanet ifn tinycd fc_ef fc_siam_conc fc_siam_diff changestar lightcdnet tinycd_v2)

MODE="${1:-all}"
SUFFIX=""
# 默认 20k(峰值都<=20k, 省时), val 每 2000 iter, poly 终点同步到 20000
EXTRA="--cfg-options train_cfg.max_iters=20000 train_cfg.val_interval=2000 param_scheduler.1.end=20000 default_hooks.checkpoint.interval=2000"
if [ "$MODE" = "sanity" ]; then
  EXTRA="--cfg-options train_cfg.max_iters=20 train_cfg.val_interval=20 default_hooks.logger.interval=5 default_hooks.checkpoint.interval=20"
  SUFFIX="_sanity"
fi

i=0
for m in "${METHODS[@]}"; do
  gpu=$((i % 4)); port=$((29620 + i))
  cfg=$CFGDIR/${m}_512x512_40k.py; wd=$WORKROOT/${m}${SUFFIX}
  echo "[launch] $m on GPU$gpu port$port -> $wd"
  CUDA_VISIBLE_DEVICES=$gpu nohup "$PY" -m torch.distributed.run --nproc_per_node=1 --master_port=$port \
    "$OPENCD/tools/train.py" "$cfg" --work-dir "$wd" --launcher pytorch $EXTRA \
    > "$LOGDIR/${m}${SUFFIX}.log" 2>&1 &
  i=$((i+1))
  if [ $((i % 4)) -eq 0 ]; then echo "  --- 等待本波 4 个结束 ---"; wait; echo "  --- 本波结束 ---"; fi
done
wait
echo "===== ALL WAVES DONE ($i methods) ====="
