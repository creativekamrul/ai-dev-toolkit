"""Portable project search, environment checks and resumable checkpoints. Stdlib only."""
import argparse,json,os,shutil,sys
from datetime import datetime,timezone
from pathlib import Path


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))


def search(index,query='',limit=8,status=None):
    if not 1<=limit<=50:raise ValueError('Limit must be between 1 and 50')
    terms=query.casefold().split();ranked=[]
    for row in index['skills']:
        if status and row['status']!=status:continue
        hay=(row['id']+' '+row['description']+' '+' '.join(row.get('tags',[]))).casefold()
        if not all(t in hay for t in terms):continue
        score=sum(4 if t in row['id'] else 1 for t in terms)+(2 if row['status']=='reviewed' else 0)
        ranked.append((score,row))
    return [r for _,r in sorted(ranked,key=lambda x:(-x[0],x[1]['id']))[:limit]]


def doctor(project):
    config=read(project/'.ai-toolkit/project.json');preset=config['preset']
    required=['python']
    if preset in ('php','laravel','wordpress','wordpress-plugin','wordpress-theme','wordpress-headless'):required+=['php']
    if preset in ('nextjs','react-vite','mern','node-express','nestjs','saas','wordpress-headless'):required+=['node','npm']
    elif preset.startswith('wordpress'):required+=['node']
    if preset=='laravel':required+=['composer']
    tools={name:bool(shutil.which(name)) for name in required}
    return {'preset':preset,'tools':tools,'ready':all(tools.values()),
            'notes':['Checks executable availability only; no downloads, services or credentials are configured.',
                     'WordPress projects need a separate WordPress runtime for integration tests.']}


def checkpoint(project,summary,next_task,decision=None,blocker=None,evidence=None):
    folder=project/'.ai-team';target=folder/'state.json'
    for p in [project,folder,target]:
        if p.is_symlink() or (p.exists() and getattr(p.lstat(),'st_file_attributes',0)&1024):raise ValueError('Linked project state is unsupported')
    if not summary.strip() or not next_task.strip():raise ValueError('Summary and next task are required')
    if any(len(v)>4000 for v in (summary,next_task,decision or '',blocker or '',evidence or '')):raise ValueError('Keep checkpoint fields under 4000 characters')
    lock=folder/'state.lock'
    with lock.open('x') as f:f.write(str(os.getpid()))
    temp=folder/'state.next.json'
    try:
        state=read(target)
        state.update(summary=summary,nextTask=next_task,updatedAt=datetime.now(timezone.utc).isoformat())
        for key,value in [('decisions',decision),('blockers',blocker),('evidence',evidence)]:
            if value is not None:state[key]=(state.get(key,[])+[value])[-12:] if value else []
        with temp.open('x',encoding='utf-8') as f:f.write(json.dumps(state,indent=2)+'\n')
        os.replace(temp,target)
    finally:lock.unlink()
    return state


def resume(project):
    state=read(project/'.ai-team/state.json');tasks=read(project/'.ai-team/tasks.json')['tasks']
    return {'state':state,'activeTasks':[t for t in tasks if t['status']!='done'],
            'readNext':['AGENTS.md','docs/PROJECT-BRIEF.md','docs/DESIGN-CONTRACT.md'],
            'instruction':'Verify the current code and evidence before continuing the next task; checkpoint notes are not proof that checks passed.'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',type=Path)
    sub=p.add_subparsers(dest='command',required=True)
    q=sub.add_parser('search');q.add_argument('query',nargs='?',default='');q.add_argument('--limit',type=int,default=8);q.add_argument('--status',choices=['reviewed','screened'])
    sub.add_parser('resume');sub.add_parser('doctor')
    c=sub.add_parser('checkpoint');c.add_argument('--summary',required=True);c.add_argument('--next',required=True);c.add_argument('--decision');c.add_argument('--blocker');c.add_argument('--evidence')
    a=p.parse_args(argv);project=(a.project or Path(__file__).resolve().parents[1]).absolute()
    if a.command=='search':
        result=search(read(project/'.ai-toolkit/search-index.json'),a.query,a.limit,a.status)
        if not result:print('No matches. Try fewer terms or a stack name, for example: search php. Use the central toolkit to review and add a skill.',file=sys.stderr)
    elif a.command=='resume':result=resume(project)
    elif a.command=='doctor':result=doctor(project)
    else:result=checkpoint(project,a.summary,a.next,a.decision,a.blocker,a.evidence)
    print(json.dumps(result,indent=2))
    return 1 if a.command=='doctor' and not result['ready'] else 0


if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,OSError,KeyError) as e:sys.exit(str(e))
