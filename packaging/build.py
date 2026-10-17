"""Build self-contained desktop and loopback-web executables."""
from pathlib import Path
import os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];os.chdir(ROOT)
sep=';' if os.name=='nt' else ':'
def freeze(name,script,onefile=False,web=False):
    args=[sys.executable,'-m','PyInstaller','--noconfirm','--clean','--windowed','--name',name]
    if onefile:args.append('--onefile')
    if os.name=='nt':args.extend(['--icon',str(ROOT/'assets/icon.ico')])
    data=['translations.json','LICENSE','NOTICE','THIRD_PARTY.md','licenses','docs','assets']
    if web:data.append('dist/web')
    for path in data:args.extend(['--add-data',str(ROOT/path)+sep+path if (ROOT/path).is_dir() else str(ROOT/path)+sep+'.'])
    args.append(script);subprocess.run(args,check=True)
freeze('Marco Video','player.py')
for name in ['LICENSE','NOTICE','THIRD_PARTY.md','README.md']:
    shutil.copy2(ROOT/name,ROOT/'dist/Marco Video'/name)
for name in ['licenses','docs']:shutil.copytree(ROOT/name,ROOT/'dist/Marco Video'/name,dirs_exist_ok=True)
if os.name=='nt':
    freeze('Marco-Video-Portable','player.py',onefile=True)
    freeze('Marco-Video-Web-Portable','portable_web.py',onefile=True,web=True)
print('Aplicaciones compiladas.')
