"""Restore comma-separated English text accidentally parsed as YAML flow-map keys."""

from pathlib import Path
import yaml

path = Path(__file__).resolve().parent / "T1573-research-handoff.yaml"
root = yaml.safe_load(path.read_text())
count = 0

def repair(value):
    global count
    if isinstance(value, list):
        return [repair(item) for item in value]
    if isinstance(value, dict):
        if "zh" in value and "en" in value and len(value) > 2:
            extra = [(k, v) for k, v in value.items() if k not in ("zh", "en")]
            if not all(v is None for _, v in extra):
                raise ValueError(extra)
            en = ", ".join([value["en"], *(k for k, _ in extra)])
            count += 1
            return {"zh": value["zh"], "en": en}
        return {k: repair(v) for k, v in value.items()}
    return value

fixed = repair(root)
path.write_text(yaml.safe_dump(fixed, allow_unicode=True, sort_keys=False, width=120))
print("Restored", count, "bilingual inline mappings")
