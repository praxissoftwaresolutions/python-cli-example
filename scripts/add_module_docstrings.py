#!/usr/bin/env python3
"""
Add a simple module docstring to all .py files in the repository that are missing one.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
IGNORE_DIRS = {'venv', 'env', '.venv', '.env', '__pycache__', '.git', 'node_modules'}

def should_skip(path):
    return any(part in IGNORE_DIRS for part in path.parts)

def has_module_docstring(lines):
    i = 0
    if i < len(lines) and lines[0].startswith('#!'):
        i = 1
    if i < len(lines) and re.search(r'coding[:=]\s*', lines[i]):
        i += 1
    while i < len(lines) and lines[i].strip() == '':
        i += 1
    return i < len(lines) and lines[i].lstrip().startswith(('"""', "'''"))

def make_docstring(path):
    rel = path.relative_to(ROOT)
    return f'"""{rel.as_posix()} module."""\n\n'

changed = []
for p in ROOT.rglob('*.py'):
    if should_skip(p):
        continue
    text = p.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=True)
    if not lines:
        continue
    if has_module_docstring(lines):
        continue
    # find insertion index (after shebang/encoding and initial blank lines)
    i = 0
    if i < len(lines) and lines[0].startswith('#!'):
        i = 1
    if i < len(lines) and re.search(r'coding[:=]\s*', lines[i]):
        i += 1
    while i < len(lines) and lines[i].strip() == '':
        i += 1
    doc = make_docstring(p)
    new_text = ''.join(lines[:i]) + doc + ''.join(lines[i:])
    p.write_text(new_text, encoding='utf-8')
    changed.append(str(p.relative_to(ROOT)))

if changed:
    print("Added module docstrings to:")
    for c in changed:
        print(" -", c)
else:
    print("No files needed changes.")