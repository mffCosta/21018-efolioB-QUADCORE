import os, glob
from pathlib import Path

expected_dir = Path('Testes') / 'expected'
if not expected_dir.exists():
    print('No expected dir')
    raise SystemExit(1)

for path in sorted(expected_dir.glob('*.*')):
    b = path.read_bytes()
    text = None
    # BOM checks
    if b.startswith(b'\xff\xfe'):
        text = b.decode('utf-16le', errors='replace')
    elif b.startswith(b'\xfe\xff'):
        text = b.decode('utf-16be', errors='replace')
    elif b.startswith(b'\xef\xbb\xbf'):
        text = b.decode('utf-8-sig', errors='replace')
    else:
        # try utf-8 else cp1252
        try:
            text = b.decode('utf-8')
        except Exception:
            try:
                text = b.decode('cp1252')
            except Exception:
                text = b.decode('latin-1', errors='replace')
    path.write_text(text, encoding='utf-8')
    print('Rewrote', path)
print('Done')
