"""Probe installed Codex's local skill loader, without a model call or global config edits.

Uses the app-server initialize and skills/list protocol from codex-cli 0.148.0.
Pass --codex-executable with the native executable path and --project with a demo directory.
An isolated CODEX_HOME is used only for the child process.
"""
import argparse
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
import time

ROOT=Path(__file__).resolve().parents[1]

def main(executable,project):
    local=ROOT/'.local/codex-discovery'; local.mkdir(parents=True,exist_ok=True)
    isolated=local/'home'; isolated.mkdir(exist_ok=True)
    environment=dict(os.environ); environment['CODEX_HOME']=str(isolated)
    messages=queue.Queue()
    with (local/'stderr.log').open('w',encoding='utf-8') as err:
        process=subprocess.Popen([str(executable),'app-server','--stdio','-c','analytics.enabled=false'],
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',env=environment,cwd=project)
        def reader():
            for line in process.stdout:
                try: messages.put(json.loads(line))
                except ValueError: continue
        threading.Thread(target=reader,daemon=True).start()
        def send(value):
            process.stdin.write(json.dumps(value)+'\n'); process.stdin.flush()
        def receive(identifier):
            deadline=time.monotonic()+40
            while time.monotonic()<deadline:
                try: msg=messages.get(timeout=max(.1,deadline-time.monotonic()))
                except queue.Empty: break
                if msg.get('id')==identifier:
                    if 'error' in msg: raise RuntimeError(json.dumps(msg['error']))
                    return msg['result']
            raise RuntimeError('Codex app-server response timeout; see local stderr log.')
        try:
            send({'id':1,'method':'initialize','params':{'clientInfo':{'name':'toolkit-discovery-check','version':'0.1.0'},'capabilities':{'experimentalApi':True}}})
            receive(1)
            send({'method':'initialized','params':{}})
            send({'id':2,'method':'skills/list','params':{'cwds':[str(project)],'forceReload':True}})
            result=receive(2)
            expected=set(json.loads((project/'.ai-toolkit/installed.json').read_text())['skills'])
            found=[]; errors=[]
            for entry in result['data']:
                errors.extend(entry.get('errors',[]))
                for skill in entry['skills']:
                    p=Path(skill['path']).resolve()
                    if p.is_relative_to(project.resolve()) and skill['name'] in expected:
                        found.append({k:skill[k] for k in ('name','path','scope','enabled')})
            evidence={'project':str(project),'skills':found,'loaderErrors':errors,
                      'passed':{s['name'] for s in found if s['enabled']}==expected and not errors,
                      'scope':'Codex loader discovery only; no model invocation, Goose test or live Penpot edit.'}
            (local/'result.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(evidence,indent=2))
            if not evidence['passed']: raise SystemExit(1)
        finally:
            process.terminate()
            try: process.wait(timeout=5)
            except subprocess.TimeoutExpired: process.kill(); process.wait()

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--codex-executable',type=Path,required=True); parser.add_argument('--project',type=Path,required=True)
    args=parser.parse_args(); main(args.codex_executable,args.project.resolve())
