import os, glob, subprocess, re, difflib, sys

def normalize(s):
    if s is None:
        return ''
    import unicodedata
    s = s.replace('\r\n','\n')
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r'\bt\d+\b','t#',s)
    s = re.sub(r'\bL\d+\b','L#',s)
    s = '\n'.join(line.rstrip() for line in s.split('\n'))
    s = re.sub(r'[ \t]+',' ',s).strip()
    return s

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
tests_dir = os.path.join(root, 'Testes')
expected_dir = os.path.join(tests_dir, 'expected')
files = sorted(glob.glob(os.path.join(tests_dir, '*.mocp')))
failures = 0
out_lines = []
for path in files:
    name = os.path.splitext(os.path.basename(path))[0]
    exp_path = os.path.join(expected_dir, name + '.stdout.txt')
    out_lines.append('\n=== ' + name + ' ===')
    if not os.path.exists(exp_path):
        out_lines.append('MISSING expected: ' + exp_path)
        failures += 1
        continue
    with open(exp_path, 'r', encoding='utf-8', errors='replace') as f:
        expected = f.read()
    proc = subprocess.run([sys.executable, os.path.join(root,'main.py'), path], capture_output=True, text=True, encoding='utf-8', errors='replace', env={**os.environ, 'PYTHONIOENCODING':'utf-8'})
    current = proc.stdout
    ne = normalize(expected)
    nc = normalize(current)
    if ne == nc:
        out_lines.append('OK')
    else:
        out_lines.append('DIFFER')
        failures += 1
        ed = expected.splitlines()
        cd = current.splitlines()
        for line in difflib.unified_diff(ed, cd, fromfile='expected', tofile='current', n=3):
            out_lines.append(line)
out_lines.append('\nTotal failures: ' + str(failures))
if failures:
    out_lines.append('SOME FAILURES')
else:
    out_lines.append('All matched')

with open(os.path.join(root,'tools','compare_all.out.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

if failures:
    raise SystemExit(2)
