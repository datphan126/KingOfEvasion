# -*- mode: python -*-

block_cipher = None


a = Analysis(['bouncing_balls.py'],
             pathex=['C:\\Users\\sojin\\git\\KingOfEvasion\\src'],
             binaries=[],
             datas=[('Boo_sound_effect.mp3', '.'), ('TheGraveyard.mp3', '.'), ('DevilDragonBossFight.mp3', '.'), ('MikeTysonBattle.mp3', '.'), ('ForestFunk.mp3', '.'), ('Space.jpg', '.')],
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
          name='bouncing_balls',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
