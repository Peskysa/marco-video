"""Verify the collection contract and assemble release documentation/source/hashes."""
from pathlib import Path
import argparse, hashlib, json, subprocess, zipfile
ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT/'project.json').read_text(encoding='utf-8'))
DOCS = ['README.md','INSTALACION.md','MANUAL.md','DESARROLLO.md','PRIVACIDAD.md','CAPTURAS.md','LICENCIA.md','DISTRIBUCION.md']

def check():
    required = ['README.md','LICENSE','NOTICE','THIRD_PARTY.md','CHANGELOG.md','CONTRIBUTING.md','SECURITY.md','project.json','.github/workflows/release.yml']
    required += ['docs/'+p for p in DOCS]
    required += ['docs/images/'+p+'.png' for p in ['escritorio','funcion','movil']]
    for p in required:
        if not (ROOT/p).is_file() or not (ROOT/p).stat().st_size: raise SystemExit('Falta: '+p)
    if CONFIG['license'] != 'AGPL-3.0-only': raise SystemExit('Licencia diferente')
    if CONFIG['modalities'] != ['linux','windows','portable','web','android']: raise SystemExit('Modalidades diferentes')
    if 'GNU AFFERO GENERAL PUBLIC LICENSE' not in (ROOT/'LICENSE').read_text(): raise SystemExit('Texto de licencia incorrecto')
    package = ROOT/CONFIG['package']
    meta = json.loads(package.read_text(encoding='utf-8'))
    if meta['version'] != CONFIG['version'] or meta['license'] != CONFIG['license']: raise SystemExit('Versión/licencia incoherente en package.json')
    print(CONFIG['name']+': estructura, licencia, capturas y cinco modalidades verificadas.')

def docs():
    target=ROOT/'dist'/(CONFIG['prefix']+'-Documentacion.zip');target.parent.mkdir(exist_ok=True)
    files=[ROOT/p for p in ['README.md','LICENSE','NOTICE','THIRD_PARTY.md','CHANGELOG.md','CONTRIBUTING.md','SECURITY.md','project.json']]
    for folder in ['docs','assets','licenses']:
        if (ROOT/folder).exists():files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file())
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(set(files)):z.write(p,p.relative_to(ROOT))
    print(target.name)

def finalize(folder):
    import shutil
    check();docs();folder=Path(folder);folder.mkdir(exist_ok=True)
    prefix=CONFIG['prefix']
    shutil.copy2(ROOT/'dist'/(prefix+'-Documentacion.zip'),folder)
    source=folder/(prefix+'-Source.zip')
    subprocess.run(['git','archive','--format=zip','--prefix='+CONFIG['slug']+'/','--output='+str(source.resolve()),'HEAD'],cwd=ROOT,check=True)
    required=[prefix+s for s in ['-Windows-Instalador.exe','-Portable.exe','-Web-Portable.exe','-Linux-amd64.deb','-Linux-Portable.tar.gz','-Web.zip','-Android.apk','-Documentacion.zip','-Source.zip']]
    for name in required:
        if not (folder/name).is_file() or not (folder/name).stat().st_size:raise SystemExit('Publicación incompleta: '+name)
    forbidden=('.p12','.jks','.keystore','.env')
    with zipfile.ZipFile(source) as z:
        for name in z.namelist():
            if name.endswith(forbidden) or '/.signing/' in name:raise SystemExit('Secreto en fuente: '+name)
    lines=[]
    for p in sorted(folder.iterdir()):
        if p.is_file() and p.name!='SHA256SUMS.txt':
            with p.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
            lines.append(digest+'  '+p.name)
    (folder/'SHA256SUMS.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Nueve paquetes completos y sumas SHA-256 verificados.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['check','docs','finalize']);parser.add_argument('folder',nargs='?',default='artifacts');args=parser.parse_args()
    if args.action=='check':check()
    elif args.action=='docs':docs()
    else:finalize(args.folder)
