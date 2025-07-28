# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=['.', 'src', 'src/speech2text'],
    binaries=[],
    datas=[
        ('src/speech2text/*.py', 'speech2text'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk', 
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'openai',
        'pyaudio',
        'cryptography',
        'cryptography.fernet',
        'numpy',
        'pynput',
        'pynput.keyboard',
        'pynput.mouse',
        'threading',
        'tempfile',
        'wave',
        'json',
        'base64',
        'hashlib',
        'pathlib',
        'ctypes',
        'ctypes.wintypes',
        'platform',
        'time',
        'datetime',
        'math',
        'os',
        'sys',
        'speech2text',
        'speech2text.modern_speech_app',
        'speech2text.settings',
        'speech2text.theme',
        'speech2text.audio_monitor', 
        'speech2text.global_hotkey',
        'speech2text.animations',
        'speech2text.modern_settings_dialog'
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
    name='Speech2Text',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to .ico file if you have one
    version_info={
        'version': '0.1.0',
        'description': 'Modern Speech-to-Text Application',
        'product_name': 'Speech2Text',
        'file_description': 'Speech2Text - Modern Desktop Application',
        'company_name': 'Speech2Text Contributors',
        'copyright': '(C) 2025 Speech2Text Contributors'
    }
)
