# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for NP-Tennis.
Run with: pyinstaller NP-Tennis.spec

Dependencies sourced from pyproject.toml:
  - textual, httpx, pydantic[email], pydantic-settings, keyring
"""

from pathlib import Path
from PyInstaller.utils.hooks import collect_all, collect_submodules

project_root = Path(SPECPATH)
src_dir      = project_root / "src"
tuiapp_dir   = src_dir / "tuiapp"

binaries      = []
datas         = []
hiddenimports = []

for pkg in [
    "textual",
    "httpx",
    "pydantic",
    "pydantic_settings",
    "email_validator",
    "keyring",
    "jaraco",
    "importlib_metadata",
]:
    _d, _b, _h = collect_all(pkg)
    datas         += _d
    binaries      += _b
    hiddenimports += _h

hiddenimports += collect_submodules("tuiapp")

# Each .tcss is placed at "styles/<filename>" inside the bundle.
for tcss in tuiapp_dir.rglob("*.tcss"):
    datas.append((str(tcss), "styles"))

env_file = project_root / ".env"
if env_file.exists():
    datas.append((str(env_file), "."))

a = Analysis(
    [str(tuiapp_dir / "main.py")],
    pathex=[str(src_dir)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "unittest",
        "xmlrpc",
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="NP-Tennis",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True,
)
