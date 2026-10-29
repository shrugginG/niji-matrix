"""Build an atomic, validated website snapshot from the canonical YAML tree."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from datetime import datetime, timezone
import yaml

WEB = Path(__file__).resolve().parents[1]
ROOT = Path(os.environ.get('NIJI_MATRIX_ROOT', WEB.parent / 'niji-matrix')).resolve()
OUT = Path(os.environ.get('NIJI_DATA_OUT', WEB / 'public' / 'data')).resolve()
LOCATIONS = ['matrix.yaml', 'matrix', 'mechanisms', 'references', 'claims', 'cases', 'detections', 'analytics', 'mitigations', 'relationships']

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, default=str), encoding='utf-8')
    temp.replace(path)

def read_inputs():
    files = {}
    for loc in LOCATIONS:
        base = ROOT / loc
        paths = [base] if base.is_file() else sorted(base.rglob('*.yaml'))
        for path in paths:
            files[path] = path.read_bytes()
    return files

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        inputs = read_inputs()
        spec = importlib.util.spec_from_file_location('niji_validator', ROOT / 'scripts/validate.py')
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        log = io.StringIO()
        with contextlib.redirect_stdout(log):
            result = validator.main()
        if result:
            raise ValueError(log.getvalue())
        if inputs != read_inputs():
            raise ValueError('内容在校验期间发生变化，正在等待下一轮校验。')
        objects = {}
        digest = hashlib.sha256()
        digest.update(Path(__file__).read_bytes())
        for path, raw in inputs.items():
            digest.update(str(path.relative_to(ROOT)).encode() + raw)
            obj = yaml.safe_load(raw)
            if not isinstance(obj, dict) or not isinstance(obj.get('id'), str):
                raise ValueError(f'缺少对象 ID：{path}')
            if obj['id'] in objects:
                raise ValueError(f'重复 ID：{obj["id"]}')
            obj['_source'] = str(path.relative_to(ROOT))
            objects[obj['id']] = obj
        revision = digest.hexdigest()[:16]
        reverse = {key: set() for key in objects}
        def refs(value, source):
            if isinstance(value, dict):
                for key, child in value.items():
                    if key not in ('id', '_source'): refs(child, source)
            elif isinstance(value, list):
                for child in value: refs(child, source)
            elif isinstance(value, str) and value in reverse and value != source:
                reverse[value].add(source)
        for key, obj in objects.items(): refs(obj, key)
        summaries = {}
        for key, obj in objects.items():
            summaries[key] = {field: obj[field] for field in ['id','type','name','name_zh','name_en','title_zh','title_en','summary','classification','parent_ref','lifecycle','aliases','statement_zh','statement_en','description_zh','description_en','publisher','published','source_type','analytic_refs','url','archive_url','source'] if field in obj}
            summaries[key]['mechanism_refs'] = [m['mechanism_ref'] for m in obj.get('stealth_mechanisms', [])]
            summaries[key]['children'] = sorted(k for k,v in objects.items() if v.get('parent_ref') == key)
        stage = Path(tempfile.mkdtemp(dir=OUT, prefix='.stage-'))
        try:
            for key, obj in objects.items():
                write(stage / 'objects' / f'{key}.json', {**obj, '_reverse': sorted(reverse[key])})
            index = {'revision':revision, 'generated_at':datetime.now(timezone.utc).isoformat(), 'matrix':objects['niji-matrix'], 'objects':summaries}
            write(stage / 'index.json', index)
            target = OUT / revision
            if target.exists(): shutil.rmtree(stage)
            else: stage.rename(target)
            write(OUT / 'status.json', {'ok':True,'revision':revision,'generated_at':index['generated_at'],'warnings':[line for line in log.getvalue().splitlines() if line.startswith('WARNING:')]})
        finally:
            if stage.exists(): shutil.rmtree(stage)
        print(f'已生成 {len(objects)} 个对象，版本 {revision}')
        return 0
    except Exception as exc:
        write(OUT / 'status.json', {'ok':False,'message':str(exc),'checked_at':datetime.now(timezone.utc).isoformat()})
        print(str(exc), file=sys.stderr)
        return 1

if __name__ == '__main__': sys.exit(main())
