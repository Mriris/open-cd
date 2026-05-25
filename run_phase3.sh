#!/usr/bin/env bash
# Phase3: BAN + TTP + MTKD(5-run pipeline). 需 GPU0-3 空闲(wave2 结束后运行)
# 用法: bash run_phase3.sh [sanity|all]
set -u
ROOT=/mnt/data2/jingwei/yantingxuan/0Program/HeteCD2GOLD
OPENCD=$ROOT/open-cd
PY=$ROOT/.conda_opencd/bin/python
CFGDIR=configs/hcd3s_xiongan
WORKROOT=$OPENCD/work_dirs/hcd3s_xiongan
LOGDIR=/tmp/opencd_train
mkdir -p "$LOGDIR" "$WORKROOT"; cd "$OPENCD"

MODE="${1:-all}"
# 默认 20k(与 wave2 一致)
EXTRA_S="--cfg-options train_cfg.max_iters=20000 train_cfg.val_interval=2000 param_scheduler.1.end=20000 default_hooks.checkpoint.interval=2000"
if [ "$MODE" = "sanity" ]; then
  EXTRA_S="--cfg-options train_cfg.max_iters=20 train_cfg.val_interval=20 default_hooks.logger.interval=5 default_hooks.checkpoint.interval=20"
fi

launch(){ # name cfg gpu port [extra...]
  local name=$1 cfg=$2 gpu=$3 port=$4; shift 4
  echo "[launch] $name on GPU$gpu port$port"
  CUDA_VISIBLE_DEVICES=$gpu nohup "$PY" -m torch.distributed.run --nproc_per_node=1 --master_port=$port \
    "$OPENCD/tools/train.py" "$cfg" --work-dir "$WORKROOT/$name" --launcher pytorch "$@" \
    > "$LOGDIR/$name.log" 2>&1 &
  echo "  pid $!"
}

echo "########## Wave A: MTKD step1 + 3 teachers (GPU0-3) ##########"
launch mtkd_step1_initial      $CFGDIR/mtkd/mtkd_step1_initial.py      0 29640 $EXTRA_S
launch mtkd_step2_teacher_small  $CFGDIR/mtkd/mtkd_step2_teacher_small.py  1 29641 $EXTRA_S
launch mtkd_step2_teacher_medium $CFGDIR/mtkd/mtkd_step2_teacher_medium.py 2 29642 $EXTRA_S
launch mtkd_step2_teacher_large  $CFGDIR/mtkd/mtkd_step2_teacher_large.py  3 29643 $EXTRA_S
wait; echo "--- Wave A 结束 ---"

ST=$(ls -t $WORKROOT/mtkd_step1_initial/best_mIoU_*.pth 2>/dev/null | head -1)
TL=$(ls -t $WORKROOT/mtkd_step2_teacher_large/best_mIoU_*.pth 2>/dev/null | head -1)
TM=$(ls -t $WORKROOT/mtkd_step2_teacher_medium/best_mIoU_*.pth 2>/dev/null | head -1)
TS=$(ls -t $WORKROOT/mtkd_step2_teacher_small/best_mIoU_*.pth 2>/dev/null | head -1)
echo "MTKD ckpts: student=$ST"; echo "  tl=$TL"; echo "  tm=$TM"; echo "  ts=$TS"

echo "########## Wave B: BAN + TTP + MTKD step3 (GPU0-2) ##########"
launch ban  $CFGDIR/ban_vit-b16-clip_mit-b0_512x512_40k.py 0 29644 $EXTRA_S
launch ttp  $CFGDIR/ttp_vit-sam-l_512x512_40k.py           1 29645 $EXTRA_S
if [ -n "$ST" ] && [ -n "$TL" ] && [ -n "$TM" ] && [ -n "$TS" ]; then
  launch mtkd_step3_distill $CFGDIR/mtkd/mtkd_step3_distill.py 2 29646 \
    --cfg-options model.init_cfg.checkpoint=$ST model.init_cfg_t_l.checkpoint=$TL \
                  model.init_cfg_t_m.checkpoint=$TM model.init_cfg_t_s.checkpoint=$TS $EXTRA_S
else
  echo "[!] MTKD teacher/initial ckpt 缺失, 跳过 step3"
fi
wait; echo "########## Phase3 ALL DONE ##########"
