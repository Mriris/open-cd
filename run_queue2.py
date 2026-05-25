#!/usr/bin/env python
"""接管剩余: 3 个 MTKD teacher + TTP + MTKD step3(蒸馏).
step3 在 step1(孤儿进程在跑) + 3 teacher 的 best_mIoU ckpt 都就绪后才launch(否则推迟,不跳过).
哪张卡空(mem<2GB 且未被本队列占用)就塞下一个; 单卡 torchrun --launcher pytorch."""
import subprocess, time, os, glob
ROOT = '/mnt/data2/jingwei/yantingxuan/0Program/HeteCD2GOLD'
OPENCD = f'{ROOT}/open-cd'; PY = f'{ROOT}/.conda_opencd/bin/python'
CFG = 'configs/hcd3s_xiongan'; WORKROOT = f'{OPENCD}/work_dirs/hcd3s_xiongan'; LOGDIR = '/tmp/opencd_train'
GPUS = [0, 1, 2, 3]
EXTRA20K = ['train_cfg.max_iters=20000', 'train_cfg.val_interval=2000',
            'param_scheduler.1.end=20000', 'default_hooks.checkpoint.interval=2000']
os.chdir(OPENCD)
JOBS = [
    ('mtkd_step2_teacher_small',  f'{CFG}/mtkd/mtkd_step2_teacher_small.py', []),
    ('mtkd_step2_teacher_medium', f'{CFG}/mtkd/mtkd_step2_teacher_medium.py', []),
    ('mtkd_step2_teacher_large',  f'{CFG}/mtkd/mtkd_step2_teacher_large.py', []),
    ('ttp',                       f'{CFG}/ttp_vit-sam-l_512x512_40k.py', []),
    ('mtkd_step3_distill',        f'{CFG}/mtkd/mtkd_step3_distill.py',
     ['mtkd_step2_teacher_small', 'mtkd_step2_teacher_medium', 'mtkd_step2_teacher_large']),
]

def gpu_free():
    out = subprocess.run(['nvidia-smi', '--query-gpu=index,memory.used',
                          '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout
    return {int(l.split(',')[0]): int(l.split(',')[1]) for l in out.strip().splitlines()}

def best(name):
    c = sorted(glob.glob(f'{WORKROOT}/{name}/best_mIoU_*.pth'), key=os.path.getmtime)
    return c[-1] if c else None

def build_extra(name):
    opts = list(EXTRA20K)
    if name == 'mtkd_step3_distill':
        st, tl = best('mtkd_step1_initial'), best('mtkd_step2_teacher_large')
        tm, ts = best('mtkd_step2_teacher_medium'), best('mtkd_step2_teacher_small')
        if not all([st, tl, tm, ts]):
            return None   # 推迟(step1 或 teacher 未就绪)
        opts += [f'model.init_cfg.checkpoint={st}', f'model.init_cfg_t_l.checkpoint={tl}',
                 f'model.init_cfg_t_m.checkpoint={tm}', f'model.init_cfg_t_s.checkpoint={ts}']
    return ['--cfg-options'] + opts

def launch(name, cfg, gpu, port):
    log = open(f'{LOGDIR}/{name}.log', 'w')
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(gpu))
    cmd = [PY, '-m', 'torch.distributed.run', '--nproc_per_node=1', f'--master_port={port}',
           f'{OPENCD}/tools/train.py', cfg, '--work-dir', f'{WORKROOT}/{name}',
           '--launcher', 'pytorch'] + build_extra(name)
    p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env)
    print(f'[{time.strftime("%H:%M:%S")}] LAUNCH {name} GPU{gpu} port{port} pid{p.pid}', flush=True)
    return p

pending = list(JOBS); running = {}; done = set(); port0 = 29700; pi = 0
while pending or running:
    for g in list(running):
        nm, p = running[g]
        if p.poll() is not None:
            done.add(nm); print(f'[{time.strftime("%H:%M:%S")}] DONE {nm} GPU{g} rc={p.returncode}', flush=True); del running[g]
    mem = gpu_free()
    for g in GPUS:
        if g in running or mem.get(g, 9999) >= 2000:
            continue
        idx = next((k for k, (nm, c, deps) in enumerate(pending)
                    if all(d in done for d in deps) and build_extra(nm) is not None), None)
        if idx is None:
            continue
        nm, c, deps = pending.pop(idx)
        running[g] = (nm, launch(nm, c, g, port0 + pi)); pi += 1
    time.sleep(20)
print(f'[{time.strftime("%H:%M:%S")}] ===== QUEUE2 ALL DONE: {sorted(done)} =====', flush=True)
