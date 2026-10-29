"""Converge two exact URL duplicates discovered during concurrent batches."""

from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[3]
replace = {"REF-000593": "REF-000561", "REF-000612": "REF-000572"}
changed = []
for folder in ("matrix", "claims", "cases", "detections", "analytics", "mitigations", "relationships"):
    for path in (ROOT / folder).rglob("*.yaml"):
        original = path.read_text(encoding="utf-8")
        updated = original
        for old, new in replace.items():
            updated = re.sub(rf"\b{old}\b", new, updated)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))

older = next((ROOT / "references").glob("REF-000561-*.yaml"))
record = yaml.safe_load(older.read_text(encoding="utf-8"))
record["locator"] = "Purview audit operation names and caveats for repository search/read/download, SharePoint/OneDrive FileModified, FileAccessed, and FilePreviewed"
record["notes_zh"] = "支撑查询、文件访问、下载、修改和预览等操作名；实际事件的启用、延迟、预取、保留与许可须按工作负载和租户核验。"
record["notes_en"] = "Supports query, file access, download, modification, and preview operation names; verify enablement, delay, prefetch, retention, and licensing per workload and tenant."
older.write_text(yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

older = next((ROOT / "references").glob("REF-000572-*.yaml"))
record = yaml.safe_load(older.read_text(encoding="utf-8"))
record["locator"] = "Purview New-InboxRule and Set-InboxRule audit, Get-InboxRule current conditions, and distinction between rule state and matched message outcome"
record["notes_zh"] = "支撑邮箱规则创建、修改、当前谓词和审计字段；规则存在不证明任一邮件已匹配、复制或送达。"
record["notes_en"] = "Supports mailbox rule creation, modification, current predicates, and audit fields; a rule alone does not prove any message matched, was copied, or arrived."
older.write_text(yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

for duplicate in replace:
    matches = list((ROOT / "references").glob(f"{duplicate}-*.yaml"))
    for path in matches:
        path.unlink()
print(f"Repointed {len(changed)} canonical YAML files; removed duplicate REF-000593 and REF-000612 source files")
