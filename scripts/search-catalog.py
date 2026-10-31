"""Search bundled skill metadata or excluded/source-reference inventory without loading bodies."""
import argparse,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('query',nargs='?',default='');p.add_argument('--category');p.add_argument('--technology');p.add_argument('--status');p.add_argument('--references',action='store_true');p.add_argument('--json',action='store_true');a=p.parse_args()
rows=json.loads((root/('manifests/discovered-skills.json' if a.references else 'manifests/catalog.json')).read_text(encoding='utf-8'))
rows=rows['resources'] if a.references else rows['skills']
for row in rows:
    status=row.get('validation',{}).get('status',row.get('status',''))
    if a.query.casefold() not in (row['id']+' '+row['name']+' '+row.get('description','')).casefold():continue
    if a.category and row['category']!=a.category:continue
    if a.technology and a.technology not in row.get('technologies',[]):continue
    if a.status and status!=a.status:continue
    if a.json:print(json.dumps(row,ensure_ascii=True))
    else:print(f"{row['id']} [{status}] ({row['category']})")
