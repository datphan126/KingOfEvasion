# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['king_of_evasion.py'],
             pathex=['C:\\Users\\Sojin\\git\\KingOfEvasion\\src'],
             binaries=[],
             datas=[('data\\\\sound\\\\*.mp3', 'data\\\\sound'), ('data\\\\images\\\\*.png', 'data\\\\images'), ('data\\\\images\\\\*.jpg', 'data\\\\images')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='king_of_evasion',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
