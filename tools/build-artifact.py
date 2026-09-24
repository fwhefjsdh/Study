#!/usr/bin/env python3
"""Build the single-file page published to the Answer Grid artifact on claude.ai.
Inlines css/app.css and js/*.js. The bundled seed is left out: inside the artifact, data comes from its own database."""
import pathlib,re
root=pathlib.Path(__file__).resolve().parent.parent
html=(root/"index.html").read_text()
body=re.search(r"<body>(.*)</body>",html,re.S).group(1)
body=re.sub(r'\s*<script src="[^"]+"></script>',"",body)
fonts=re.search(r'<link rel="stylesheet" href="https://fonts[^>]+>',html).group(0)
css=(root/"css/app.css").read_text()
js="\n".join((root/f"js/{n}.js").read_text() for n in ("logic","store","app"))
js=js.replace("</script","<\\/script")
out=f'<title>Answer Grid</title>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n{fonts}\n<style>\n{css}</style>\n{body.strip()}\n<script>\n{js}\n</script>\n'
dst=root/"dist/answer-grid-artifact.html";dst.parent.mkdir(exist_ok=True);dst.write_text(out)
print(dst,len(out),"bytes")
