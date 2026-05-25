#!/usr/bin/env python
# 解析 /tmp/opencd_train/<method>.log, 取每方法在雄安 val 上 changed 类 IoU 峰值, 输出全表对照
import re, os, json, sys
L = '/tmp/opencd_train'
ORDER = ['changer', 'bit', 'changeformer', 'snunet',
         'cgnet', 'hanet', 'ifn', 'tinycd', 'fc_ef', 'fc_siam_conc',
         'fc_siam_diff', 'changestar', 'lightcdnet', 'tinycd_v2',
         'ban', 'ttp', 'mtkd_step1_initial', 'mtkd_step3_distill']
row_re = re.compile(r'\|\s*changed\s*\|\s*([\d.nae]+)\s*\|\s*([\d.nae]+)\s*\|\s*([\d.nae]+)\s*\|\s*([\d.nae]+)\s*\|')
def fl(x):
    try: return float(x)
    except: return float('nan')
res = {}
for m in ORDER:
    fp = os.path.join(L, f'{m}.log')
    if not os.path.exists(fp):
        res[m] = {'status': 'no-log'}; continue
    txt = open(fp, errors='ignore').read()
    crashed = 'Traceback (most recent call last)' in txt
    rows = row_re.findall(txt)  # (F,P,R,IoU)
    # 从日志推断 val 间隔: max_iters / 验证次数 (20k->2000, 40k->4000)
    mi = re.search(r"max_iters\s*=\s*(\d+)", txt)
    maxit = int(mi.group(1)) if mi else 40000
    vi = (maxit // len(rows)) if rows else 4000
    vals = [dict(iter=(i+1)*vi, F=fl(f), P=fl(p), R=fl(r), IoU=fl(iou))
            for i, (f, p, r, iou) in enumerate(rows)]
    clean = [v for v in vals if v['IoU'] == v['IoU']]  # drop nan
    best = max(clean, key=lambda d: d['IoU']) if clean else None
    res[m] = {'status': 'crashed' if crashed and not clean else ('ok' if best else 'no-val'),
              'n_val': len(vals), 'best': best, 'final': vals[-1] if vals else None}
print(f"{'method':14} {'st':8} {'#v':>3} | {'BEST changed (peak)':>30} | {'FINAL':>13}")
print(f"{'':14} {'':8} {'':>3} | {'iter':>6}{'IoU':>7}{'F1':>7}{'P':>5}{'R':>5} | {'IoU':>6}{'F1':>6}")
print('-'*82)
for m in ORDER:
    r = res[m]
    if r['status'] in ('no-log',):
        print(f"{m:14} {r['status']:8}"); continue
    b = r.get('best'); f = r.get('final')
    bs = f"{b['iter']:>6}{b['IoU']:>7.2f}{b['F']:>7.2f}{b['P']:>5.0f}{b['R']:>5.0f}" if b else f"{'-':>30}"
    fs = f"{f['IoU']:>6.2f}{f['F']:>6.2f}" if f and f['IoU']==f['IoU'] else f"{'nan':>12}"
    print(f"{m:14} {r['status']:8} {r.get('n_val',0):>3} | {bs} | {fs}")
print('-'*82)
print(f"{'GOLD(student)':14} {'ref':8}     |      55.86  71.68   66   78 |  (best-epoch)")
json.dump(res, open(os.path.join(L, 'parsed_all.json'), 'w'), indent=2, ensure_ascii=False)
print('\nsaved', os.path.join(L, 'parsed_all.json'))
