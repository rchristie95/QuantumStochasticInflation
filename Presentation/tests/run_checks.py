"""Run the retained presentation checks against either or both editions."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
TESTS=Path(__file__).resolve().parent
EDITION_CHECKS=('verify_physics.py','test_image_cache.py','test_foreground.py')


def run_check(filename,edition):
    # Separate interpreters prevent Long/Short modules leaking through sys.modules.
    worker=('import runpy,sys; sys.path.insert(0,sys.argv[1]); '
            'path=sys.argv[2]; sys.argv=[path]; runpy.run_path(path,run_name="__main__")')
    print(f'[{edition.name}] {filename}',flush=True)
    subprocess.run([sys.executable,'-c',worker,str(edition),str(TESTS/filename)],
                   cwd=edition,check=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--edition',choices=('all','long','short'),default='all')
    args=parser.parse_args()
    selected=('Long','Short') if args.edition=='all' else (args.edition.title(),)
    for name in selected:
        for filename in EDITION_CHECKS:run_check(filename,ROOT/name)
    # This operator-algebra check has no edition-specific imports.
    run_check('verify_unravellings.py',ROOT/selected[0])
    print('PASS: all retained presentation checks.',flush=True)


if __name__=='__main__':main()
