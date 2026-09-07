import os
import glob

def check_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()
    assert '<!DOCTYPE html>' in c, f"missing doctype in {file_path}"
    assert 'rel="icon"' in c, f"missing favicon in {file_path}"
    norm = file_path.replace('\\', '/')
    if norm not in ['index.html', 'tools/index.html']:
        assert 'export-fab-btn' in c, f"missing export button in {file_path}"
        assert 'ql-toolbox:' in c, f"missing localstorage key in {file_path}"
        assert 'tool-select' in c, f"missing tool switcher in {file_path}"
    return True

pages = ['index.html', 'tools/index.html'] + glob.glob('tools/*/index.html')
for p in pages:
    check_html(p)
    print(f"Verified OK: {p}")
print(f"All {len(pages)} HTML pages passed verification!")
