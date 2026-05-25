#!/usr/bin/env bash
# 训练结束后: 对每个 baseline 取 best checkpoint, 在雄安 val 跑 test.py, 收集 changed 类 IoU/F1
# 用法: bash collect_xiongan.sh
set -u
ROOT=/mnt/data2/jingwei/yantingxuan/0Program/HeteCD2GOLD
OPENCD=$ROOT/open-cd
PY=$ROOT/.conda_opencd/bin/python
CFGDIR=configs/hcd3s_xiongan
OUT=/tmp/opencd_train/xiongan_eval
mkdir -p "$OUT"
cd "$OPENCD"

declare -A CFG=(
  [changer]=changer_ex_r18_512x512_40k.py
  [bit]=bit_r18_512x512_40k.py
  [changeformer]=changeformer_mit-b0_512x512_40k.py
  [snunet]=snunet_c16_512x512_40k.py
)

echo "method,best_ckpt,changed_IoU,changed_Fscore,changed_Precision,changed_Recall" > "$OUT/summary.csv"
for n in changer bit changeformer snunet; do
  wd=$OPENCD/work_dirs/hcd3s_xiongan/$n
  ckpt=$(ls -t "$wd"/best_mIoU_*.pth 2>/dev/null | head -1)
  if [ -z "$ckpt" ]; then echo "[$n] 无 best ckpt, 跳过"; continue; fi
  echo "==================== test $n : $(basename "$ckpt") ===================="
  CUDA_VISIBLE_DEVICES=0 "$PY" -m torch.distributed.run --nproc_per_node=1 --master_port=29650 \
    "$OPENCD/tools/test.py" "$CFGDIR/${CFG[$n]}" "$ckpt" --launcher pytorch \
    > "$OUT/$n.test.log" 2>&1
  # 解析 changed 行: | changed | Fscore | Precision | Recall | IoU | Acc |
  row=$(grep -E "^\|\s*changed" "$OUT/$n.test.log" | tail -1)
  echo "$row"
  # 列序: |空|changed|Fscore($3)|Precision($4)|Recall($5)|IoU($6)|Acc($7)|
  vals=$(echo "$row" | tr -d ' ' | awk -F'|' '{print $6","$3","$4","$5}')  # IoU,Fscore,Precision,Recall
  echo "$n,$(basename "$ckpt"),$vals" >> "$OUT/summary.csv"
done
echo
echo "==================== 汇总 (changed 类, 雄安跨区域) ===================="
column -t -s, "$OUT/summary.csv"
echo
echo "对照: GOLD 学生(A+B) 跨区域 IoU_1=55.86 / F1=71.68 (域内 68.34/81.19)"
echo "CSV: $OUT/summary.csv ; 各方法 test 日志: $OUT/<method>.test.log"
