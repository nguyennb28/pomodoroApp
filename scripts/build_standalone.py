#!/usr/bin/env python3
"""
Automated script to build a standalone single-file binary for Linux.
Produces: dist/pomodoro
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def build() -> None:
    workspace_dir = Path(__file__).resolve().parent.parent
    assets_dir = workspace_dir / "src" / "pomodoro" / "assets"
    main_py = workspace_dir / "src" / "pomodoro" / "main.py"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name",
        "pomodoro",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        f"--add-data={assets_dir}:pomodoro/assets",
        str(main_py),
    ]

    print("🚀 Starting PyInstaller build for Linux...")
    print(f"Command: {' '.join(cmd)}\n")

    res = subprocess.run(cmd, cwd=str(workspace_dir))
    if res.returncode == 0:
        dist_bin = workspace_dir / "dist" / "pomodoro"
        print("\n" + "=" * 60)
        print("🎉 Build Successful!")
        print(f"Standalone executable created at: {dist_bin}")
        print("You can distribute this file to other Linux systems without needing Python!")
        print("=" * 60)
    else:
        print("\n❌ Build failed! Please check the output above.", file=sys.stderr)
        sys.exit(res.returncode)


if __name__ == "__main__":
    build()
