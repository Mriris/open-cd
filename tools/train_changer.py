#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
单独训练 Changer 模型的脚本。
功能等价于 bash 脚本中：
    python tools/train.py configs/custom/changer_custom.py --work-dir ./work_dirs/custom12/changer
提供可选参数以对齐 tools/train.py：
    --work-dir, --resume, --amp, --cfg-options, --launcher

新增参数：
    --use-ac-dataset  使用 A/C 数据集配置（configs/custom/changer_custom_ac.py）
    --gpu-devices     设置 CUDA_VISIBLE_DEVICES（默认 2）
    --work-subdir     仅指定子目录名
"""
import argparse
import os
import subprocess
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='单独训练 Changer 模型')
    parser.add_argument('--use-ac-dataset', action='store_true', default=False,
                        help='使用 A/C 数据集（configs/custom/changer_custom_ac.py）')
    parser.add_argument('--work-dir', type=str, default='./work_dirs/custom13',
                        help='保存日志与权重的目录（绝对或相对路径）')
    parser.add_argument('--work-subdir', type=str, default='changer',
                        help='与 --work-dir 互斥；将作为 ./work_dirs/custom12/<subdir>')
    parser.add_argument('--resume', action='store_true', default=False,
                        help='自动从最新权重恢复训练')
    parser.add_argument('--amp', action='store_true', default=False,
                        help='启用混合精度训练')
    parser.add_argument('--cfg-options', nargs='+', default=None,
                        help='以 key=val 形式覆盖配置，同 tools/train.py')
    parser.add_argument('--launcher', choices=['none', 'pytorch', 'slurm', 'mpi'],
                        default='none', help='分布式启动器')
    parser.add_argument('--gpu-devices', type=str, default=os.environ.get('GPU_DEVICES', '0'),
                        help='CUDA_VISIBLE_DEVICES 设置')
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # 设置 GPU 可见性
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu_devices)
    print(f"已设置 CUDA_VISIBLE_DEVICES={os.environ['CUDA_VISIBLE_DEVICES']}")

    # 选择配置文件
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    cfg_rel = 'configs/custom/changer_custom_ac.py' if args.use_ac_dataset else 'configs/custom/changer_custom.py'
    cfg_path = os.path.join(repo_root, cfg_rel)
    if not os.path.exists(cfg_path):
        print(f'配置文件不存在：{cfg_path}', file=sys.stderr)
        return 1

    # 确定工作目录
    if args.work_dir is not None:
        work_dir = args.work_dir
    else:
        work_dir = os.path.join(repo_root, 'work_dirs', 'custom12', args.work_subdir)
    os.makedirs(work_dir, exist_ok=True)

    # 组装命令，透传到 tools/train.py
    train_py = os.path.join(repo_root, 'tools', 'train.py')
    cmd = [sys.executable, train_py, cfg_path, '--work-dir', work_dir]
    if args.resume:
        cmd.append('--resume')
    if args.amp:
        cmd.append('--amp')
    if args.launcher and args.launcher != 'none':
        cmd.extend(['--launcher', args.launcher])
    if args.cfg_options:
        cmd.extend(['--cfg-options'] + list(args.cfg_options))

    print(f'运行命令: {" ".join(cmd)}')
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except KeyboardInterrupt:
        return 130


if __name__ == '__main__':
    sys.exit(main())


