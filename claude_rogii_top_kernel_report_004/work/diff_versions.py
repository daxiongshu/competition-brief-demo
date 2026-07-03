#!/usr/bin/env python3
"""Classify version-to-version changes for an archived kernel.

Given a dir of v<NNN>__scriptVersionId-<id>/source.ipynb, extract the code
(code cells only, outputs/exec-counts stripped) and compare consecutive
versions: identical rerun vs real edit, with +/- line counts and a code hash.
"""
import hashlib
import json
import re
import sys
import difflib
from pathlib import Path


def code_of_dir(d: Path) -> str:
    py = d / "source.py"
    nb = d / "source.ipynb"
    if nb.exists():
        return code_of(nb)
    if py.exists():
        return py.read_text().rstrip() + "\n"
    raise FileNotFoundError(f"no source in {d}")


def code_of(nb_path: Path) -> str:
    nb = json.loads(nb_path.read_text())
    cells = nb.get("cells", nb.get("worksheets", [{}])[0].get("cells", []))
    parts = []
    for c in cells:
        if c.get("cell_type") != "code":
            continue
        src = c.get("source", c.get("input", ""))
        if isinstance(src, list):
            src = "".join(src)
        parts.append(src.rstrip())
    return "\n\n".join(parts).strip() + "\n"


def norm(code: str) -> str:
    # normalize whitespace-only churn so we don't call trivial reflow a change
    lines = [ln.rstrip() for ln in code.splitlines()]
    lines = [ln for ln in lines if ln.strip() != ""]
    return "\n".join(lines)


def main():
    root = Path(sys.argv[1])
    vdirs = sorted(root.glob("v*__scriptVersionId-*"),
                   key=lambda p: int(re.match(r"v(\d+)", p.name).group(1)))
    rows = []
    prev_code = None
    prev_v = None
    for d in vdirs:
        vnum = int(re.match(r"v(\d+)", d.name).group(1))
        meta = json.loads((d / "metadata.json").read_text())
        sv = meta["selected_version"]
        score = sv.get("public_lb")
        kind = "ipynb" if (d / "source.ipynb").exists() else "py"
        code = code_of_dir(d)
        h = hashlib.sha256(norm(code).encode()).hexdigest()[:10]
        if prev_code is None:
            status = "—"
            added = removed = 0
        else:
            a = norm(prev_code).splitlines()
            b = norm(code).splitlines()
            if a == b:
                status = "IDENTICAL rerun"
                added = removed = 0
            else:
                diff = list(difflib.unified_diff(a, b, lineterm=""))
                added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
                removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
                status = "CHANGED"
        rows.append(dict(version=vnum, score=score, codehash=h, vs_prev=status,
                         added=added, removed=removed, nbytes=len(code), kind=kind))
        prev_code, prev_v = code, vnum
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
