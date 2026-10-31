"""Stage a pinned public skill collection and optionally add licensed packages to the passive library.

Never executes upstream code. Imported skills begin as screened, not behavior-reviewed.
Usage: python scripts/import-collection.py --checkout PATH --source-id NAME --repo OWNER/REPO [--apply]
"""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from toolkit_lib import metadata
from scope_policy import exclusion_reason

ROOT=Path(__file__).resolve().parents[1]
EXEC={'.py','.js','.mjs','.cjs','.ts','.ps1','.sh','.bash','.cmd','.bat','.php','.exe','.dll'}
SECRET=re.compile(rb'\b(?:sk-[A-Za-z0-9_-]{24,}|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16})\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
def hash_bytes(data):return hashlib.sha256(data).hexdigest()
def license_kind(text):
    lower=text.lower()
    if 'additional restrictions' in lower or 'all rights reserved' in lower and 'permission is hereby granted' not in lower: return None
    if 'apache license' in lower and 'version 2.0' in lower:return 'Apache-2.0'
    if 'permission is hereby granted, free of charge' in lower:return 'MIT'
    if 'gnu general public license' in lower and ('either version 2' in lower or 'version 2, june' in lower):return 'GPL-2.0-or-later'
    return None
def find_license(folder,checkout):
    for parent in [folder,*folder.parents]:
        if not parent.is_relative_to(checkout):break
        found=[p for p in parent.iterdir() if p.is_file() and p.name.lower().startswith(('license','copying'))]
        if found:
            for p in sorted(found):
                txt=p.read_text(encoding='utf-8',errors='replace'); kind=license_kind(txt)
                if kind:return kind,p.read_bytes(),p.relative_to(checkout).as_posix()
            return None,None,'restricted-or-unrecognized-license'
    return None,None,'license-text-not-found'
def category(name):
    for cat,pattern in [('wordpress','wordpress|wp-'),('database','mongo|postgres|supabase|database'),('design','design|art|theme|brand'),('testing','test|review|debug|verification'),('devops','cloudflare|deploy|worker|wrangler|git-'),('documentation','writing|doc|content|grammar|copywriting'),('frontend','react|frontend|web-'),('security','security|privacy|leak|pentest'),('ai','skill|agent|mcp')]:
        if re.search(pattern,name):return cat
    return 'utilities'
def import_source(checkout,source_id,repo,apply=False):
    if not re.fullmatch(r'[a-z0-9-]+',source_id) or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo):raise ValueError('Invalid source ID or public repository slug')
    checkout=checkout.resolve()
    revision=subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],text=True).strip()
    dirty=subprocess.check_output(['git','-C',str(checkout),'status','--porcelain'],text=True)
    if dirty.strip():raise ValueError('Use an unmodified upstream checkout')
    catalog=json.loads((ROOT/'manifests/catalog.json').read_text(encoding='utf-8'))
    existing={x['id']:x for x in catalog['skills']}; results=[];seen=set()
    paths=sorted(checkout.rglob('SKILL.md'),key=lambda p:(len(p.parts),str(p)))
    for skill_file in paths:
        relative=skill_file.relative_to(checkout).as_posix()
        if any(p in ('.git','node_modules','test','tests','fixtures','template','tools') for p in skill_file.relative_to(checkout).parts):continue
        text=skill_file.read_text(encoding='utf-8-sig');meta=metadata(text); original=meta['name']
        if original in seen:continue
        seen.add(original)
        sid=source_id+'-'+re.sub(r'[^a-z0-9-]+','-',original.lower()).strip('-')
        if len(sid)>64:sid=sid[:55]+'-'+hash_bytes(text.encode())[:8]
        row={'id':sid,'name':original,'source':f'https://github.com/{repo}','revision':revision,'upstreamPath':relative,'status':'reference-only'}
        reason=exclusion_reason(ROOT,sid,original)
        if reason:
            row['reason']=reason;results.append(row);continue
        kind,license_data,evidence=find_license(skill_file.parent,checkout)
        if not kind:
            row['reason']=evidence;results.append(row);continue
        files={};fail=None
        for f in sorted(skill_file.parent.rglob('*')):
            if f.is_symlink():fail='linked-resource';break
            if not f.is_file():continue
            rel=f.relative_to(skill_file.parent).as_posix()
            if any(p in ('.git','node_modules','__pycache__','.venv') for p in f.relative_to(skill_file.parent).parts):continue
            if f.name.startswith('.env') or f.name.lower() in ('auth.json','credentials.json') or f.suffix.lower() in ('.exe','.dll','.key','.pem'):fail='sensitive-or-binary-resource';break
            data=f.read_bytes()
            if len(data)>8_000_000:fail='large-resource-needs-review';break
            if SECRET.search(data):fail='potential-secret-needs-review';break
            if f.name.lower().startswith(('license','copying')) and not license_kind(data.decode('utf-8',errors='replace')):
                fail='nested-license-needs-review';break
            files[rel]=data
        if sum(len(v) for v in files.values())>32_000_000:fail='package-over-size-limit'
        if fail:row['reason']=fail;results.append(row);continue
        # Minimal documented portability adaptation. Preserve all other frontmatter and resources.
        adapted=re.sub(r'(?m)^name:\s*[^\n]+','name: '+sid,text,count=1)
        if source_id=='wordpress':
            adapted=re.sub(r'(?<![\w/])skills/([a-z0-9-]+)/',lambda m:'.agents/skills/wordpress-'+m[1]+'/',adapted)
        files['SKILL.md']=adapted.encode('utf-8')
        files['TOOLKIT-UPSTREAM-LICENSE.txt']=license_data
        if kind.startswith('GPL'):
            full=ROOT/'manifests/license-texts/GPL-2.0.txt'
            if not full.is_file():raise ValueError('Full GPL text is required before importing WordPress')
            files['TOOLKIT-GPL-2.0.txt']=full.read_bytes()
        executables=[p for p in files if Path(p).suffix.lower() in EXEC]
        flags=[]
        corpus='\n'.join(v.decode('utf-8',errors='ignore') for p,v in files.items() if Path(p).suffix in ('.md','.txt'))
        for flag,pattern in [('destructive-workflow',r'git (?:reset --hard|push --force)|rm -rf|Remove-Item.*Recurse'),('external-service',r'\b(?:API_KEY|access.token|oauth|MCP)\b'),('agent-framework-assumptions',r'superpowers:|subagent|Task tool|Claude Code')]:
            if re.search(pattern,corpus,re.I):flags.append(flag)
        provenance={'source':row['source'],'revision':revision,'upstreamPath':relative,'license':kind,'licenseEvidence':evidence,
                    'upstreamEntrypointSha256':hash_bytes(skill_file.read_bytes()),'localChanges':['Namespaced discovery name']+(['Adapted SKILL.md paths to installed WordPress skill locations'] if source_id=='wordpress' else []),
                    'review':{'status':'screened','scope':'license evidence, YAML, file inventory, size, executable presence and common secret patterns; no behavioral approval','executableFiles':executables,'flags':flags}}
        files['TOOLKIT-PROVENANCE.json']=(json.dumps(provenance,indent=2)+'\n').encode()
        location=f'library/community/{source_id}/{sid}'
        entry=dict(id=sid,name=sid,description=meta['description'],path=location,category=category(original),technologies=[source_id],projectTypes=['software'],
            compatibility=['portable-format; tools-may-vary'],dependencies=[str(meta.get('compatibility','Review upstream tool and runtime requirements before use'))],requires=[],
            source={'kind':'imported','attribution':repo+' contributors','url':row['source'],'upstreamRevision':revision,'licenseEvidence':evidence,'localChanges':'; '.join(provenance['localChanges'])},
            license=kind,revision=revision,validation={'status':'screened','executableReview':'pending' if executables else 'no-executables','compatibility':'YAML format checked; runtime and behavior not certified'},
            files=sorted(files),fileHashes={p:hash_bytes(v) for p,v in files.items()})
        if apply:
            dest=ROOT/location
            if sid in existing:
                if existing[sid]['revision']!=revision:raise ValueError('Existing import differs; stage an update preview instead of overwriting: '+sid)
                row['status']='already-bundled';results.append(row);continue
            if dest.exists():raise ValueError('Destination exists outside catalog: '+location)
            for p,data in files.items():
                target=dest/p;target.parent.mkdir(parents=True,exist_ok=True)
                with target.open('xb') as out:out.write(data)
            catalog['skills'].append(entry)
        row.update(status='bundled-screened' if apply else 'eligible-preview',license=kind,files=len(files),executables=len(executables),flags=flags)
        results.append(row)
    if apply:
        (ROOT/'manifests/catalog.json').write_text(json.dumps(catalog,indent=2)+'\n',encoding='utf-8')
    folder=ROOT/'manifests/imports' if apply else ROOT/'.local/import-previews';folder.mkdir(parents=True,exist_ok=True)
    (folder/(source_id+'.json')).write_text(json.dumps({'source':repo,'revision':revision,'resources':results},indent=2)+'\n',encoding='utf-8')
    return results
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--checkout',type=Path,required=True);p.add_argument('--source-id',required=True);p.add_argument('--repo',required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
    rows=import_source(a.checkout,a.source_id,a.repo,a.apply)
    from collections import Counter
    print(json.dumps(dict(Counter(r['status'] for r in rows)),indent=2))
