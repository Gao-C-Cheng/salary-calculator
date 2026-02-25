# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec 文件
用法: pyinstaller salary-calculator.spec
"""

import os
import sys

block_cipher = None
BASE_DIR = os.path.dirname(os.path.abspath(SPECPATH))

a = Analysis(
    [os.path.join(BASE_DIR, 'app.py')],
    pathex=[BASE_DIR],
    binaries=[],
    datas=[
        (os.path.join(BASE_DIR, 'logic'), 'logic'),
        (os.path.join(BASE_DIR, 'util'), 'util'),
        (os.path.join(BASE_DIR, 'gui'), 'gui'),
    ],
    hiddenimports=[
        'logic',
        'logic.PreDataLogic',
        'logic.OverAllDataLogic',
        'logic.PersonalDataLogic',
        'util.FileUtil',
        'util.SalaryDetailUtil',
        'util.SalaryPersonalDetailUtil',
        'openpyxl',
        'pandas',
        'xlrd',
        'PyQt5',
        'PyQt5.QtWidgets',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='salary-calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI 应用不显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
