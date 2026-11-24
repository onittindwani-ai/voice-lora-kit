#!/usr/bin/env python3
"""Merge your adapter into one standalone model folder, the safe way.

WHY THIS WRAPPER EXISTS: in our test, merging the adapter into the compressed 4 bit model with a plain
`mlx_lm fuse` produced a model that had LOST the voice (0 of 10 style checks, the adapter alone scored
10 of 10). Merging with --dequantize kept it (10 of 10) but the folder is about 2.9 GB instead of 0.85 GB.
We believe the tiny change is rounded away when it is squeezed back into 4 bit numbers, but we did not
prove that cause. So this tool always uses --dequantize, and `docs/05` tells you to test the result.

Usage:
  python3 tools/fuse.py --model mlx-community/Qwen2.5-1.5B-Instruct-4bit \
      --adapter-path work/adapter/best --save-path work/fused-16bit
"""
import argparse
import subprocess
import sys
from pathlib import Path

from common import free_disk_gb

NEEDED_GB = 6.0


def build_command(model, adapter_path, save_path):
    return [
        sys.executable, "-m", "mlx_lm", "fuse",
        "--model", model,
        "--adapter-path", adapter_path,
        "--save-path", save_path,
        "--dequantize",
    ]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", required=True)
    p.add_argument("--adapter-path", required=True)
    p.add_argument("--save-path", default="work/fused-16bit")
    args = p.parse_args()
    if not (Path(args.adapter_path) / "adapters.safetensors").exists():
        print(f"Stop: {args.adapter_path}/adapters.safetensors not found. Use the folder train.py called best.")
        return 2
    if free_disk_gb(".") < NEEDED_GB:
        print(f"Stop: the merged model needs about 3 GB and you should keep 5 GB free. Free disk is {free_disk_gb('.'):.1f} GB.")
        return 2
    command = build_command(args.model, args.adapter_path, args.save_path)
    print("Running:", " ".join(command))
    code = subprocess.call(command)
    if code == 0:
        print(f"\nMerged model written to {args.save_path}.")
        print("Now test it before you trust it:")
        print(f"  python tools/compare.py --model {args.model} --fused-model {args.save_path} --card <your style card>")
    return code


if __name__ == "__main__":
    sys.exit(main())
