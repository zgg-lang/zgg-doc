#!/usr/bin/env python3
"""校验文档中的 zgg 代码块：逐个提取并运行，报告失败。

用法:
    python3 scripts/check_examples.py [--bin /path/to/zgg]

默认从环境变量 ZGG_BIN 或 PATH 中查找 zgg。
标记为 ```text 的块会被跳过（它们是不可直接运行的片段）。
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_bin(explicit):
    if explicit:
        return explicit
    if os.environ.get("ZGG_BIN"):
        return os.environ["ZGG_BIN"]
    return shutil.which("zgg")


def iter_blocks():
    for dirpath, _, files in os.walk(ROOT):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            text = open(path, encoding="utf-8").read()
            for m in re.finditer(r"```zgg\n(.*?)```", text, re.S):
                line = text[: m.start()].count("\n") + 1
                yield os.path.relpath(path, ROOT), line, m.group(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", help="zgg executable")
    ap.add_argument("--timeout", type=float, default=20.0)
    args = ap.parse_args()

    bin_path = find_bin(args.bin)
    if not bin_path:
        sys.exit("找不到 zgg：请用 --bin 指定，或设置 ZGG_BIN / PATH")

    blocks = list(iter_blocks())
    failed = 0
    for rel, line, code in blocks:
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "case.zgg")
            open(p, "w", encoding="utf-8").write(code)
            try:
                r = subprocess.run(
                    [bin_path, p],
                    capture_output=True,
                    text=True,
                    timeout=args.timeout,
                    cwd=td,
                    env=dict(os.environ, CAN_EVAL="1"),
                )
                ok = r.returncode == 0 and "Exception!" not in r.stderr
            except subprocess.TimeoutExpired:
                ok, r = False, None
        if not ok:
            failed += 1
            print("=" * 70)
            print(f"FAIL {rel}:{line}")
            print(code)
            if r is not None:
                print("--- stderr ---")
                print(r.stderr.strip()[:800])

    print(f"\n共 {len(blocks)} 个 zgg 代码块，失败 {failed} 个")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
