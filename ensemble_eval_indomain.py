# 3-seed ensemble + flip4-TTA 评测（域内 Split45 val，回应第二轮审稿意见 2 的公平性对照）
# 协议与主仓 ensemble_eval.py 对齐：N 模型前景概率平均 + 原生判决规则；
# flip4 = identity / hflip / vflip / 180°。同时输出各成员单模型 no-TTA 的 IoU_1，
# 用于与 refine-logs/seed_stats_round2.json 交叉校验协议正确性。
#
# 前景概率：双通道头取 softmax 的 class-1 通道，单通道二值头（如 IFN out_channels=1）
# 取 sigmoid。判决沿用各方法训练时 val 的原生规则：双通道 argmax（等价 >0.5）、
# 单通道用 decode_head.threshold（mmseg 默认 0.3）——保证单模型 no-TTA 能逐位复现
# 训练日志里的 best IoU。
#
# 用法（.conda_opencd 环境）：
#   CUDA_VISIBLE_DEVICES=0 python ensemble_eval_indomain.py \
#     --config configs/hcd3s_indomain/changer_ex_r18_512x512_40k.py \
#     --ckpts work_dirs/hcd3s_indomain/changer_seed{222,444,777}/best_mIoU_iter_*.pth
import argparse
import glob

import torch
from mmengine.config import Config
from mmengine.registry import DefaultScope
from mmengine.runner import Runner
from mmengine.runner.checkpoint import load_checkpoint

ALL_VIEWS = {'id': (), 'h': (-1,), 'v': (-2,), 'hv': (-2, -1)}


class Stats:
    """整数据集累计 TP/FP/FN，输出前景类 P/R/F1/IoU（与 mmseg IoUMetric 同口径）。"""

    def __init__(self):
        self.tp = self.fp = self.fn = 0

    def update(self, pred, gt):
        p1, g1 = pred, gt == 1
        self.tp += int((p1 & g1).sum())
        self.fp += int((p1 & ~g1).sum())
        self.fn += int((~p1 & g1).sum())

    def metrics(self):
        eps = 1e-12
        prec = self.tp / (self.tp + self.fp + eps)
        rec = self.tp / (self.tp + self.fn + eps)
        f1 = 2 * prec * rec / (prec + rec + eps)
        iou = self.tp / (self.tp + self.fp + self.fn + eps)
        return {k: round(v * 100, 2) for k, v in
                dict(P=prec, R=rec, F1=f1, IoU=iou).items()}


def fg_prob(logits):
    """(C,H,W) seg_logits -> (H,W) 前景概率。

    mmseg postprocess_result 对 out_channels==1 存的已是 sigmoid 概率，直接取用；
    多通道存的是原始 logits，取 softmax 的 class-1 通道。
    """
    if logits.shape[0] == 1:
        return logits[0]
    return logits.softmax(0)[1]


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--ckpts', nargs='+', required=True)
    ap.add_argument('--views', default='id,h,v,hv',
                    help='逗号分隔的 TTA 视角子集，如 "id" / "id,h"')
    ap.add_argument('--limit', type=int, default=0, help='仅评前 N 个样本（冒烟测试）')
    args = ap.parse_args()

    views = [ALL_VIEWS[v] for v in args.views.split(',')]

    ckpts = []
    for pat in args.ckpts:
        hits = sorted(glob.glob(pat))
        assert hits, f'no checkpoint matches {pat}'
        ckpts.extend(hits)
    print(f'members ({len(ckpts)}), views: {args.views}')
    for c in ckpts:
        print(' ', c)

    cfg = Config.fromfile(args.config)
    DefaultScope.get_instance('ensemble_eval_indomain',
                              scope_name=cfg.get('default_scope', 'opencd'))
    from opencd.registry import MODELS

    dl_cfg = cfg.val_dataloader
    dl_cfg['persistent_workers'] = False
    loader = Runner.build_dataloader(dl_cfg)

    device = 'cuda'
    models = []
    for ck in ckpts:
        m = MODELS.build(cfg.model)
        load_checkpoint(m, ck, map_location='cpu')
        models.append(m.to(device).eval())

    # 判决阈值：双通道 argmax 等价 0.5；单通道用头上的原生阈值（mmseg 默认 0.3）
    head = models[0].decode_head
    if getattr(head, 'out_channels', 2) == 1:
        thresh = getattr(head, 'threshold', None) or 0.3
    else:
        thresh = 0.5
    print(f'decision threshold on mean fg-prob: {thresh}')

    per_model = [Stats() for _ in models]   # 单模型 no-TTA（首视角，协议校验用）
    ens_first = Stats()                     # ensemble 仅首视角
    ens_all = Stats()                       # ensemble 全视角

    for bi, data in enumerate(loader):
        if args.limit and bi >= args.limit:
            break
        gt = (data['data_samples'][0].gt_sem_seg.data.squeeze(0) > 0).long()
        p_first = None   # 首视角的模型平均
        p_all = None     # 全视角 × 全模型平均
        for mi, model in enumerate(models):
            for vi, dims in enumerate(views):
                inputs = [x.flip(dims=dims) if dims else x
                          for x in data['inputs']]
                out = model.test_step(
                    {'inputs': inputs, 'data_samples': data['data_samples']})
                logits = out[0].seg_logits.data
                if dims:
                    logits = logits.flip(dims=dims)
                p = fg_prob(logits).cpu()
                p_all = p if p_all is None else p_all + p
                if vi == 0:
                    per_model[mi].update(p > thresh, gt)
                    p_first = p if p_first is None else p_first + p
        ens_first.update(p_first / len(models) > thresh, gt)
        ens_all.update(p_all / (len(models) * len(views)) > thresh, gt)
        if (bi + 1) % 50 == 0:
            print(f'  [{bi + 1}] ens_all so far: {ens_all.metrics()}', flush=True)

    first_name = args.views.split(',')[0]
    print(f'\n=== per-model (single, view={first_name}) ===')
    for ck, st in zip(ckpts, per_model):
        print(f'  {ck.split("/")[-2]}: {st.metrics()}')
    print(f'=== ensemble view={first_name} ===')
    print(' ', ens_first.metrics())
    print(f'=== ensemble views={args.views} ===')
    print(' ', ens_all.metrics())


if __name__ == '__main__':
    main()
