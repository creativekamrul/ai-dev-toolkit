"""Copy reusable licensed local skill packages into the portable library; keep paths private.

Requires a private inventory produced by audit-local.py. No upstream script is executed.
Run after auditing: python scripts/import-local.py --inventory .local/inventory.json --apply
"""
import argparse,collections,hashlib,importlib.util,json,re
from pathlib import Path
from toolkit_lib import metadata
from scope_policy import exclusion_reason
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('collection_import',Path(__file__).with_name('import-collection.py'))
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def h(data):return hashlib.sha256(data).hexdigest()
def license_record(skill,evidence):
    if evidence!=skill:
        return {'kind':'license-file','filename':evidence.name,'sha256':h(evidence.read_bytes())}
    for parent in [skill.parent,*list(skill.parent.parents)[:6]]:
        manifest=parent/'.codex-plugin/plugin.json'
        if manifest.is_file():
            plugin=json.loads(manifest.read_text(encoding='utf-8-sig'))
            if plugin.get('license') in ('MIT','Apache-2.0'):
                author=plugin.get('author',{})
                return {'kind':'plugin-license-declaration','manifestSha256':h(manifest.read_bytes()),
                        'declaration':{k:plugin[k] for k in ('name','version','license') if k in plugin},
                        'author':author.get('name','') if isinstance(author,dict) else str(author)}
        if parent.name in ('.codex','.agents','.config') or (parent/'.git').exists():break
    return {'kind':'skill-license-declaration','entrypointSha256':h(skill.read_bytes()),
            'license':metadata(skill.read_text(encoding='utf-8-sig')).get('license')}

def license_evidence(skill):
    declaration=None; attribution=None; public_url=None
    for parent in [skill.parent,*list(skill.parent.parents)[:6]]:
        licenses=[p for p in parent.glob('*') if p.is_file() and p.name.lower().startswith(('license','copying'))]
        if licenses:
            for p in licenses:
                data=p.read_bytes();kind=mod.license_kind(data.decode('utf-8',errors='replace'))
                if kind:return kind,data,attribution or 'Original authors; see preserved license and notices',public_url,p,parent
            return None,None,None,None,None,None
        manifest=parent/'.codex-plugin/plugin.json'
        if manifest.is_file():
            try:
                plugin=json.loads(manifest.read_text(encoding='utf-8-sig'));declaration=plugin.get('license');author=plugin.get('author',{})
                attribution=author.get('name') if isinstance(author,dict) else str(author)
                url=plugin.get('repository','')
                if isinstance(url,str) and url.startswith('https://github.com/') and '/openai/openai' not in url and '/oai-maintained-' not in url:public_url=url
            except (ValueError,OSError):pass
            if declaration and declaration not in ('MIT','Apache-2.0'):return None,None,None,None,None,None
            if declaration:break
        if parent.name in ('.codex','.agents','.config') or (parent/'.git').exists():break
    if declaration is None:
        try:declaration=metadata(skill.read_text(encoding='utf-8-sig')).get('license')
        except (ValueError,OSError):pass
    if declaration in ('MIT','Apache-2.0'):
        if declaration=='MIT':
            # The source declaration grants MIT; preserve its actual authorship, without
            # inventing a new copyright year or applying the toolkit's copyright to it.
            standard=(ROOT/'LICENSE').read_text().split('Permission is hereby granted',1)[1]
            data=('MIT License\n\nUpstream attribution: '+(attribution or 'See original skill metadata and preserved notices')+'\n\nPermission is hereby granted'+standard).encode()
        else:data=(ROOT/'manifests/license-texts/Apache-2.0.txt').read_bytes()
        return declaration,data,attribution or 'Original skill authors',public_url,skill,skill.parent
    return None,None,None,None,None,None

