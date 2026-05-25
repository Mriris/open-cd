#!/usr/bin/env python
"""动态 GPU 队列调度: 哪张卡空了(mem<2GB 且未被本队列占用)就launch下一个待跑任务.
并发<=len(GPUS); 处理 mtkd_step3 对 step1+3teachers 的依赖(完成后自动填 ckpt 路径).
单卡用 torch.distributed.run --nproc_per_node=1 --launcher pytorch (SyncBN 兼容)."""
import subprocess, time, os, glob, sys

ROOT = '/mnt/data2/jingwei/yantingxuan/0Program/HeteCD2GOLD'
OPENCD = f'{ROOT}/open-cd'
PY = f'{ROOT}/.conda_opencd/bin/python'
CFG = 'configs/hcd3s_xiongan'
WORKROOT = f'{OPENCD}/work_dirs/hcd3s_xiongan'
LOGDIR = '/tmp/opencd_train'
GPUS = [0, 1, 2, 3]
EXTRA20K = ['train_cfg.max_iters=20000', 'train_cfg.val_interval=2000',
            'param_scheduler.1.end=20000', 'default_hooks.checkpoint.interval=2000']
os.chdir(OPENCD)

# (name, config, deps)
JOBS = [
    ('lightcdnet',              f'{CFG}/lightcdnet_512x512_40k.py', []),
    ('tinycd_v2',               f'{CFG}/tinycd_v2_512x512_40k.py', []),
    ('ban',                     f'{CFG}/ban_vit-b16-clip_mit-b0_512x512_40k.py', []),
    ('ttp',                     f'{CFG}/ttp_vit-sam-l_512x512_40k.py', []),
    ('mtkd_step1_initial',      f'{CFG}/mtkd/mtkd_step1_initial.py', []),
    ('mtkd_step2_teacher_small',  f'{CFG}/mtkd/mtkd_step2_teacher_small.py', []),
    ('mtkd_step2_teacher_medium', f'{CFG}/mtkd/mtkd_step2_teacher_medium.py', []),
    ('mtkd_step2_teacher_large',  f'{CFG}/mtkd/mtkd_step2_teacher_large.py', []),
    ('mtkd_step3_distill',      f'{CFG}/mtkd/mtkd_step3_distill.py',
     ['mtkd_step1_initial', 'mtkd_step2_teacher_small', 'mtkd_step2_teacher_medium', 'mtkd_step2_teacher_large']),
]

def gpu_free_mem():
    out = subprocess.run(['nvidia-smi', '--query-gpu=index,memory.used',
                          '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout
    m = {}
    for line in out.strip().splitlines():
        i, used = [x.strip() for x in line.split(',')]
        m[int(i)] = int(used)
    return m

def best_ckpt(name):
    c = sorted(glob.glob(f'{WORKROOT}/{name}/best_mIoU_*.pth'), key=os.path.getmtime)
    return c[-1] if c else None

def build_extra(name):
    opts = list(EXTRA20K)
    if name == 'mtkd_step3_distill':
        st = best_ckpt('mtkd_step1_initial'); tl = best_ckpt('mtkd_step2_teacher_large')
        tm = best_ckpt('mtkd_step2_teacher_medium'); ts = best_ckpt('mtkd_step2_teacher_small')
        if not all([st, tl, tm, ts]):
            return None
        opts += [f'model.init_cfg.checkpoint={st}', f'model.init_cfg_t_l.checkpoint={tl}',
                 f'model.init_cfg_t_m.checkpoint={tm}', f'model.init_cfg_t_s.checkpoint={ts}']
    return ['--cfg-options'] + opts

def launch(name, cfg, gpu, port):
    extra = build_extra(name)
    log = open(f'{LOGDIR}/{name}.log', 'w')
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(gpu))
    cmd = [PY, '-m', 'torch.distributed.run', '--nproc_per_node=1', f'--master_port={port}',
           f'{OPENCD}/tools/train.py', cfg, '--work-dir', f'{WORKROOT}/{name}',
           '--launcher', 'pytorch'] + extra
    p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env)
    print(f'[{time.strftime("%H:%M:%S")}] LAUNCH {name} on GPU{gpu} port{port} pid{p.pid}', flush=True)
    return p

pending = list(JOBS)
running = {}   # gpu -> (name, popen)
done = set()
port0 = 29660
pi = 0
while pending or running:
    # reap
    for g in list(running):
        nm, p = running[g]
        if p.poll() is not None:
            done.add(nm)
            print(f'[{time.strftime("%H:%M:%S")}] DONE  {nm} (GPU{g}, rc={p.returncode})', flush=True)
            del running[g]
    # schedule
    mem = gpu_free_mem()
    busy_gpus = set(running)
    for g in GPUS:
        if g in busy_gpus:
            continue
        if mem.get(g, 9999) >= 2000:   # 被别的进程(如changestar/外部)占用
            continue
        # 找一个deps已满足的待跑任务
        idx = next((k for k, (nm, cfg, deps) in enumerate(pending) if all(d in done for d in deps)), None)
        if idx is None:
            continue
        nm, cfg, deps = pending.pop(idx)
        if nm == 'mtkd_step3_distill' and build_extra(nm) is None:
            print(f'[WARN] {nm} 依赖 ckpt 缺失, 跳过', flush=True); done.add(nm); continue
        running[g] = (nm, launch(nm, cfg, g, port0 + pi)); pi += 1
    time.sleep(20)
print(f'[{time.strftime("%H:%M:%S")}] ===== QUEUE ALL DONE: {sorted(done)} =====', flush=True)
