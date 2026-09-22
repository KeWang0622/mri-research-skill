#!/usr/bin/env python3
"""Repo structure validation for CI (standard library only).

Checks:
  1. skills.sh.json is valid JSON.
  2. Every skills/<name>/SKILL.md has frontmatter with name, description,
     metadata.version, and metadata.author.
  3. The skills listed in skills.sh.json exactly match the skills/<name>/ folders.
"""
import json
import os
import sys

errors = []

# 1) skills.sh.json valid JSON
try:
    reg = json.load(open("skills.sh.json", encoding="utf-8"))
except Exception as e:  # noqa: BLE001
    print(f"::error file=skills.sh.json::invalid JSON: {e}")
    sys.exit(1)

# 2) SKILL.md frontmatter
skill_dirs = sorted(
    d for d in os.listdir("skills") if os.path.isdir(os.path.join("skills", d))
)
for d in skill_dirs:
    p = os.path.join("skills", d, "SKILL.md")
    if not os.path.isfile(p):
        errors.append(f"{p}: missing SKILL.md")
        continue
    text = open(p, encoding="utf-8").read()
    if not text.startswith("---"):
        errors.append(f"{p}: missing YAML frontmatter")
        continue
    frontmatter = text.split("---", 2)[1]
    for key in ("name:", "description:", "version:", "author:"):
        if key not in frontmatter:
            errors.append(f"{p}: frontmatter missing '{key}'")

# 3) registry <-> folder consistency
listed = {s for g in reg.get("groupings", []) for s in g.get("skills", [])}
folders = set(skill_dirs)
for miss in sorted(folders - listed):
    errors.append(f"skills.sh.json: folder '{miss}' is not listed in any grouping")
for miss in sorted(listed - folders):
    errors.append(f"skills.sh.json: lists '{miss}' but skills/{miss}/ does not exist")

if errors:
    for e in errors:
        print(f"::error::{e}")
    sys.exit(1)

print(
    f"OK: {len(skill_dirs)} skills; skills.sh.json valid; "
    "frontmatter complete; registry matches folders."
)
