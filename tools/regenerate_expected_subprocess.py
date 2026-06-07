import subprocess, glob, os
from pathlib import Path
root = Path('.')
tests_dir = root / 'Testes'
expected_dir = tests_dir / 'expected'
expected_dir.mkdir(parents=True, exist_ok=True)

for path in sorted(tests_dir.glob('*.mocp')):
    name = path.stem
    print('Generating expectation for', name)
    p = subprocess.run(
        ['python', str(root / 'main.py'), str(path)],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        env={**os.environ, 'PYTHONIOENCODING':'utf-8'}
    )
    out = p.stdout
    expected_dir.joinpath(f'{name}.stdout.txt').write_text(out, encoding='utf-8')
    expected_dir.joinpath(f'{name}.exitcode.txt').write_text(str(p.returncode), encoding='utf-8')
print('Done')
