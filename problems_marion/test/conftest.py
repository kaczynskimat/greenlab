import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for kind in ("Modified", "Unmodified"):
    for problem in ("ValidPalindrome", "NumberOfIslands", "TransposeMatrix"):
        folder = ROOT / kind / problem
        if folder.is_dir():
            sys.path.insert(0, str(folder))
