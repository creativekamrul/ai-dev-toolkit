"""Audit discovered skill files without executing or changing them. Private output only.

Usage: python scripts/audit-local.py --discovery <directory with *-paths.txt>
Filename discovery is performed separately with rg --files --hidden --no-ignore.
Metadata extraction is heuristic, not a complete YAML validator.
"""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'token-like-string': r'\b(?:sk-[A-Za-z0-9_-]{24,}|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16})\b',
    'private-key-marker': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'credential-assignment-review': r'''(?im)(?:api[_-]?key|access[_-]?token|password|client[_-]?secret)\s*[=:]\s*["']?[^\s"'${}<]{12,}''',
    'private-endpoint-review': r'https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|[^/\s]+\.(?:local|internal))\b',
    'machine-path-review': r'(?:[C-Z]:[\\/](?:Users|Projects)[\\/]|/Users/|/home/)',
}
EXEC = {'.py','.ps1','.sh','.bash','.js','.ts','.mjs','.cjs','.bat','.cmd','.exe','.dll'}
DEPENDENCIES = {'package.json','requirements.txt','pyproject.toml','Cargo.toml','go.mod','Dockerfile','uv.lock','package-lock.json','pnpm-lock.yaml'}

def findings(text):
    return [key for key, pattern in PATTERNS.items() if re.search(pattern,text)]

def safe(text):
    text = str(text)
    for pattern in PATTERNS.values():
        text = re.sub(pattern,'[REDACTED]',text)
    return text.replace('|','\\|').replace('\n',' ')

def metadata(text):
    match = re.match(r'\A\ufeff?---\s*\n(.*?)\n---\s*(?:\n|$)',text,re.S)
    if not match:
        return {}, ['missing-or-unclosed-frontmatter']
    fields = {}
    lines = match.group(1).splitlines()
    for index,line in enumerate(lines):
        m = re.match(r'^(name|description|license|author|version):\s*(.*)$',line)
        if not m: continue
        value = m[2].strip()
        if value in ('>','|','>-','|-','>+','|+',''):
            rest=[]
            for following in lines[index+1:]:
                if following and not following[0].isspace(): break
                rest.append(following.strip())
            value=' '.join(rest)
        fields[m[1]]=value.strip('\"\'')
    issues=[]
    for key in ('name','description'):
        if not fields.get(key): issues.append('missing-'+key)
    if fields.get('name') and not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',fields['name']):
        issues.append('nonstandard-name')
    if len(fields.get('name',''))>64: issues.append('name-too-long')
    return fields,issues

def category(name,description):
    label=(name+' '+description).lower()
    for cat,pattern in [
        ('wordpress',r'wordpress|\bwp-|wpds'), ('database',r'mongodb|postgres|supabase|database|sql'),
        ('design',r'figma|penpot|design|canvas|brand|typograph'),
        ('testing',r'test|qa\b|regression'),('security',r'secur|pentest|leak|vulnerab'),
        ('devops',r'cloudflare|deploy|vercel-cli|workers|wrangler|terraform|kubernetes'),
        ('frontend',r'react|frontend|nextjs|css|web-perf'),
        ('documentation',r'doc|pdf|pptx|slides|xlsx|spreadsheet|writing|content|blog|grammar'),
        ('ai',r'agent|skill|codex|claude|prompt|openai|mcp'),
        ('backend',r'api|backend|server'),('automation',r'automation|workflow')]:
        if re.search(pattern,label): return cat
    return 'utilities'

def family(path):
    s=str(path).lower().replace('\\','/')
    if '/.codex/.tmp/' in s: return 'Codex temporary plugin catalogs'
    if '/.openclaw-autoclaw/' in s: return 'OpenClaw skills and design skeletons'
    if '/.codex/plugins/' in s: return 'Codex plugin cache'
    if '/.codex/vendor_imports/' in s: return 'Codex vendor collection'
    if '/.config/goose/' in s: return 'Goose user skills'
    if '/appdata/roaming/block/goose/' in s: return 'Goose Windows application skills'
    if s.startswith('k:/.agents/'): return 'K drive shared skills'
    if '/.agents/skills/' in s and s.startswith('c:/users/'): return 'User or project .agents skills'
    if '/.codex/skills/' in s: return 'Codex user/system skills'
    if '/node_modules/' in s: return 'Dependency-bundled resources'
    if '/.git/' in s or '/.cache/' in s or '/cache/' in s: return 'Other caches'
    return 'Other local/project resources'

