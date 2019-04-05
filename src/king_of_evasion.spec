# -*- mode: python -*-

block_cipher = None


a = Analysis(['king_of_evasion.py'],
             pathex=['C:\\Users\\sojin\\git\\KingOfEvasion\\src'],
             binaries=[],
             datas=[('PacManGameOver.mp3', '.'), ('TheGraveyard.mp3', '.'), ('DevilDragonBossFight.mp3', '.'), ('MikeTysonBattle.mp3', '.'), ('ForestFunk.mp3', '.'), ('Space.jpg', '.')],
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
          runtime_tmpdir=None,
          console=True )
