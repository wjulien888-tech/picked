#!/usr/bin/env python3
"""Bundle the application and its vendored libraries into exports/Picked.html."""
from pathlib import Path
import base64
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
html = (DIST / 'index.html').read_text()
for name in ['vendor/katex.min.css', 'style.css']:
    css = (DIST / name).read_text()
    if name.startswith('vendor/'):
        def inline_font(match):
            font = DIST / 'vendor' / match[1]
            return ('url(data:font/' + font.suffix[1:] + ';base64,'
                    + base64.b64encode(font.read_bytes()).decode() + ')')
        css = re.sub(r'url\((fonts/[^)]+)\)', inline_font, css)
    html = html.replace('<link rel="stylesheet" href="' + name + '">', '<style>' + css + '</style>')
worker = (DIST / 'vendor/pdf.worker.min.js').read_text()
for name in re.findall(r'<script src="([^"]+)"></script>', html):
    code = (DIST / name).read_text()
    if name == 'app.js':
        code = ('window.PICKED_WORKER_URL=URL.createObjectURL(new Blob(['
                + json.dumps(worker) + '],{type:"application/javascript"}));\n' + code)
    code = re.sub('</script', r'<\\/script', code, flags=re.I)
    html = html.replace('<script src="' + name + '"></script>', '<script>' + code + '</script>')
output = ROOT / 'exports/Picked.html'
output.parent.mkdir(exist_ok=True)
output.write_text(html)
print('Built:', output)
