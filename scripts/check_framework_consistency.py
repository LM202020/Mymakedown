#!/usr/bin/env python3
"""Framework integrity checks for the Project Agent Workflow Framework package.

This guards the framework repo itself (not adopted target projects). Run it after
editing templates or the manifest:

    python3 scripts/check_framework_consistency.py   # or: python scripts\\check_framework_consistency.py

Checks (FAIL = exit non-zero, WARN = informational):
  1. Every Template Path in the manifest exists on disk.
  2. No stale `templates/root/` references (must be `templates/target/root/`).
  3. Handoff size numbers live only in HANDOFF_POLICY and hooks-config.yaml.
  4. Root entry/title docs declare the expected framework version.
  5. (WARN) Template files not referenced by the manifest.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_VERSION = "v7"  # bump when cutting a new framework version

MANIFEST = ROOT / "templates/FILE_ADOPTION_MANIFEST.md"
SIZE_SOURCE = ROOT / "templates/target/docs/HANDOFF_POLICY.md.template"
# Files intentionally not referenced by the manifest (package helpers / placeholders).
ORPHAN_ALLOWLIST = {
    "templates/target/root/AGENTS.append-snippet.md",
    "templates/target/root/CLAUDE.append-snippet.md",
    "templates/target/root/CODEX.append-snippet.md",
}
# Patterns for the handoff size policy numbers that must not be restated elsewhere.
SIZE_PATTERNS = [
    r"100 ?- ?200", r"80 ?- ?150",
    r"300 (?:lines|行)", r"250 (?:lines|行)",
    r"超过 ?300", r"超过 ?250", r"超过 10 条",
    r"exceeds .*?(?:300|250)", r"beyond 200",
]

fails: list[str] = []
warns: list[str] = []


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")


def text_docs() -> list[Path]:
    out = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        r = rel(p)
        if r.startswith(".git/") or "__pycache__" in r:
            continue
        if p.suffix in (".md", ".template"):
            out.append(p)
    return out


def manifest_refs() -> list[str]:
    text = MANIFEST.read_text(encoding="utf-8", errors="replace")
    return sorted(set(re.findall(r"`(templates/target/[^`]+)`", text)))


def check_manifest_refs():
    for r in manifest_refs():
        if not (ROOT / r).is_file():
            fails.append(f"[manifest-refs] {r} referenced in manifest but missing on disk")


def check_stale_paths():
    for p in text_docs():
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if "templates/root/" in line:  # correct form is templates/target/root/
                fails.append(f"[stale-path] {rel(p)}:{i} stale `templates/root/` (use templates/target/root/)")


def check_size_single_source():
    allowed = rel(SIZE_SOURCE)
    combined = re.compile("|".join(SIZE_PATTERNS))
    for p in text_docs():
        if rel(p) == allowed:
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if combined.search(line):
                fails.append(f"[size-source] {rel(p)}:{i} restates handoff size limit; reference HANDOFF_POLICY instead -> {line.strip()}")


def check_version():
    targets = [ROOT / "README.md"] + sorted((ROOT / "templates/target/root").glob("*.template"))
    pat = re.compile(r"(?:Framework|Template|framework)[ _]v(\d+)")
    expected = EXPECTED_VERSION.lstrip("v")
    for p in targets:
        if not p.is_file():
            continue
        first = p.read_text(encoding="utf-8", errors="replace").splitlines()[:1]
        if not first:
            continue
        m = pat.search(first[0])
        if m and m.group(1) != expected:
            fails.append(f"[version] {rel(p)} title declares v{m.group(1)} but expected {EXPECTED_VERSION}")


def check_orphans():
    refs = set(manifest_refs())
    for p in (ROOT / "templates/target").rglob("*.md*"):
        if not p.is_file():
            continue
        r = rel(p)
        if r in refs or r in ORPHAN_ALLOWLIST:
            continue
        if p.name == "README.md.template" and p.parent != ROOT / "templates/target/root":
            continue  # directory-placeholder READMEs
        warns.append(f"[orphan] {r} not referenced by the manifest (intentional helper? else add a row)")


def main() -> int:
    for fn in (check_manifest_refs, check_stale_paths, check_size_single_source, check_version, check_orphans):
        fn()
    for w in warns:
        print("WARN " + w)
    for f in fails:
        print("FAIL " + f)
    if fails:
        print(f"\n{len(fails)} failure(s), {len(warns)} warning(s).")
        return 1
    print(f"\nOK: framework consistency checks passed ({len(warns)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
