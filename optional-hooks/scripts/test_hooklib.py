#!/usr/bin/env python3
"""Tests for hooklib's hand-written YAML parser (parse_scalar / load_config).

Dependency-free. Run from the repo root:

    python3 optional-hooks/scripts/test_hooklib.py

Covers the inline-comment footgun: a value like `adoption_manifest: false  # off`
must parse to boolean ``False`` (not the truthy string ``"false  # off"``), while
quoted regex values that legitimately contain ``#`` must survive untouched.
"""
from __future__ import annotations
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hooklib

REAL_CONFIG = Path(__file__).resolve().parent.parent / "config/hooks-config.yaml"


def test_parse_scalar_strips_inline_comment_on_bool():
    assert hooklib.parse_scalar("false   # 某注释") is False
    assert hooklib.parse_scalar("true  # keep on") is True


def test_parse_scalar_strips_inline_comment_on_int():
    assert hooklib.parse_scalar("300  # max lines") == 300


def test_parse_scalar_keeps_hash_inside_quotes():
    # A quoted scalar whose content legitimately contains ' #' must survive.
    assert hooklib.parse_scalar('"a # b"') == "a # b"


def test_parse_scalar_no_hash_unchanged():
    # Regex-ish value with no '#' is returned verbatim (no false truncation).
    assert hooklib.parse_scalar("API_KEY\\s*=") == "API_KEY\\s*="


def test_parse_scalar_hash_without_leading_space_not_a_comment():
    # Per spec: only truncate when '#' is preceded by whitespace.
    assert hooklib.parse_scalar("a#b") == "a#b"


def _load(content):
    """Run load_config against an ad-hoc config body via a temp file."""
    with tempfile.NamedTemporaryFile(
        "w", suffix=".yaml", delete=False, encoding="utf-8"
    ) as f:
        f.write(content)
        tmp = Path(f.name)
    orig = hooklib.CONFIG_PATH
    try:
        hooklib.CONFIG_PATH = tmp
        return hooklib.load_config()
    finally:
        hooklib.CONFIG_PATH = orig
        tmp.unlink()


def test_load_config_inline_comment_toggle_is_false():
    cfg = _load(
        "checks:\n"
        "  adoption_manifest: false   # turned off for now\n"
        "  secrets: true  # keep on\n"
    )
    assert cfg["checks"]["adoption_manifest"] is False, cfg["checks"]
    assert cfg["checks"]["secrets"] is True, cfg["checks"]
    # The toggle must actually disable the check via `if not cfg[...]`.
    assert not cfg["checks"]["adoption_manifest"]


def test_load_config_list_items_with_and_without_comments():
    cfg = _load(
        "secret_patterns:\n"
        "  - API_KEY\\s*=\n"
        "  - 'TOKEN\\s*='   # quoted regex, annotated\n"
    )
    # Unquoted regex with no comment: preserved verbatim.
    assert "API_KEY\\s*=" in cfg["secret_patterns"], cfg["secret_patterns"]
    # Quoted regex with a trailing comment: comment stripped, regex intact.
    assert "TOKEN\\s*=" in cfg["secret_patterns"], cfg["secret_patterns"]


def test_load_config_real_file_no_regression():
    orig = hooklib.CONFIG_PATH
    try:
        hooklib.CONFIG_PATH = REAL_CONFIG
        cfg = hooklib.load_config()
    finally:
        hooklib.CONFIG_PATH = orig
    for pat in ("API_KEY\\s*=", "SECRET\\s*=", "PRIVATE_KEY", "DATABASE_URL\\s*="):
        assert pat in cfg["secret_patterns"], (pat, cfg["secret_patterns"])
    for ph in ("TODO", "TBD", "placeholder"):
        assert ph in cfg["placeholder_patterns"], (ph, cfg["placeholder_patterns"])
    assert cfg["checks"]["owned_files"] is False
    assert cfg["checks"]["secrets"] is True
    assert cfg["mode"] == "warn"


def run():
    fns = [v for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    failures = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"FAIL {fn.__name__}: {e}")
        except Exception as e:  # noqa: BLE001 - surface any error in the harness
            failures += 1
            print(f"ERROR {fn.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(fns) - failures}/{len(fns)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
