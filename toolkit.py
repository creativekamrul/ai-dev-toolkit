"""Run the toolkit without installing a package: python toolkit.py --help."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'scripts'))
from cli import main
if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,OSError,KeyError) as e:sys.exit('ERROR: '+str(e))
