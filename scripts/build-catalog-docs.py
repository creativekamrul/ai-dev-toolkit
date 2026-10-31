"""Generate searchable Markdown catalog and attribution from the bundled manifest."""
import collections,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'manifests/catalog.json').read_text(encoding='utf-8'))
counts=collections.Counter(s['validation']['status'] for s in catalog['skills'])
lines=['# Bundled skill catalog','',f"{len(catalog['skills'])} actual skill packages: {counts['reviewed']} reviewed defaults/choices and {counts['screened']} screened optional packages.",'','Screened packages need task-specific tool, path and executable review before use. The library is passive; selecting a project does not activate every skill.','','Search: `python scripts/search-catalog.py <query> [--category design] [--status reviewed]`.','']
for category in sorted({s['category'] for s in catalog['skills']}):
    lines += ['## '+category,'','| Skill | Status | Origin |','|---|---|---|']
    for s in sorted((s for s in catalog['skills'] if s['category']==category),key=lambda s:s['id']):
        lines.append(f"| [{s['id']}](../{s['path']}/SKILL.md) | {s['validation']['status']} | {s['source']['kind']} |")
    lines.append('')
(root/'docs/CATALOG.md').write_text('\n'.join(lines),encoding='utf-8')
lines=['# Third-party attribution','','Each bundled package retains its license and provenance. Toolkit MIT licensing does not replace upstream terms.','','| Package | License | Attribution | Source |','|---|---|---|']
for s in catalog['skills']:
    if s['source']['kind']=='original':continue
    url=s['source'].get('url','');source=f'[source]({url})' if url else 'Local snapshot; see preserved evidence'
    lines.append(f"| [{s['id']}]({s['path']}/TOOLKIT-PROVENANCE.json) | {s['license']} | {s['source']['attribution'].replace('|','/')} | {source} |")
(root/'THIRD-PARTY-NOTICES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f"Generated catalog and attribution for {len(catalog['skills'])} packages.")
