"""
PyInstaller build script for the TUI application.
Delegates all bundling logic to NP-Tennis.spec.
"""

import shutil
import subprocess
import sys
from pathlib import Path


def main():
    project_root = Path(__file__).parent.absolute()
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    spec_file = project_root / "NP-Tennis.spec"

    if not spec_file.exists():
        print(f"ERROR: spec file not found at {spec_file}")
        sys.exit(1)

    # Clean previous build
    for d in (dist_dir, build_dir):
        if d.exists():
            print(f"Removing {d}")
            shutil.rmtree(d)

    cmd = ["pyinstaller", str(spec_file)]
    print(f"Running: {' '.join(cmd)}\n")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}")
        sys.exit(1)

    exe_name = "NP-Tennis.exe" if sys.platform == "win32" else "NP-Tennis"
    exe_path = dist_dir / exe_name

    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print("\nBuild successful!")
        print(f"  Output : {exe_path}")
        print(f"  Size   : {size_mb:.1f} MB")
    else:
        print("\nBuild ran but executable not found — check PyInstaller output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
