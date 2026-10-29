#!/usr/bin/env python3
"""Repair unquoted English commas in research-only flow maps; no prose is added."""
from pathlib import Path
import yaml
RUN=Path(__file__).resolve().parent
NAMES=["T1080","T1091","T1210","T1534","T1563"]
META={"key","control_type","disposition","object","resolution","confidence","role","target_ref","mechanism_ref","temporary_key"}
def repair(v):
    count=0
    if isinstance(v,dict):
        if "en" in v and "zh" in v:
            extras=[k for k in list(v) if k not in META and k not in {"zh","en"}]
            for key in extras:
                if v[key] is not None: raise ValueError((key,v[key]))
            if extras:
                if not isinstance(v["en"],str):raise ValueError(v)
                v["en"]=v["en"]+", "+", ".join(extras)
                for key in extras:del v[key]
                count+=1
        for value in v.values():count+=repair(value)
    elif isinstance(v,list):
        for value in v:count+=repair(value)
    return count
for name in NAMES:
    path=RUN/f"{name}-handoff.yaml"
    data=yaml.safe_load(path.read_text())
    count=repair(data)
    if count:
        path.write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False,width=120))
    print(name,count)
