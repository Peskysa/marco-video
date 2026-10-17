"""Assemble a buildless web app, including offline file:// operation."""
from pathlib import Path
import json, shutil, zipfile, subprocess, os
ROOT=Path(__file__).resolve().parent.parent
web=ROOT/'web'
(web/'translations.js').write_text('globalThis.MarcoTranslations = '+(ROOT/'translations.json').read_text(encoding='utf-8')+';\n',encoding='utf-8')
dist=ROOT/'dist/web'; dist.mkdir(parents=True,exist_ok=True)
esbuild=web/'node_modules/.bin'/('esbuild.cmd' if os.name=='nt' else 'esbuild')
subprocess.run([str(esbuild),'native-entry.js','--bundle','--format=iife','--outfile=native.js'],cwd=web,check=True,shell=os.name=='nt')
for name in ['index.html','style.css','app.js','logic.js','icon.svg','translations.js','native.js']:
    shutil.copy2(web/name,dist/name)
for name in ['LICENSE','NOTICE','THIRD_PARTY.md']:
    if (ROOT/name).exists(): shutil.copy2(ROOT/name,dist/name)
if (ROOT/'docs/MANUAL.md').exists(): shutil.copy2(ROOT/'docs/MANUAL.md',dist/'MANUAL.md')
if (ROOT/'licenses').exists(): shutil.copytree(ROOT/'licenses',dist/'licenses',dirs_exist_ok=True)
target=ROOT/'dist/Marco-Video-Web.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(dist.rglob('*')):
        if p.is_file(): z.write(p,p.relative_to(dist))
print('Web offline lista: dist/web/index.html y Marco-Video-Web.zip')
