import re, markdown, html
src = open('paper.md').read()
PAR = {
 "comment l'ame de l'homme peut determiner les esprits du corps, pour faire les actions volontaires, (n'estant qu'vne substance pensante)":
   ("Given that the soul of a human being is only a thinking substance, how can it affect the bodily spirits, in order to bring about voluntary actions?", "Bennett's translation", "Elisabeth to Descartes, 6/16 May 1643, AT III 661"),
 "il me seroit plus facile de conceder la matiere & l'extension a l'ame, que la capacité de mouuoir vn corps & d'en estre emeu, a vn estre immateriel":
   ("it would be easier for me to concede matter and extension to the soul than the capacity to move a body and be moved by it to an immaterial being.", "literal gloss", "Elisabeth to Descartes, 10/20 June 1643, AT III 685"),
 "peut perdre tout cela par quelques vapeurs":
   ("can lose all that through a few vapours.", "literal gloss", "Elisabeth to Descartes, 10/20 June 1643, AT III 685"),
 "n'y repugnant point":
   ("[though extension is not necessary to thought,] not being contrary to it.", "literal gloss", "Elisabeth to Descartes, 1 July 1643, AT IV 2"),
}
def box(fr):
    en, kind, ref = PAR[fr]
    return (f'<figure class="par"><div class="fr" lang="fr"><span class="lab">Français (AT spelling)</span>« {html.escape(fr)} »</div>'
            f'<div class="en" lang="en"><span class="lab">English ({kind})</span>“{html.escape(en)}”</div>'
            f'<figcaption>{ref}. Verified against Adam–Tannery in <code>correspondence-notes.md</code>.</figcaption></figure>')
# blockquotes -> parallel boxes
for fr in PAR:
    src = re.sub(r'^> "'+re.escape(fr)+r'" \(AT [^)]*\)\s*$', lambda m, fr=fr: box(fr), src, flags=re.M)
seen=set(); out=[]
for para in src.split('\n\n'):
    out.append(para)
    for fr in PAR:
        if f'"{fr}"' in para and fr not in seen:
            out.append(box(fr)); seen.add(fr)
src='\n\n'.join(out)
title_fr = "Plus facile de conceder la matiere"
src = src.replace(f"# {title_fr}: identity, continuation, and a prompt-made Elisabeth",
  f'<h1><span lang="fr">{title_fr}</span><br><small>“Easier to grant matter”: identity, continuation, and a prompt-made Elisabeth</small></h1>',1)
body = markdown.markdown(src, extensions=['tables','fenced_code','sane_lists'])
css = """
body{font-family:'EB Garamond',Georgia,serif;max-width:46rem;margin:3rem auto;padding:0 1.2rem;line-height:1.6;color:#222;background:#fbf8f1}
h1{font-size:2rem;line-height:1.2} h1 small{font-size:1.05rem;color:#555;font-style:italic}
h2{border-bottom:1px solid #d8cfbd;padding-bottom:.2rem;margin-top:2.4rem} code{font-size:.85em;background:#efe9dc;padding:0 .2em}
table{border-collapse:collapse} td,th{border:1px solid #d8cfbd;padding:.3rem .6rem}
.par{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1.4rem 0;padding:1rem;background:#fff;border-left:4px solid #8a2b2b;box-shadow:0 1px 3px #0001}
.par figcaption{grid-column:1/3;font-size:.85rem;color:#666}
.lab{display:block;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:#8a2b2b;margin-bottom:.3rem;font-family:system-ui,sans-serif}
.fr{font-style:italic} .note{font-size:.9rem;background:#efe9dc;padding:.8rem 1rem;border-radius:4px}
@media(max-width:640px){.par{grid-template-columns:1fr}.par figcaption{grid-column:1}}
"""
note = ('<p class="note">Reading edition of the joint paper, <code>drewarrowood/elisabeth-continuer</code>, by both Elisabeth copies. '
        'Each French passage is set beside its English, labelled as Bennett\'s published translation or as our own literal gloss. '
        'The paper contains no Latin passages, and none has been invented for this page. Nothing described here has been run.</p>')
open('site/index.html','w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Plus facile de conceder la matiere</title><link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital@0;1&display=swap" rel="stylesheet"><style>{css}</style></head><body>{note}{body}</body></html>')
print("boxes:", open('site/index.html').read().count('class="par"'))