def run(discovery,reuse=False):
    private=ROOT/'.local'; private.mkdir(exist_ok=True)
    cached={}
    if reuse and (private/'inventory.json').is_file():
        cached={s['path']:s for s in json.loads((private/'inventory.json').read_text(encoding='utf-8'))['skills']}
    paths=set()
    for file in discovery.glob('*-paths.txt'):
        paths.update(line.strip('\ufeff\r\n') for line in file.read_text(encoding='utf-8-sig',errors='replace').splitlines() if line.strip())
    paths=sorted(paths,key=str.lower)
    sources={}
    for raw in paths:
        p=Path(raw)
        if p.name not in ('skills-lock.json','.skill-lock.json'): continue
        try:
            data=json.loads(p.read_text(encoding='utf-8-sig'))
            for name,entry in data.get('skills',{}).items():
                if isinstance(entry,dict):
                    sources.setdefault(name,[]).append({k:entry[k] for k in ('source','sourceUrl','sourceType','skillPath','skillFolderHash','computedHash') if k in entry})
        except (OSError,ValueError): pass
    skills=[]; instructions=[]; errors=[]
    for raw in paths:
        p=Path(raw)
        if p.name.lower()!='skill.md':
            if p.suffix.lower()=='.md' or p.name in ('.goosehints','.cursorrules','.mcp.json','mcp.json'):
                try:
                    text=p.read_text(encoding='utf-8-sig',errors='replace')
                    instructions.append(dict(path=raw,kind=p.name,bytes=p.stat().st_size,flags=findings(text),scope='project-or-vendor; manual review required'))
                except OSError as exc: errors.append({'path':raw,'error':type(exc).__name__})
            continue
        try:
            data=p.read_bytes(); text=data.decode('utf-8-sig',errors='replace')
            if raw in cached and cached[raw]['sha256']==hashlib.sha256(data).hexdigest():
                previous=cached[raw]; previous['family']=family(p); skills.append(previous); continue
            meta,issues=metadata(text)
            name=meta.get('name') or p.parent.name
            scripts=[]; deps=[]; licenses=[]; flags=[]; file_hashes=[]; skipped=[]
            count=0
            def onerror(exc): skipped.append(type(exc).__name__)
            for directory,dirs,files in os.walk(p.parent,followlinks=False,onerror=onerror):
                dirs[:]=[d for d in dirs if d not in ('.git','node_modules','__pycache__','.venv') and not (Path(directory)/d).is_symlink()]
                for filename in sorted(files):
                    f=Path(directory)/filename; rel=f.relative_to(p.parent).as_posix(); count+=1
                    if count>3000: skipped.append('file-limit'); break
                    if f.is_symlink(): skipped.append(rel+':symlink'); continue
                    if f.suffix.lower() in EXEC: scripts.append(rel)
                    if f.name in DEPENDENCIES: deps.append(rel)
                    if f.name.upper().startswith(('LICENSE','COPYING','NOTICE')): licenses.append(rel)
                    try:
                        if f.stat().st_size>2_000_000: skipped.append(rel+':over-2MB'); continue
                        content=f.read_bytes(); file_hashes.append((rel,hashlib.sha256(content).hexdigest()))
                        if b'\x00' not in content[:1000]:
                            found=findings(content.decode('utf-8',errors='replace'))
                            if found: flags.append({'file':rel,'kinds':found})
                    except OSError as exc: skipped.append(rel+':'+type(exc).__name__)
                if count>3000: break
            links=sorted(set(re.findall(r'https://github\.com/[\w.-]+/[\w.-]+',text)))
            skills.append(dict(path=raw,name=name,description=meta.get('description',''),category=category(name,meta.get('description','')),
                family=family(p),metadataIssues=issues,metadataValidation='heuristic-only',sha256=hashlib.sha256(data).hexdigest(),
                bundleHash=hashlib.sha256(json.dumps(sorted(file_hashes)).encode()).hexdigest(),bundleComplete=not skipped,
                scripts=scripts,dependencyFiles=deps,licenseFiles=licenses,declaredLicense=meta.get('license'),
                sourceCandidates=sources.get(name,[]),mentionedRepositories=links,flags=flags,skipped=skipped,
                reviewStatus='triaged-not-approved',executableReview='not-executed-not-reviewed'))
        except OSError as exc: errors.append({'path':raw,'error':type(exc).__name__})
    configs=[]
    home=Path.home()
    for rel in ('.codex/config.toml','.config/goose/config.yaml','.goose/config.yaml','.claude/settings.json',
                '.config/opencode/opencode.json','.config/opencode/opencode.jsonc',
                'AppData/Roaming/Block/goose/config/config.yaml','AppData/Roaming/Goose/settings.json'):
        p=home/rel
        if not p.is_file(): continue
        try:
            text=p.read_text(encoding='utf-8-sig',errors='replace')
            configs.append(dict(path=str(p),flags=findings(text),status='inspected-for-flags; values-not-exported'))
        except OSError: configs.append(dict(path=str(p),status='unreadable'))
    # Authentication files are inventoried by existence only; their contents are never read.
    for rel in ('.codex/auth.json','.codex/auth.json.backup','.aws/credentials','.ssh/id_rsa','.ssh/id_ed25519'):
        p=home/rel
        if p.is_file(): configs.append(dict(path=str(p),status='sensitive-file-present; contents-not-read; do-not-import'))
    statuses=[]
    for f in sorted(discovery.glob('*-status.json')):
        if f.name!='scan-status.json': statuses.append(json.loads(f.read_text(encoding='utf-8-sig')))
    groups=collections.defaultdict(list); names=collections.defaultdict(list)
    for s in skills: groups[s['sha256']].append(s); names[s['name']].append(s)
    summary=dict(skillFiles=len(skills),uniqueSkillBodies=len(groups),uniqueNames=len(names),
                 repeatedBodyGroups=sum(len(g)>1 for g in groups.values()),
                 nameCollisionGroups=sum(len({s['sha256'] for s in g})>1 for g in names.values()),
                 metadataFlagged=sum(bool(s['metadataIssues']) for s in skills),
                 withScripts=sum(bool(s['scripts']) for s in skills),
                 sensitivityFlagged=sum(bool(s['flags']) for s in skills),
                 instructions=len(instructions),configs=len(configs),readErrors=len(errors))
    # Store redacted descriptions/provenance, never raw matching credential-like text.
    for skill in skills:
        for field in ('description','declaredLicense'):
            if skill.get(field):
                for pattern in PATTERNS.values(): skill[field]=re.sub(pattern,'[REDACTED]',skill[field])
    result=dict(summary=summary,driveScans=statuses,skills=skills,instructions=instructions,configs=configs,readErrors=errors)
    (private/'inventory.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    lines=['# Local resource inventory','', 'Audit date: 2026-10-31 (Asia/Dhaka). **LOCAL ONLY: excluded from Git.**', '',
        'Original resources were read, never moved, overwritten or executed. Full paths and descriptions below may be private.', '',
        '## Coverage and limits','',
        'Filename discovery uses ripgrep including hidden and ignored directories on C:, E:, H:, I: and K:. '
        'Access-denied paths are recorded in the separate discovery directory. Symlinks/junctions are not followed; '
        'archives, WSL/container filesystems and unavailable cloud-only files are not unpacked or hydrated. '
        'No claim is made to inspect every document or credential on the computer. Only recognized agent-resource filenames '
        'and selected configuration files are content-audited. This is heuristic triage, not an exhaustive security or license review.', '',
        '| Drive | Matches | Error lines | Exit code |','|---|---:|---:|---:|']
    for s in statuses: lines.append(f"| {s['drive']}: | {s['matches']} | {s['error_lines']} | {s['exit_code']} |")
    lines += ['', 'A drive without a completed status is still pending or incomplete. Exit 2 means traversal encountered errors.', '', '## Totals', '']
    lines += [f'- {k}: {v}' for k,v in summary.items()]
    lines += ['', '## Main locations', '', '| Location family | Skill files |','|---|---:|']
    lines += [f'| {safe(k)} | {v} |' for k,v in collections.Counter(s['family'] for s in skills).most_common()]
    lines += ['', '### Largest skill folders', '', '| Directory | Direct child skill files |','|---|---:|']
    lines += [f'| `{safe(k)}` | {v} |' for k,v in collections.Counter(str(Path(s['path']).parent.parent) for s in skills).most_common(25)]
    lines += ['', '### Metadata findings', '', 'These are naming/required-field checks, not proof that a vendor plugin fails its own loader.', '', '| File | Findings |','|---|---|']
    lines += [f"| `{safe(s['path'])}` | {', '.join(s['metadataIssues'])} |" for s in skills if s['metadataIssues']]
    lines += ['', '## Import recommendations', '',
        '- Prioritize one reviewed copy of React/Vercel guidance, WordPress development, database guidance, testing and code review.',
        '- Keep plugin-managed skills as source references unless their exact license permits copying and tool dependencies are portable.',
        '- Keep media-center and other project instructions scoped to their original projects.',
        '- Existing frontend-design guidance favors experimental and dramatic visuals; it conflicts with the requested restrained UI default. Preserve it as an optional variant.',
        '- Review destructive git-history and skill-purge workflows individually; never activate them globally by default.',
        '- Treat lockfile origins as candidates, not proven attribution for every same-named copy. Verify against a pinned upstream revision.',
        '- Missing license evidence means hold for review, not public-domain permission.', '', '## Categorized skills', '']
    for cat in sorted(set(s['category'] for s in skills)):
        lines += [f'### {cat}', '', '| Name / description | Location | Review indicators |','|---|---|---|']
        for s in sorted((x for x in skills if x['category']==cat),key=lambda x:(x['name'],x['path'])):
            indicators=s['metadataIssues']+[f"{len(s['scripts'])} executable files",f"{len(s['dependencyFiles'])} dependency manifests",f"{len(s['flags'])} files flagged"]
            indicators += ['license evidence present' if s['licenseFiles'] or s['declaredLicense'] else 'license unresolved']
            lines.append(f"| **{safe(s['name'])}** — {safe(s['description'][:360])} | `{safe(s['path'])}` | {'; '.join(indicators)} |")
        lines.append('')
    lines += ['## Duplicate bodies', '', 'These groups have identical SKILL.md bytes; supporting assets may still differ.', '']
    for digest,group in sorted(groups.items()):
        if len(group)<2: continue
        lines += [f"- {safe(group[0]['name'])}: {len(group)} copies; SHA-256 `{digest}`"]
        lines += [f"  - `{safe(s['path'])}`" for s in group]
    lines += ['', '## Same-name variants requiring comparison', '']
    for name,group in sorted(names.items()):
        if len({s['sha256'] for s in group})>1:
            lines.append(f"- {safe(name)}: {len(group)} locations, {len({s['sha256'] for s in group})} different bodies.")
    lines += ['', '## Instructions and MCP manifests', '', 'Keep project and dependency instructions local unless reviewed for portability.', '', '| File | Flags |','|---|---|']
    lines += [f"| `{safe(i['path'])}` | {', '.join(i['flags']) or 'none detected by heuristic'} |" for i in instructions]
    lines += ['', '## Configuration and excluded credentials', '', '| File | Inspection |','|---|---|']
    lines += [f"| `{safe(c['path'])}` | {c['status']}; {', '.join(c.get('flags',[]))} |" for c in configs]
    lines += ['', '## Machine-readable detail', '',
        '`.local/inventory.json` contains full descriptions, paths, body hashes, package hashes, script/dependency/license filenames, '
        'source candidates and per-file sensitivity flag categories. It contains no credential values. '
        'Descriptions and paths are private, so this file is also excluded from Git.', '',
        'Metadata findings detect missing required fields and naming problems. Arbitrary existing YAML syntax is not fully parsed. '
        'Executable file presence is not proof of safe behavior. A dependency manifest does not enumerate every runtime tool. '
        'Bundle hashes omit files over 2 MB, linked files and excluded dependency directories; consult bundleComplete and skipped. '
        'With --reuse, unchanged entrypoints reuse the previous supporting-file snapshot; do not use that flag for a fresh package audit.', '']
    (ROOT/'docs').mkdir(exist_ok=True)
    (ROOT/'docs/LOCAL-INVENTORY.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--discovery',type=Path,required=True)
    parser.add_argument('--reuse',action='store_true',help='Reuse supporting-file audit when entrypoint hash is unchanged.')
    args=parser.parse_args(); run(args.discovery,args.reuse)
