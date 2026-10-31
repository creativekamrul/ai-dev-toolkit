"""Development-only parsers. The initializer itself has no third-party dependencies."""
from pathlib import Path
import sys
local=Path(__file__).resolve().parents[1]/'.local/python-deps'
if local.is_dir(): sys.path.insert(0,str(local))
try:
    import yaml
except ImportError as exc:
    raise SystemExit('Install development requirements: python -m pip install -r requirements-dev.txt') from exc

class UniqueLoader(yaml.SafeLoader): pass
def unique_mapping(loader,node,deep=False):
    result={}
    for key_node,value_node in node.value:
        key=loader.construct_object(key_node,deep=deep)
        if key in result: raise ValueError('Duplicate YAML key: '+str(key))
        result[key]=loader.construct_object(value_node,deep=deep)
    return result
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique_mapping)
def metadata(text):
    import re
    match=re.match(r'\A\ufeff?---\s*\n(.*?)\n---(?:\s*\n|$)',text,re.S)
    if not match: raise ValueError('Missing YAML frontmatter')
    result=yaml.load(match[1],Loader=UniqueLoader)
    if not isinstance(result,dict) or not all(isinstance(result.get(k),str) and result[k].strip() for k in ('name','description')):
        raise ValueError('name and description must be nonempty strings')
    return result
