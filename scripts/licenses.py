"""Preserve installed dependency notices and the open-source license texts."""
from pathlib import Path
import importlib.metadata as md
import json, shutil, urllib.request
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'licenses';folder.mkdir(exist_ok=True)
inventory=[]
for name in ('PySide6','PySide6_Essentials','PySide6_Addons','shiboken6'):
    dist=md.distribution(name)
    entry={'name':name,'version':dist.version,'license':dist.metadata.get('License'),'files':[]}
    for file in dist.files or []:
        if '/licenses/' in str(file):
            path=Path(dist.locate_file(file));target=folder/name/path.name;target.parent.mkdir(exist_ok=True);shutil.copy2(path,target);entry['files'].append(str(target.relative_to(ROOT)))
    inventory.append(entry)
(folder/'python-inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
for name,url in {
    'LGPL-3.0.txt':'https://www.gnu.org/licenses/lgpl-3.0.txt',
    'LGPL-2.1.txt':'https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt',
    'GPL-2.0.txt':'https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt',
    'FFmpeg-COPYING.LGPLv2.1':'https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.1.3/COPYING.LGPLv2.1',
}.items():
    target=folder/name
    if not target.exists():target.write_bytes(urllib.request.urlopen(url,timeout=40).read())
for name in ('@capacitor/core','@capacitor/android','@capacitor/filesystem','@capacitor/share'):
    package=ROOT/'web/node_modules'/name
    target=folder/name.replace('/','-').lstrip('@');target.mkdir(exist_ok=True)
    for p in package.iterdir():
        if p.is_file() and p.name.lower().startswith(('license','notice')):shutil.copy2(p,target/p.name)
    shutil.copy2(package/'package.json',target/'package.json')
print('Licencias y metadatos de Qt/PySide y Capacitor conservados.')
