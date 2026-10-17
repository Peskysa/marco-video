"""Preserve Qt 6.10.3 upstream attribution records and referenced license files.

Run only when updating dependencies; requires authenticated gh or public API access.
These upstream records can include optional Qt features beyond the modules deployed.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path,PurePosixPath
import base64,json,posixpath,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
GH=shutil.which('gh') or 'D:/PROGRAMAS/tools/gh/bin/gh.exe'
def api(path):return json.loads(subprocess.check_output([GH,'api',path],text=True,encoding='utf-8'))
def get_file(repo,path):
    target=ROOT/'licenses/qt-upstream'/repo/path
    if target.exists():return path,target.read_bytes()
    result=api(f'repos/qt/{repo}/contents/{path}?ref=v6.10.3')
    data=base64.b64decode(result['content'])
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    return path,data
count=0
for repo in ['qtbase','qtmultimedia','qtsvg']:
    tree=api(f'repos/qt/{repo}/git/trees/v6.10.3?recursive=1')['tree']
    available={entry['path'] for entry in tree if entry['type']=='blob'}
    paths=[p for p in available if p.startswith('LICENSES/') or (p.startswith('src/') and p.endswith('qt_attribution.json'))]
    with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(lambda p:get_file(repo,p),sorted(paths)))
    references=set()
    for path,data in results:
        if not path.endswith('qt_attribution.json'):continue
        records=json.loads(data,strict=False)
        if isinstance(records,dict):records=[records]
        for record in records:
            value=record.get('LicenseFile',[])
            for file in ([value] if isinstance(value,str) else value):
                candidate=posixpath.normpath(str(PurePosixPath(path).parent/file))
                if candidate in available and candidate not in paths:references.add(candidate)
    with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(lambda p:get_file(repo,p),sorted(references)))
    count+=len(paths)+len(references)
print(f'{count} textos de licencia y registros de atribución Qt 6.10.3 conservados.')
