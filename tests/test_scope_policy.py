"""Imports must add specialist guidance, not reintroduce basic harness wrappers."""
import contextlib,hashlib,importlib.util,io,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from scope_policy import exclusion_reason


def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/file)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result


class ScopeTests(unittest.TestCase):
    def setUp(self):
        base=ROOT/'.local/test-runs';base.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=base);self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.toolkit=self.root/'toolkit';(self.toolkit/'manifests').mkdir(parents=True);(self.toolkit/'.local').mkdir()
        shutil.copyfile(ROOT/'manifests/exclusions.json',self.toolkit/'manifests/exclusions.json')
        (self.toolkit/'manifests/catalog.json').write_text('{"skills":[]}')
    def source(self,base,name):
        folder=base/name;folder.mkdir(parents=True)
        (folder/'SKILL.md').write_text('---\nname: '+name+'\ndescription: Test skill for '+name+'\n---\n\nInstructions.\n',encoding='utf-8')
        shutil.copyfile(ROOT/'LICENSE',folder/'LICENSE');return folder/'SKILL.md'
    def test_specialist_edit_search_and_framework_skills_are_preserved(self):
        for name in ('image-editing','mongodb-search-and-ai','wordpress-wp-plugin-development','eve','design-foundations'):
            self.assertIsNone(exclusion_reason(ROOT,'some-source-'+name,name))
        for name in ('edit-file','apply-patch','agent-browser','agent-browser-verify'):
            self.assertTrue(exclusion_reason(ROOT,'new-source-'+name,name))
    def test_local_import_excludes_basic_operation_before_copy(self):
        base=self.root/'.config/goose/skills';files=[self.source(base,name) for name in ('edit-file','image-editing')]
        inventory={'skills':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'name':p.parent.name,'category':'utilities'} for p in files]}
        inv=self.root/'inventory.json';inv.write_text(json.dumps(inventory));imp=module('local_scope_test','import-local.py')
        with patch.object(imp,'ROOT',self.toolkit),contextlib.redirect_stdout(io.StringIO()):imp.run(inv,False)
        decisions=json.loads((self.toolkit/'.local/local-import-decisions.json').read_text())
        # Preview preserves useful packages and never creates library files.
        self.assertTrue(any(row['name']=='image-editing' and row['status']=='eligible' for row in decisions))
        self.assertFalse(any(row['name']=='edit-file' and row['status']=='eligible' for row in decisions))
        self.assertFalse((self.toolkit/'library').exists())
    def test_community_import_blocks_new_namespaced_copy(self):
        checkout=self.root/'upstream';checkout.mkdir()
        self.source(checkout,'agent-browser');self.source(checkout,'image-editing')
        subprocess.run(['git','init',str(checkout)],check=True,capture_output=True)
        subprocess.run(['git','-C',str(checkout),'add','.'],check=True,capture_output=True)
        subprocess.run(['git','-C',str(checkout),'-c','user.name=Toolkit Test','-c','user.email=test@example.invalid','commit','-m','Test input'],check=True,capture_output=True)
        imp=module('collection_scope_test','import-collection.py')
        with patch.object(imp,'ROOT',self.toolkit):rows=imp.import_source(checkout,'new-source','example/skills',True)
        statuses={r['name']:r['status'] for r in rows}
        self.assertEqual(statuses['agent-browser'],'reference-only');self.assertEqual(statuses['image-editing'],'bundled-screened')
        self.assertFalse((self.toolkit/'library/community/new-source/new-source-agent-browser').exists())
        self.assertTrue((self.toolkit/'library/community/new-source/new-source-image-editing/SKILL.md').is_file())


if __name__=='__main__':unittest.main()
