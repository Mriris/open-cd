#!/bin/bash
# 三基线 3-seed ensemble + flip4-TTA 全量评测（串行，GPU0）
set -e
PY=../.conda_opencd/bin/python
run() {
  name=$1; cfg=$2
  echo "===== $name ====="
  CUDA_VISIBLE_DEVICES=0 $PY ensemble_eval_indomain.py --config $cfg \
    --ckpts "work_dirs/hcd3s_indomain/${name}_seed222/best_mIoU_iter_*.pth" \
            "work_dirs/hcd3s_indomain/${name}_seed444/best_mIoU_iter_*.pth" \
            "work_dirs/hcd3s_indomain/${name}_seed777/best_mIoU_iter_*.pth"
}
run changer configs/hcd3s_indomain/changer_ex_r18_512x512_40k.py
run ifn     configs/hcd3s_indomain/ifn_512x512_40k.py
run snunet  configs/hcd3s_indomain/snunet_c16_512x512_40k.py
echo "ALL DONE"
