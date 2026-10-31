"""Small, explicit skill routing rules; no service, model or package dependency."""
import json
from pathlib import Path


def rules(root):
    return json.loads((Path(root)/'manifests/curation.json').read_text(encoding='utf-8'))


def validate_selection(root, selected, preset, style, database, capabilities=()):
    policy=rules(root)
    unknown=set(capabilities)-set(policy['capabilities'])
    if unknown:raise ValueError('Unknown capabilities: '+', '.join(sorted(unknown)))
    for sid in selected:
        rule=policy['skills'].get(sid,{})
        if rule.get('stacks') and preset not in rule['stacks']:
            raise ValueError(f'{sid} does not match stack {preset}')
        if rule.get('styles') and style not in rule['styles']:
            raise ValueError(f'{sid} does not match style {style}')
        if rule.get('databases') and database not in rule['databases']:
            raise ValueError(f'{sid} needs one of these databases: '+', '.join(rule['databases']))
        if set(rule.get('conflicts',[])) & set(selected):
            raise ValueError(f'Conflicting skill selection: {sid}')
    return policy


def recommendations(root, preset, style, database='none', capabilities=()):
    root=Path(root);policy=rules(root)
    unknown=set(capabilities)-set(policy['capabilities'])
    if unknown:raise ValueError('Unknown capabilities: '+', '.join(sorted(unknown)))
    selected={}
    def add(ids,reason):
        for sid in ids:selected.setdefault(sid,[]).append(reason)
    for folder,key in [('presets',preset),('styles',style)]:
        # IDs come from actual files, never interpolated traversal paths.
        available={p.stem:p for p in (root/folder).glob('*.json')}
        if key not in available:raise ValueError('Unknown '+folder+': '+key)
        add(json.loads(available[key].read_text(encoding='utf-8'))['skills'],folder+': '+key)
    options=json.loads((root/'manifests/project-options.json').read_text(encoding='utf-8'))
    if database not in options['databases']:raise ValueError('Unknown database: '+database)
    add(options['databases'][database]['skills'],'database: '+database)
    for cap in capabilities:add(policy['capabilities'][cap]['skills'],'capability: '+cap)
    validate_selection(root,selected,preset,style,database,capabilities)
    return [{'id':sid,'reasons':selected[sid]} for sid in sorted(selected)]
