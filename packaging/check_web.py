"""Launch only the frozen localhost server, inspect it and terminate our child."""
from pathlib import Path
import json,subprocess,sys,time,urllib.request,urllib.error
root=Path(__file__).resolve().parents[1];out=root/'test-output';out.mkdir(exist_ok=True)
report=out/'web-launcher.json';report.unlink(missing_ok=True)
process=subprocess.Popen([str(Path(sys.argv[1]).resolve()),'--serve-test',str(report)])
try:
    for _ in range(100):
        if report.exists():break
        if process.poll() is not None:raise RuntimeError('Launcher exited')
        time.sleep(.2)
    data=json.loads(report.read_text());url=data['url'];assert url.startswith('http://127.0.0.1:')
    assert b'Marco V' in urllib.request.urlopen(url).read()
    for name in ['style.css','app.js','translations.js','native.js','LICENSE']:
        assert urllib.request.urlopen(url+name).status==200,name
    try:urllib.request.urlopen(urllib.request.Request(url,data=b'test',method='POST'))
    except urllib.error.HTTPError as e:assert e.code==501
    else:raise AssertionError('POST unexpectedly accepted')
    print('Portable web: recursos incluidos, localhost y servidor de lectura comprobados.')
finally:
    process.terminate()
    try:process.wait(timeout=10)
    except subprocess.TimeoutExpired:process.kill();process.wait()
