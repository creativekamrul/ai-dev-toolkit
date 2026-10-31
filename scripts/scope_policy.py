"""Keep instruction packages focused on knowledge beyond the host's basic tools."""
import json
from pathlib import Path


def exclusion_reason(root,skill_id,original_name):
    policy=json.loads((Path(root)/'manifests/exclusions.json').read_text(encoding='utf-8'))
    return policy.get('skills',{}).get(skill_id) or policy.get('originalNames',{}).get(original_name)