def run(inventory_file,apply):
    inv=json.loads(inventory_file.read_text(encoding='utf-8'))
    catalog=json.loads((ROOT/'manifests/catalog.json').read_text());existing={s['id']:s for s in catalog['skills']}
    decisions=[];private=[];seen=set()
    # Prefer a normal reusable installation over a cached copy of identical content.
    source_rows=sorted(inv['skills'],key=lambda s:('node_modules' in s['path'],'.codex\\.tmp' in s['path'],s['path']))
    for source in source_rows:
        raw=source['path'];file=Path(raw)
        if source['sha256'] in seen:continue
        if not file.is_file():continue
        normalized=raw.lower().replace('\\','/')
        user_root=Path.home().as_posix().lower()
        reusable=any(x in normalized for x in ('/.config/goose/','/appdata/roaming/block/goose/','/.codex/plugins/','/.codex/.tmp/plugins/','/.codex/skills/.system/','/.openclaw-autoclaw/')) or bool(re.match(r'^[a-z]:/\.agents/',normalized)) or normalized.startswith(user_root+'/.agents/') or normalized.startswith(user_root+'/.codex/skills/')
        if any(part in ('fixtures','tests','test','examples') for part in normalized.split('/')):reusable=False
        row={'entrypointSha256':source['sha256'],'name':source['name'],'status':'excluded','reason':'project-specific-or-dependency-location'}
        if not reusable:
            private.append(dict(row,path=raw));continue
        try:meta=metadata(file.read_text(encoding='utf-8-sig'))
        except Exception:
            row['reason']='invalid-metadata';decisions.append(row);continue
        key='local-'+re.sub(r'[^a-z0-9-]+','-',meta['name'].lower()).strip('-')
        key=key[:54].strip('-')+'-'+source['sha256'][:8]
        excluded=exclusion_reason(ROOT,key,meta['name'])
        if excluded:
            row['reason']=excluded;decisions.append(row);seen.add(source['sha256']);continue
        kind,license_data,author,url,evidence,bound=license_evidence(file)
        if not kind:
            row['reason']='license-unresolved-or-restricted';decisions.append(row);continue
        files={};reason=None
        for p in sorted(file.parent.rglob('*')):
            if p.is_symlink():reason='linked-resources';break
            if not p.is_file():continue
            rel=p.relative_to(file.parent).as_posix()
            if any(part in ('.git','node_modules','__pycache__','.venv') for part in p.relative_to(file.parent).parts):continue
            if p.name.startswith('.env') or p.name.lower() in ('auth.json','credentials.json') or p.suffix.lower() in ('.exe','.dll','.key','.pem'):reason='private-or-binary-resource';break
            data=p.read_bytes()
            if len(data)>8_000_000:reason='large-asset-needs-review';break
            if mod.SECRET.search(data):reason='potential-secret';break
            if p.suffix.lower() in ('.md','.json','.yaml','.yml','.toml','.ps1','.sh','.py','.js','.mjs','.txt','.html'):
                text=data.decode('utf-8',errors='replace')
                private_path=re.escape(str(Path.home())).replace(r'\\',r'[\\/]')
                if re.search(private_path,text,re.I) or re.search(r'https?://[^\s/]+\.(?:internal|corp)(?:/|\b)',text,re.I):reason='machine-specific-or-private-content';break
            if p.name.lower().startswith(('license','copying')) and not mod.license_kind(data.decode('utf-8',errors='replace')):reason='nested-license-needs-review';break
            files[rel]=data
        if sum(map(len,files.values()))>32_000_000:reason='large-package-needs-review'
        if reason:row['reason']=reason;decisions.append(row);continue
        text=file.read_text(encoding='utf-8-sig')
        files['SKILL.md']=re.sub(r'(?m)^name:\s*[^\n]+','name: '+key,text,count=1).encode('utf-8')
        files['TOOLKIT-UPSTREAM-LICENSE.txt']=license_data
        files['TOOLKIT-LICENSE-EVIDENCE.json']=(json.dumps(license_record(file,evidence),indent=2)+'\n').encode('utf-8')
        # Preserve attribution from an enclosing collection, including OpenCoworkAI's notice.
        for ancestor in [file.parent,*file.parent.parents]:
            if not ancestor.is_relative_to(bound):break
            for notice in ancestor.glob('NOTICE*'):
                if notice.is_file():files['TOOLKIT-NOTICE-'+h(notice.read_bytes())[:8]+notice.suffix]=notice.read_bytes()
        if kind.startswith('GPL'):files['TOOLKIT-GPL-2.0.txt']=(ROOT/'manifests/license-texts/GPL-2.0.txt').read_bytes()
        executables=[p for p in files if Path(p).suffix.lower() in mod.EXEC]
        provenance={'kind':'local-import','originalName':meta['name'],'originalEntrypointSha256':source['sha256'],
                    'source':url,'attribution':author,'license':kind,'licenseEvidence':'Preserved skill/collection license or explicit skill/plugin SPDX declaration',
                    'localChanges':['Namespaced discovery name; retained supporting files and notices'],
                    'review':{'status':'screened','executableFiles':executables,'scope':'Local snapshot; licensing and static privacy screening. Host-tool and cross-skill references require review before activation.'}}
        files['TOOLKIT-PROVENANCE.json']=(json.dumps(provenance,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
        location='library/local/'+key
        entry={'id':key,'name':key,'description':meta['description'],'path':location,'category':source['category'],'technologies':['local-collection'],'projectTypes':['software'],
               'compatibility':['portable-format; original-host-tools-may-be-required'],'dependencies':['Review original host tools, cross-skill paths and runtime requirements before activation'],'requires':[],
               'source':{'kind':'local-import','attribution':author,'url':url or '', 'localChanges':'Namespaced skill name; original local files preserved'},
               'license':kind,'revision':'sha256:'+source['sha256'],'validation':{'status':'screened','executableReview':'pending' if executables else 'no-executables','compatibility':'Actual local package copied; no runtime compatibility guarantee'},
               'files':sorted(files),'fileHashes':{p:h(v) for p,v in files.items()}}
        if apply and key not in existing:
            dest=ROOT/location
            if dest.exists():raise ValueError('Uncataloged destination exists: '+key)
            for rel,data in files.items():
                target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True)
                with target.open('xb') as output:output.write(data)
            catalog['skills'].append(entry);existing[key]=entry
        row.update(id=key,status='bundled' if apply else 'eligible',reason='',license=kind,files=len(files))
        decisions.append(row);private.append(dict(row,path=raw));seen.add(source['sha256'])
    if apply:
        (ROOT/'manifests/catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        (ROOT/'manifests/local-imports.json').write_text(json.dumps({'resources':decisions},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        registry=json.loads((ROOT/'manifests/discovered-skills.json').read_text())
        bundled={r['entrypointSha256']:r['id'] for r in decisions if r['status']=='bundled'}
        for resource in registry['resources']:
            if resource['entrypointSha256'] in bundled:
                resource['status']='bundled-local';resource['bundledSkill']=bundled[resource['entrypointSha256']];resource['note']='Actual reusable local skill package is included, with supporting files and attribution.'
        (ROOT/'manifests/discovered-skills.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (ROOT/'.local/local-import-decisions.json').write_text(json.dumps(private,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(dict(collections.Counter((r['status']+':'+r['reason']).rstrip(':') for r in decisions)),indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--inventory',type=Path,required=True);parser.add_argument('--apply',action='store_true');a=parser.parse_args();run(a.inventory,a.apply)
