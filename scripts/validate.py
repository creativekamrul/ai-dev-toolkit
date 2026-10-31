"""Validate catalog schema, YAML, immutable file lists, presets, styles and obvious secrets."""
import hashlib,json,os,re,sys
from pathlib import Path
from toolkit_lib import metadata
import jsonschema
ROOT=Path(__file__).resolve().parents[1]

def contained(root,relative):
    p=Path(relative)
    if p.is_absolute() or '..' in p.parts or '\\' in relative:raise ValueError('unsafe path')
    target=(root/p).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():raise ValueError('missing/escaping file: '+relative)
    return target

def validate(root=ROOT):
    errors=[]
    catalog=json.loads((root/'manifests/catalog.json').read_text(encoding='utf-8'))
    schema=json.loads((root/'manifests/catalog.schema.json').read_text())
    for e in jsonschema.Draft202012Validator(schema).iter_errors(catalog):errors.append('schema: '+e.message)
    ids=set();names=set();known=set()
    for item in catalog['skills']:
        try:
            if item['id'] in ids or item['name'] in names:raise ValueError('duplicate id/name')
            ids.add(item['id']);names.add(item['name'])
            path=contained(root,item['path']+'/SKILL.md');known.add(path)
            meta=metadata(path.read_text(encoding='utf-8-sig'))
            if meta['name']!=item['name'] or meta['description']!=item['description']:raise ValueError('metadata differs from catalog')
            if path.parent.name!=item['name']:raise ValueError('folder differs from name')
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',item['name']) or len(item['name'])>64:raise ValueError('invalid name')
            if set(item['files'])!=set(item['fileHashes']):raise ValueError('file/hash set mismatch')
            actual={p.relative_to(path.parent).as_posix() for p in path.parent.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
            if actual!=set(item['files']):raise ValueError('unlisted/missing package files')
            for rel in item['files']:
                f=contained(path.parent,rel)
                if f.name=='SKILL.md':known.add(f.resolve())
                if hashlib.sha256(f.read_bytes()).hexdigest()!=item['fileHashes'][rel]:raise ValueError('hash mismatch: '+rel)
            if not any('license' in f.lower() for f in item['files']):raise ValueError('license text missing')
            if item['source']['kind']=='imported' and (not item['source'].get('url') or not re.fullmatch(r'[a-f0-9]{40}',item['source'].get('upstreamRevision',''))):raise ValueError('missing pinned provenance')
            if item['validation']['status']=='reviewed' and item['validation']['executableReview']=='pending':raise ValueError('reviewed skill has pending executable review')
            if item['validation']['status']=='reviewed':
                text=path.read_text(encoding='utf-8')
                for link in re.findall(r'\]\(([^)]+)\)',text):
                    if not re.match(r'(https?://|#)',link):contained(path.parent,link.split('#')[0])
        except (ValueError,OSError,KeyError,TypeError) as exc:errors.append(f"{item.get('id','?')}: {exc}")
    actual={p.resolve() for base in ('library/skills','library/community','library/local') for p in (root/base).rglob('SKILL.md')}
    if actual!=known:errors.append('unlisted/missing SKILL.md')
    entries={s['id']:s for s in catalog['skills']}
    for e in catalog['skills']:
        if any(s not in ids for s in e.get('requires',[])):errors.append(e['id']+': unknown dependency')
    for base in ('presets','styles'):
        for p in (root/base).glob('*.json'):
            try:
                data=json.loads(p.read_text())
                if data['id']!=p.stem:raise ValueError('filename/id mismatch')
                for sid in data['skills']:
                    if sid not in ids or entries[sid]['validation']['status']!='reviewed':raise ValueError('defaults must use reviewed known skills: '+sid)
                contained(root,data['instructions'])
            except (ValueError,OSError,KeyError) as exc:errors.append(f'{p.name}: {exc}')
    secret=re.compile(rb'\b(?:sk-[A-Za-z0-9_-]{24,}|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16})\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
    for directory,dirs,files in os.walk(root):
        dirs[:]=[d for d in dirs if d not in ('.git','.local','__pycache__','staging','generated')]
        for name in files:
            p=Path(directory)/name;rel=p.relative_to(root)
            if name=='LOCAL-INVENTORY.md':continue
            if name.startswith('auth.json') or name.startswith('.env') and name!='.env.example':errors.append('private filename: '+str(rel))
            if secret.search(p.read_bytes()):errors.append('possible secret: '+str(rel))
    return errors
if __name__=='__main__':
    errors=validate()
    if errors:print('\n'.join(errors));sys.exit(1)
    print('PASS: JSON Schema, YAML, IDs, file hashes, licenses, default selections and obvious-secret checks.')
