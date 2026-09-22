import json
import sys
from pathlib import Path

from .core import find_matches, normalize

if len(sys.argv) != 3:
    raise SystemExit("Usage: python -m threat_intel <ioc-file> <evidence-file>")
iocs = normalize(Path(sys.argv[1]).read_text(encoding="utf-8").splitlines())
evidence = Path(sys.argv[2]).read_text(encoding="utf-8")
print(json.dumps({"indicators": [item.__dict__ for item in iocs],
                  "matches": [item.__dict__ for item in find_matches(evidence, iocs)]},
                 indent=2))
