#!/usr/bin/env python3
"""Build the standalone GPT plugin without including the Antigravity root."""

import argparse
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / 'plugins' / 'ego-flow-gpt'


def contained_file(relative):
    if not isinstance(relative, str) or not relative.startswith('./'):
        raise ValueError(f'Expected ./-prefixed plugin path: {relative!r}')
    resolved = (PLUGIN / relative).resolve()
    if not resolved.is_relative_to(PLUGIN.resolve()) or not resolved.is_file():
        raise ValueError(f'Missing or escaping plugin path: {relative}')
    return resolved


def check_package():
    data = json.loads((PLUGIN / 'plugin.json').read_text(encoding='utf-8'))
    if data.get('$schema') != 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json':
        raise ValueError('Missing portable Agent Plugins schema')
    if data.get('name') != PLUGIN.name:
        raise ValueError('Plugin name must match its folder')
    if not re.fullmatch(r'\d+\.\d+\.\d+', data.get('version', '')):
        raise ValueError('Expected strict version X.Y.Z')
    ext = data['extensions']['com.openai']
    if ext.get('requires_local_executor') is not True:
        raise ValueError('EGO requires a local executor')
    contained_file(ext['onboardingSkill'])
    interface = ext['interface']
    if not 0 < len(interface['shortDescription']) <= 30:
        raise ValueError('Listing subtitle must contain 1 to 30 characters')
    for name in ('composerIcon', 'logo'):
        contained_file(interface[name])
    skills = list((PLUGIN / 'skills').glob('*/SKILL.md'))
    if len(skills) != 3:
        raise ValueError('Expected setup, image and video skills')
    for skill in skills:
        content = skill.read_text(encoding='utf-8')
        if not content.startswith('---\n') or len(content.encode('utf-8')) > 1024 * 1024:
            raise ValueError(f'Invalid skill entry: {skill}')
    files = sorted(p for p in PLUGIN.rglob('*') if p.is_file())
    for path in PLUGIN.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Symlinks are not packaged: {path}')
    for file in files:
        if file.name in {'.DS_Store', '.env'} or '.git' in file.parts:
            raise ValueError(f'Unexpected private/generated file: {file}')
        if file.name.endswith('.md'):
            text = file.read_text(encoding='utf-8')
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in target or target.startswith('#'):
                    continue
                local = (file.parent / target.split('#', 1)[0]).resolve()
                if not local.is_relative_to(PLUGIN.resolve()) or not local.exists():
                    raise ValueError(f'Broken internal link: {file}: {target}')
    return data, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check without creating a ZIP')
    parser.add_argument('--out', type=Path, help='Output ZIP; refuses to replace an existing file')
    args = parser.parse_args()
    data, files = check_package()
    if args.check:
        print(f'Package layout and links valid: {len(files)} files, 3 skills')
        return
    out = args.out or REPO / 'dist' / f"{data['name']}-{data['version']}.zip"
    out = out.resolve()
    if out.is_relative_to(PLUGIN.resolve()):
        raise ValueError('Write the ZIP outside the plugin directory')
    out.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(out, 'x', compression=ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, (Path(PLUGIN.name) / file.relative_to(PLUGIN)).as_posix())
    with ZipFile(out) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP integrity check failed')
        manifests = [n for n in archive.namelist() if n.endswith('/plugin.json')]
        if manifests != [f'{PLUGIN.name}/plugin.json']:
            raise ValueError('Archive must contain exactly the GPT plugin')
    print(out)


if __name__ == '__main__':
    main()
