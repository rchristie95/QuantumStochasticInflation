"""Atomic publication helper; the short talk is one continuous scene."""
import json
from pathlib import Path

def atomic_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(value,indent=2),encoding="utf-8")
    tmp.replace(path)
