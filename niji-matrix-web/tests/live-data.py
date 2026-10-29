"""Exercise export updates and failed validation in a temporary content copy."""
import json, os, pathlib, shutil, subprocess, tempfile
web=pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='niji-web-test-') as tmp:
 root=pathlib.Path(tmp)/'matrix'
 shutil.copytree(web.parent/'niji-matrix',root,ignore=shutil.ignore_patterns('dist','planning','__pycache__'))
 out=pathlib.Path(tmp)/'data'
 env={**os.environ,'NIJI_MATRIX_ROOT':str(root),'NIJI_DATA_OUT':str(out)}
 matrix=root/'matrix.yaml'; original=matrix.read_text()
 matrix.write_text(original.replace('name_zh: 匿迹技战术矩阵','name_zh: 内容同步测试矩阵'))
 assert subprocess.run(['python3','scripts/export.py'],cwd=web,env=env).returncode==0
 status=json.loads((out/'status.json').read_text()); revision=status['revision']
 index=json.loads((out/revision/'index.json').read_text())
 assert index['matrix']['name_zh']=='内容同步测试矩阵'
 matrix.write_text(original.replace('id: niji-matrix','id: invalid-matrix-id'))
 result=subprocess.run(['python3','scripts/export.py'],cwd=web,env=env,capture_output=True)
 assert result.returncode!=0
 status=json.loads((out/'status.json').read_text());assert status['ok'] is False
 assert (out/revision/'index.json').exists(), 'Previous valid snapshot must remain available'
 matrix.write_text(original)
 assert subprocess.run(['python3','scripts/export.py'],cwd=web,env=env).returncode==0
 status=json.loads((out/'status.json').read_text());assert status['ok'] is True
 index=json.loads((out/status['revision']/'index.json').read_text());assert index['matrix']['name_zh']=='匿迹技战术矩阵'
 print('PASS: content edits exported, schema failure visible, last valid snapshot retained, recovery successful')
