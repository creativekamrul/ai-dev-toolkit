"""Create a disposable, loopback-only WordPress test site. Downloads pinned official archives."""
import argparse,hashlib,io,json,secrets,shutil,subprocess,sys,urllib.request,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent


def setup(directory,php):
    directory=directory.absolute()
    if any(p.is_symlink() or p.exists() and getattr(p.lstat(),'st_file_attributes',0)&1024 for p in [directory,*directory.parents]):raise ValueError('Linked test directories are unsupported')
    if directory.exists() and any(directory.iterdir()):raise ValueError('Choose a new or empty test directory; existing sites are never changed')
    directory.mkdir(parents=True,exist_ok=True)
    sources=json.loads((ROOT/'wordpress-sources.json').read_text(encoding='utf-8'))
    for source in sources['archives']:
        if not source['url'].startswith('https://downloads.wordpress.org/'):raise ValueError('Unexpected source host')
        with urllib.request.urlopen(source['url'],timeout=90) as response:data=response.read(100_000_001)
        if len(data)>100_000_000 or hashlib.sha256(data).hexdigest()!=source['sha256']:raise ValueError('Archive size/hash mismatch')
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for member in archive.infolist():
                target=(directory/member.filename).resolve()
                if not target.is_relative_to(directory.resolve()) or '\\' in member.filename or ':' in member.filename or (member.external_attr>>16)&0o170000==0o120000:raise ValueError('Unsafe archive entry')
            archive.extractall(directory)
    site=directory/'wordpress';plugin=site/'wp-content/plugins/sqlite-database-integration'
    shutil.copytree(directory/'sqlite-database-integration',plugin)
    (site/'wp-content/db.php').write_bytes((plugin/'db.copy').read_bytes())
    sample=site/'wp-content/plugins/toolkit-events';sample.mkdir()
    shutil.copyfile(ROOT/'fixtures/wordpress-plugin/toolkit-events.php',sample/'toolkit-events.php')
    (site/'wp-config.php').write_text("""<?php
define('DB_NAME','toolkit');define('DB_USER','toolkit');define('DB_PASSWORD','');define('DB_HOST','localhost');
define('DB_CHARSET','utf8');define('DB_COLLATE','');define('DB_ENGINE','sqlite');
define('WP_HOME','http://127.0.0.1:8767');define('WP_SITEURL','http://127.0.0.1:8767');
define('DISABLE_WP_CRON',true);define('WP_HTTP_BLOCK_EXTERNAL',true);define('WP_AUTO_UPDATE_CORE',false);
define('WP_DEBUG',false);if(!defined('ABSPATH')){define('ABSPATH',__DIR__.'/');}$table_prefix='wp_';
require_once ABSPATH.'wp-settings.php';
""",encoding='utf-8')
    mu=site/'wp-content/mu-plugins';mu.mkdir(exist_ok=True)
    (mu/'no-external-mail.php').write_text("<?php add_filter('pre_wp_mail',function(){return true;});",encoding='utf-8')
    theme=site/'wp-content/themes/toolkit-evaluation';theme.mkdir()
    (theme/'style.css').write_text('/* Theme Name: Toolkit Evaluation */',encoding='utf-8')
    (theme/'index.php').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Community sessions</title><?php wp_head(); ?></head><body style="margin:0;background:#fffaf2"><main style="max-width:1100px;margin:40px auto;padding:20px"><?php while(have_posts()){the_post();the_content();} ?></main><?php wp_footer(); ?></body></html>''',encoding='utf-8')
    script="""<?php
define('WP_INSTALLING',true);require __DIR__.'/wordpress/wp-load.php';require_once ABSPATH.'wp-admin/includes/upgrade.php';
wp_install('Toolkit Evaluation','evaluation_admin','nobody@example.invalid',false,'','PASSWORD');
require_once ABSPATH.'wp-admin/includes/plugin.php';$result=activate_plugin('toolkit-events/toolkit-events.php');
if(is_wp_error($result)){fwrite(STDERR,$result->get_error_message());exit(1);}
switch_theme('toolkit-evaluation');
$id=wp_insert_post(['post_type'=>'page','post_status'=>'publish','post_title'=>'Community sessions','post_content'=>'[toolkit_sessions]']);
update_option('show_on_front','page');update_option('page_on_front',$id);
$escaped=do_shortcode('[toolkit_sessions heading="<script>alert(1)</script>"]');
if(strpos($escaped,'<script>')!==false || strpos($escaped,'&lt;script&gt;')===false){fwrite(STDERR,'Escaping failed');exit(2);}
if(substr_count(do_shortcode('[toolkit_sessions]'),'<li>')!==3){exit(3);}
echo json_encode(['activated'=>is_plugin_active('toolkit-events/toolkit-events.php'),'escapingPassed'=>true,'sessionCount'=>3,'wordpressVersion'=>get_bloginfo('version')]);
""".replace('PASSWORD',secrets.token_hex(24))
    (directory/'install-test.php').write_text(script,encoding='utf-8')
    loaded=subprocess.check_output([php,'-r',"echo extension_loaded('pdo_sqlite') ? 'yes' : 'no';"],text=True).strip()
    flags=[] if loaded=='yes' else ['-d','extension=pdo_sqlite']
    result=subprocess.run([php,*flags,str(directory/'install-test.php')],capture_output=True,text=True,timeout=90)
    if result.returncode:raise RuntimeError(result.stderr+result.stdout)
    evidence=json.loads(result.stdout);evidence['phpSqliteFlagRequired']=bool(flags)
    (directory/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(evidence,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True);p.add_argument('--php',default='php');a=p.parse_args()
    try:setup(a.directory,a.php)
    except (ValueError,OSError,RuntimeError) as e:sys.exit(str(e))
