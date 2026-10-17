from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1];dist=root/'dist';dist.mkdir(exist_ok=True)
files=[root/n for n in ['README.md','LICENSE','NOTICE','THIRD_PARTY.md','CHANGELOG.md','SECURITY.md','CONTRIBUTING.md']]
for name in ['docs','licenses','assets']:files.extend(p for p in (root/name).rglob('*') if p.is_file())
with zipfile.ZipFile(dist/'Marco-Video-Documentacion.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(root))
print(f'{len(files)} archivos de documentación y capturas empaquetados.')
