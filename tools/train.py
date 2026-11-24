#!/usr/bin/env python3
"""Run one LoRA training with safe defaults, and write down what really happened.

This is a thin wrapper around Apple's `mlx_lm.lora`. It checks disk space, runs the
training, keeps the full log, and saves run-summary.json with the time, peak memory,
loss numbers and adapter size, so you can see what the run cost and compare runs.

Usage:
  python3 tools/train.py --model mlx-community/Qwen2.5-1.5B-Instruct-4bit \
      --data work/data --adapter-path work/adapter
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from common import free_disk_gb

ANSI = re.compile(r"\x1b\[[0-9;]*m")
# mlx-lm 0.32 prints a table:  "   25    val 0.943    3.40s"  and  "   30    0.675 ▼    31    5.9k"
VAL_ROW = re.compile(r"^\s*(\d+)\s+val\s+([\d.]+)")
TRAIN_ROW = re.compile(r"^\s*(\d+)\s+([\d.]+)\s+[▼▲=]?\s*(\d+)\s+[\d.]+k?\s*$")
FOOTPRINT = re.compile(r"(\d+)\s+peak memory footprint")
MIN_FREE_GB = 3.0


def build_command(args):
    return [
        sys.executable, "-m", "mlx_lm", "lora",
        "--model", args.model,
        "--train",
        "--data", args.data,
        "--adapter-path", args.adapter_path,
        "--iters", str(args.iters),
        "--batch-size", str(args.batch_size),
        "--num-layers", str(args.num_layers),
        "--learning-rate", str(args.learning_rate),
        "--max-seq-length", str(args.max_seq_length),
        "--steps-per-report", str(args.report_every),
        "--steps-per-eval", str(args.eval_every),
        "--save-every", str(args.save_every),
        "--seed", str(args.seed),
        "--mask-prompt",
    ] + (["--grad-checkpoint"] if args.grad_checkpoint else [])


def parse_log(lines):
    """Pull the numbers out of the mlx-lm log. Pure function so it can be tested."""
    train, val, footprint = [], [], 0
    for raw in lines:
        line = ANSI.sub("", raw)
        m = VAL_ROW.match(line)
        if m:
            val.append((int(m.group(1)), float(m.group(2))))
            continue
        m = TRAIN_ROW.match(line)
        if m:
            train.append((int(m.group(1)), float(m.group(2))))
        m = FOOTPRINT.search(line)
        if m:
            footprint = max(footprint, int(m.group(1)))
    return {
        "train_loss": train,
        "val_loss": val,
        "peak_memory_gb": round(footprint / 1024**3, 2) if footprint else None,
    }


def keep_best_checkpoint(adapter_dir, best_iter):
    """Copy the checkpoint with the lowest validation loss into <adapter>/best so you can use it."""
    adapter_dir = Path(adapter_dir)
    source = adapter_dir / f"{best_iter:07d}_adapters.safetensors"
    if not source.exists():
        return None
    best = adapter_dir / "best"
    best.mkdir(exist_ok=True)
    shutil.copyfile(source, best / "adapters.safetensors")
    shutil.copyfile(adapter_dir / "adapter_config.json", best / "adapter_config.json")
    return str(best)


def adapter_size_mb(folder):
    files = list(Path(folder).glob("adapters.safetensors"))
    return round(sum(f.stat().st_size for f in files) / 1024**2, 2)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", default="mlx-community/Qwen2.5-1.5B-Instruct-4bit")
    p.add_argument("--data", default="work/data")
    p.add_argument("--adapter-path", default="work/adapter")
    p.add_argument("--iters", type=int, default=60)
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--num-layers", type=int, default=16)
    p.add_argument("--learning-rate", type=float, default=1e-5)
    p.add_argument("--max-seq-length", type=int, default=1024)
    p.add_argument("--report-every", type=int, default=10)
    p.add_argument("--eval-every", type=int, default=10)
    p.add_argument("--save-every", type=int, default=10)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--grad-checkpoint", action="store_true", help="use less memory, run slower")
    args = p.parse_args()

    if free_disk_gb(".") < MIN_FREE_GB:
        print(f"Stop: only {free_disk_gb('.'):.1f} GB free disk. Free some space first.")
        return 2
    for name in ("train", "valid"):
        if not (Path(args.data) / f"{name}.jsonl").exists():
            print(f"Stop: {args.data}/{name}.jsonl is missing. Run tools/build_dataset.py first.")
            return 2

    Path(args.adapter_path).mkdir(parents=True, exist_ok=True)
    command = build_command(args)
    timer = ["/usr/bin/time", "-l"] if Path("/usr/bin/time").exists() else []
    log_path = Path(args.adapter_path) / "training.log"
    print("Running:", " ".join(command))
    started = time.time()
    lines = []
    with open(log_path, "w", encoding="utf-8") as log:
        env = dict(os.environ, PYTHONUNBUFFERED="1")
        proc = subprocess.Popen(timer + command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
        for line in proc.stdout:
            lines.append(line)
            log.write(line)
            print(line, end="")
        code = proc.wait()
    seconds = round(time.time() - started, 1)
    if code != 0:
        print(f"Training stopped with exit code {code}. The log is in {log_path}.")
        return code

    parsed = parse_log(lines)
    best_iter = min(parsed["val_loss"], key=lambda t: t[1])[0] if parsed["val_loss"] else None
    best_dir = keep_best_checkpoint(args.adapter_path, best_iter) if best_iter else None
    summary = {
        "model": args.model,
        "iters": args.iters,
        "batch_size": args.batch_size,
        "num_layers": args.num_layers,
        "learning_rate": args.learning_rate,
        "seconds": seconds,
        "peak_memory_gb": parsed["peak_memory_gb"],
        "first_val_loss": parsed["val_loss"][0][1] if parsed["val_loss"] else None,
        "best_val_loss": min((v for _, v in parsed["val_loss"]), default=None),
        "best_val_iter": best_iter,
        "best_adapter_folder": best_dir,
        "last_val_loss": parsed["val_loss"][-1][1] if parsed["val_loss"] else None,
        "last_train_loss": parsed["train_loss"][-1][1] if parsed["train_loss"] else None,
        "adapter_mb": adapter_size_mb(args.adapter_path),
        "command": command[2:],
    }
    (Path(args.adapter_path) / "run-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("\nRun summary:")
    print(json.dumps({k: v for k, v in summary.items() if k != "command"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
