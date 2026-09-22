import json
import sys
from pathlib import Path

from .core import audit_snapshot, load_snapshot

if len(sys.argv) != 2:
    raise SystemExit("Usage: python -m security_auditor <snapshot.txt>")
findings = audit_snapshot(load_snapshot(Path(sys.argv[1])))
print(json.dumps([finding.__dict__ for finding in findings], indent=2))
