"""Apply six reviewed Chinese wording corrections without changing confidence."""
from pathlib import Path
import json
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
REPLACEMENTS = {
    '故机理为 medium。': '故对此机理保持中等置信度。',
    '因此只作 medium 的条件性结论。': '因此仅形成中等置信度的条件性结论。',
    '当前 medium 匿迹结论': '当前中等置信度的匿迹结论',
    '故置信度为 medium。': '故置信度保持中等。',
    '置信度为 medium，': '保持中等置信度，',
    '该映射为 medium：': '对此机理映射保持中等置信度：',
}
changes = []


def polish(value, filename, path=''):
    if isinstance(value, dict):
        if isinstance(value.get('zh'), str):
            old = value['zh']
            for before, after in REPLACEMENTS.items():
                value['zh'] = value['zh'].replace(before, after)
            if old != value['zh']:
                changes.append({'file': filename, 'path': path, 'before': old, 'after': value['zh']})
        for k, v in value.items():
            polish(v, filename, path + '/' + str(k))
    elif isinstance(value, list):
        for n, v in enumerate(value):
            polish(v, filename, path + '/' + str(n))


for attack in ['T1120', 'T1012']:
    path = RUN / 'reviewed-handoffs' / (attack + '.yaml')
    obj = yaml.safe_load(path.read_text())
    polish(obj, str(path.relative_to(ROOT)))
    path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120))
for relative in json.loads((RUN / 'written-object-paths.json').read_text()):
    path = ROOT / relative
    obj = yaml.safe_load(path.read_text())
    if obj['type'] not in {'technique', 'evasion-subtechnique'}:
        continue
    assert obj['lifecycle']['status'] == 'draft'
    previous = len(changes)
    polish(obj, relative)
    if len(changes) != previous:
        path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120))
assert len(changes) == 12, len(changes)
(RUN / 'reader-zh-polish.json').write_text(json.dumps(changes, ensure_ascii=False, indent=2) + '\n')
print('Six wording corrections synchronized to reviewed inputs and canonical subjects; confidence enums unchanged.')
