#!/usr/bin/env python3
"""Check whether this computer can train a small LoRA with Apple's MLX, and which model to start with.

Usage:  python3 tools/check_machine.py [--json]
"""
import argparse
import json
import platform
import subprocess
import sys

from common import free_disk_gb

MODELS = {
    "tiny": "mlx-community/Qwen2.5-0.5B-Instruct-4bit",
    "small": "mlx-community/Qwen2.5-1.5B-Instruct-4bit",
}
MIN_FREE_GB = 5.0


def ram_gb():
    try:
        out = subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True).strip()
        return int(out) / 1024**3
    except (OSError, subprocess.CalledProcessError, ValueError):
        return None


def assess(system, machine, ram, free_gb, python_version):
    """Pure function so it can be tested. Returns a dict with a verdict and notes."""
    notes = []
    if system != "Darwin" or machine != "arm64":
        return {
            "verdict": "not_supported_here",
            "model": None,
            "notes": [
                "MLX needs a Mac with Apple Silicon (M1 or newer). This computer is "
                f"{system} {machine}.",
                "See docs/09-NOT-A-MAC.md for options. We have NOT tested them.",
            ],
        }
    if python_version < (3, 11):
        notes.append("mlx-lm 0.32 asks for Python 3.11 or newer. Make a fresh environment with uv or python.org Python.")
    if free_gb < MIN_FREE_GB:
        notes.append(f"Only {free_gb:.1f} GB free. Keep at least {MIN_FREE_GB:.0f} GB free: the model (839 MB) and the tools (367 MB) take about 1.2 GB and your Mac needs room to breathe.")
    if ram is None:
        notes.append("Could not read the memory size. Start with the tiny model.")
        model, tag = MODELS["tiny"], "UNKNOWN RAM"
    elif ram < 8:
        model, tag = MODELS["tiny"], "UNTESTED by us, expect it to be tight"
    elif ram < 16:
        model, tag = MODELS["tiny"], "UNTESTED by us, the 1.5B model may work too"
    else:
        model, tag = MODELS["small"], "TESTED by us on a 16 GB Mac (Apple M4)"
    verdict = "ok" if not notes else "ok_with_notes"
    return {"verdict": verdict, "model": model, "model_status": tag, "notes": notes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print machine readable output")
    args = parser.parse_args()
    ram = ram_gb()
    free = free_disk_gb(".")
    result = assess(
        platform.system(), platform.machine(), ram, free, sys.version_info[:2]
    )
    result.update(
        {
            "system": platform.system(),
            "machine": platform.machine(),
            "ram_gb": None if ram is None else round(ram, 1),
            "free_disk_gb": round(free, 1),
            "python": platform.python_version(),
        }
    )
    if args.json:
        print(json.dumps(result, indent=2))
        return 0 if result["verdict"] != "not_supported_here" else 1
    print(f"Computer : {result['system']} {result['machine']}")
    print(f"Memory   : {result['ram_gb']} GB")
    print(f"Free disk: {result['free_disk_gb']} GB")
    print(f"Python   : {result['python']}")
    print()
    if result["verdict"] == "not_supported_here":
        print("Verdict  : this computer cannot run the MLX path.")
    else:
        print(f"Verdict  : good to go. Start with {result['model']}")
        print(f"           ({result['model_status']})")
    for note in result["notes"]:
        print(f"Note     : {note}")
    return 0 if result["verdict"] != "not_supported_here" else 1


if __name__ == "__main__":
    sys.exit(main())
