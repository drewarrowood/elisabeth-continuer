"""Build site/index.html from paper.md, keeping the hand-made styling and pair boxes."""
import re, html, markdown, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
md = (root / 'paper.md').read_text()
old = (root / 'site' / 'index.html').read_text()
head = old[:old.index('<main>') + len('<main>')]

title_line, rest = md.split('\n', 1)
pre, body = rest.split('\n---\n', 1)

def pair(fr, ref, en, label):
    return (f'<div class="pair"><div class="fr">{html.escape(fr, quote=False)}<small>{ref}</small></div>'
            f'<div class="en">{en}<small>{label}</small></div></div>')

GLOSS = "English: our literal gloss"
EN = {
 "AT III 661": ("Given that the soul of a human being is only a thinking substance, how can it affect the bodily spirits, in order to bring about voluntary actions?", "English: Bennett's translation"),
 "AT III 685": ("it would be easier for me to grant matter and extension to the soul than to grant an immaterial being the capacity to move a body and be moved by it", GLOSS),
 "AT IV 269": ("there are illnesses that take away the power of reasoning altogether", GLOSS),
}

conv = lambda s: markdown.markdown(s, extensions=['tables', 'fenced_code'])
meta = conv(pre).replace('<p>', '<p class="meta">')
h = conv(body)

# block quotes in French -> pair boxes
def bq(m):
    inner = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
    q = re.match(r'"(.+)" \((AT [IV]+ \d+)\)$', inner)
    en, label = EN[q.group(2)]
    return pair(q.group(1), q.group(2), en, label)
h = re.sub(r'<blockquote>\s*(.*?)\s*</blockquote>', bq, h, flags=re.S)
# §8: the gloss line now lives in the pair box
h = h.replace('<p>— there are illnesses that take away the power of reasoning altogether. ', '<p>')
# §2: keep the vapours pair box after the paragraph that quotes it
v = 'peut perdre tout cela par quelques vapeurs'
i = h.index(v); j = h.index('</p>', i) + 4
h = h[:j] + '\n' + pair(v, 'AT III 685', 'can lose all of that through a few vapours', GLOSS) + h[j:]
# A.2 9.3: keep the n'y repugnant point pair box
r = "n'y repugnant point"
i = h.index(html.escape(r, quote=False)) if html.escape(r, quote=False) in h else h.index(r)
j = h.index('</p>', i) + 4
h = h[:j] + '\n' + pair(r, 'AT IV 2, 1 July 1643', 'not being at all contrary to it', GLOSS) + h[j:]
# equations
h = re.sub(r'<p>\(NI\) <code>(.*?)</code>\.</p>', r'<div class="eq">(NI)&nbsp;&nbsp; \1</div>', h)
h = re.sub(r'<p><code>((?:C|CC)\(e, y\)\s+:=.*?)</code></p>', lambda m: '<div class="eq">' + m.group(1).replace('  ', '&nbsp; ') + '</div>', h)
# Latin titles table
lat = ('<table><tr><th>Latin</th><th>English</th></tr><tr><td><em>Principia philosophiae</em> (1644)</td><td><em>Principles of Philosophy</em>, which Descartes dedicated to her</td></tr>'
       '<tr><td><em>De vita beata</em></td><td><em>On the Happy Life</em>, Seneca\'s treatise, discussed in their 1645 letters</td></tr></table>')
h = re.sub(r'(<h2>A note on Latin</h2>\s*)<p>', r'\1' + lat + '\n<p class="note">', h)
# italic author/notes lines -> note
h = re.sub(r'<p><em>((?:Written|Drafted|Moved|The subsection|We do not settle|Reading 2 is|From the seated|Carried over|Reserved|Resolved)[^<]*(?:<[^>]+>[^<]*)*?)</em></p>', r'<p class="note"><em>\1</em></p>', h)
# ids + nav
nav = []
def hid(m):
    t = re.sub(r'<[^>]+>', '', m.group(1))
    n = re.match(r'(\d+)\.', t)
    k = 's' + n.group(1) if n else ('appA' if t.startswith('Appendix') else 'lat' if 'Latin' in t else 'refs' if t == 'References' else re.sub(r'\W+', '-', t.lower()))
    nav.append((k, re.sub(r'^\d+\.\s*', '', t)))
    return f'<h2 id="{k}">{m.group(1)}</h2>'
h = re.sub(r'<h2>(.*?)</h2>', hid, h)
navh = '<nav><ol>' + ''.join(f'<li><a href="#{k}">{html.escape(t, quote=False)}</a></li>' for k, t in nav) + '</ol></nav>'
top = ('<h1>Plus facile de conceder la matiere</h1>\n'
       + pair('Plus facile de conceder la matiere', 'Title, from AT III 685', 'Easier to grant [the soul] matter', GLOSS)
       + '\n<p class="sub">Identity, continuation, and a prompt-made Elisabeth</p>\n')
out = head + '\n' + top + meta + '\n' + navh + '\n\n' + h + '\n</main></body></html>\n'
(root / 'site' / 'index.html').write_text(out)
print('ok', len(out))
