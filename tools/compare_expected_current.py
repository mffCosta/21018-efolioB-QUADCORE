import re, subprocess, difflib, sys, os

def normalize(s):
    if s is None:
        return ''
    s=s.replace('\r\n','\n')
    s=re.sub(r'\bt\d+\b','t#',s)
    s=re.sub(r'\bL\d+\b','L#',s)
    s='\n'.join(line.rstrip() for line in s.split('\n'))
    s=re.sub(r'[ \t]+',' ',s).strip()
    return s

name='exemplo_correto'
with open(f'Testes/expected/{name}.stdout.txt','r',encoding='utf-8',errors='replace') as f:
    expected=f.read()
proc=subprocess.run([sys.executable,'main.py',f'Testes/{name}.mocp'], capture_output=True, text=True, encoding='utf-8', errors='replace', env={**os.environ, 'PYTHONIOENCODING':'utf-8'})
current=proc.stdout
ne=normalize(expected)
nc=normalize(current)
print('EQUAL=', ne==nc)
if ne!=nc:
    ed=expected.splitlines()
    cd=current.splitlines()
    for line in difflib.unified_diff(ed,cd, fromfile='expected', tofile='current', n=3):
        print(line)
else:
    print('No differences')
