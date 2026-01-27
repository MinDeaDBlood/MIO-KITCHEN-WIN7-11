# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = []
datas += collect_data_files('sv_ttk')
datas += collect_data_files('chlorophyll')

# Добавляем все Python файлы из src как data files
import os
for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            datas.append((filepath, root))

# Собираем все подмодули src
hiddenimports_src = collect_submodules('src')


a = Analysis(
    ['tool.py'],
    pathex=['.', 'src', 'src/core', 'src/tkui', 'src/porttool'],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'tkinter', 
        'PIL', 
        'PIL._tkinter_finder',
        'requests',
        'zstandard',
        'protobuf',
    ] + hiddenimports_src,
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'PyQt5', 'PyQt6'],
    noarchive=False,
)
pyz = PYZ(a.pure)
splash = Splash(
    'splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    splash,
    splash.binaries,
    [],
    name='tool',
    debug=False,  # Отключаем debug режим для релиза
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Отключаем UPX - может вызывать проблемы
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Отключаем консоль для GUI приложения
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
