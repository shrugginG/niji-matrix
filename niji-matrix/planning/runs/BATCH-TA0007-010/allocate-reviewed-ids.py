"""Reserve reviewed counts through the canonical allocator, sequentially."""
from pathlib import Path
import json
import subprocess
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
assert (RUN / 'admission-and-convergence.md').is_file()
assert (RUN / 'T1018-reviewed-handoff.yaml').is_file()
destination = RUN / 'allocated-ids.json'
assert not destination.exists(), 'Refusing to allocate this batch twice'
counts = json.loads((RUN / 'allocation-counts.json').read_text())
allocated = {}
for entity, count in counts.items():
    command = [sys.executable, str(ROOT / 'scripts/allocate_id.py'), 'reserve', entity,
               '--count', str(count), '--owner', 'BATCH-TA0007-010']
    if entity == 'NJS':
        command.extend(['--parent', allocated['NJT'][0]])
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True)
    values = result.stdout.strip().splitlines()
    assert len(values) == count, result.stdout
    allocated[entity] = values
    destination.write_text(json.dumps(allocated, indent=2) + '\n')
    print(json.dumps({entity: values}), flush=True)
