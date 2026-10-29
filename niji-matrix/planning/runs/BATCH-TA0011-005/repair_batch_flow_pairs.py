"""Mechanically restore comma-separated bilingual text in this batch's flow maps."""

from pathlib import Path
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
FILES = [RUN / "defense-overrides.yaml", RUN / "T1572-formal-child-prose.yaml", RUN / "T1665-formal-child-prose.yaml", RUN / "T1659-formal-child-rewrite.yaml"]
for directory, prefixes in (
    ("detections", tuple(f"DET-{i:06d}" for i in range(257, 263))),
    ("analytics", tuple(f"NJA-{i:06d}" for i in range(343, 352))),
    ("mitigations", tuple(f"MIT-{i:06d}" for i in range(227, 232))),
):
    FILES.extend(p for p in (ROOT / directory).glob("*.yaml") if p.name.startswith(prefixes))
for prefix in ("NJT-0221", "NJT-0222", "NJT-0223", "NJT-0224"):
    FILES.extend((ROOT / "matrix/tactics/TA0011-command-and-control/techniques").glob(f"{prefix}-*/**/*.yaml"))

count = 0

def repair(value):
    global count
    if isinstance(value, list):
        return [repair(x) for x in value]
    if isinstance(value, dict):
        if "zh" in value and "en" in value and len(value) > 2:
            extra = [(k, v) for k, v in value.items() if k not in ("zh", "en")]
            if not all(v is None for _, v in extra):
                raise ValueError(extra)
            count += 1
            return {"zh": value["zh"], "en": ", ".join([value["en"], *(k for k, _ in extra)])}
        return {k: repair(v) for k, v in value.items()}
    return value

changed = []
for path in FILES:
    raw = yaml.safe_load(path.read_text())
    before = count
    fixed = repair(raw)
    if count > before:
        path.write_text(yaml.safe_dump(fixed, allow_unicode=True, sort_keys=False, width=120))
        changed.append(path.name)
print("Restored", count, "flow-map pairs in", len(changed), "batch files")
