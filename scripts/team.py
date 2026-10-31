"""Small-team task ledger. No AI services, credentials or third-party dependencies."""
import argparse,json,os
from pathlib import Path

ROLES=('planner','designer','builder','reviewer')
TRANSITIONS={'todo':{'doing','blocked'},'doing':{'review','blocked'},'blocked':{'todo'},'review':{'doing','done','blocked'},'done':set()}

def normalized_path(value):
    p=Path(value)
    if p.is_absolute() or '..' in p.parts or '\\' in value or ':' in value:raise ValueError('Owned paths must be relative portable paths')
    return p.as_posix().rstrip('/')

def overlap(a,b):
    a=a.casefold().rstrip('/');b=b.casefold().rstrip('/')
    return a=='.' or b=='.' or a==b or a.startswith(b+'/') or b.startswith(a+'/')

def change(data,command,task_id,**args):
    tasks=data['tasks'];by_id={t['id']:t for t in tasks}
    if command=='add':
        if task_id in by_id:raise ValueError('Task ID already exists')
        if args['owner'] not in ROLES:raise ValueError('Unknown role')
        if any(dep not in by_id for dep in args['dependencies']):raise ValueError('Dependency must be an existing task')
        if not args['acceptance']:raise ValueError('Acceptance criteria are required')
        tasks.append({'id':task_id,'title':args['title'],'owner':args['owner'],'status':'todo','dependencies':args['dependencies'],
                      'ownedPaths':[normalized_path(p) for p in args['paths']],'acceptanceCriteria':args['acceptance'],'evidence':[]})
        return
    if task_id not in by_id:raise ValueError('Unknown task')
    task=by_id[task_id];status=args['status']
    if status not in TRANSITIONS[task['status']]:raise ValueError('Invalid task state transition')
    if status=='doing':
        if any(by_id[d]['status']!='done' for d in task['dependencies']):raise ValueError('Dependencies are not done')
        for other in tasks:
            if other['id']==task_id or other['status'] not in ('doing','review'):continue
            if any(overlap(a,b) for a in task['ownedPaths'] for b in other['ownedPaths']):raise ValueError('Owned paths overlap an active task: '+other['id'])
    if status in ('review','done') and not args.get('evidence'):raise ValueError('Evidence is required for review/completion')
    if status=='done' and args.get('reviewer') not in ('reviewer','self-review'):raise ValueError('Record reviewer or self-review explicitly')
    if args.get('evidence'):task['evidence'].append({'status':status,'note':args['evidence'],'reviewer':args.get('reviewer')})
    task['status']=status

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--project',type=Path,default=Path.cwd())
    sub=parser.add_subparsers(dest='command',required=True);sub.add_parser('status')
    add=sub.add_parser('add');add.add_argument('--id',required=True);add.add_argument('--title',required=True);add.add_argument('--owner',choices=ROLES,required=True)
    add.add_argument('--depends',default='');add.add_argument('--paths',default='');add.add_argument('--acceptance',required=True)
    transition=sub.add_parser('transition');transition.add_argument('--id',required=True);transition.add_argument('--status',choices=TRANSITIONS,required=True);transition.add_argument('--evidence');transition.add_argument('--reviewer',choices=('reviewer','self-review'))
    args=parser.parse_args();folder=args.project.resolve()/'.ai-team';ledger=folder/'tasks.json'
    for p in [folder,ledger]:
        if p.is_symlink() or p.exists() and getattr(p.lstat(),'st_file_attributes',0)&1024:raise ValueError('Linked team files are unsupported')
    if args.command=='status':print(ledger.read_text(encoding='utf-8'));return
    lock=folder/'tasks.lock'
    with lock.open('x',encoding='utf-8') as out:out.write(str(os.getpid()))
    try:
        data=json.loads(ledger.read_text(encoding='utf-8'))
        if args.command=='add':change(data,'add',args.id,title=args.title,owner=args.owner,dependencies=[x for x in args.depends.split(',') if x],paths=[x for x in args.paths.split(',') if x],acceptance=args.acceptance)
        else:change(data,'transition',args.id,status=args.status,evidence=args.evidence,reviewer=args.reviewer)
        temp=folder/'tasks.next.json'
        with temp.open('x',encoding='utf-8') as out:out.write(json.dumps(data,indent=2)+'\n')
        os.replace(temp,ledger)
    finally:lock.unlink()
    print('Task ledger updated.')

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError) as exc:raise SystemExit(str(exc))
