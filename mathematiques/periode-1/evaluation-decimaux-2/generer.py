# Usage : python3 generer.py <dossier de sortie> <chemin de sciences/periode-1/evaluation/generer.py (styles communs)>
import sys, os, re
OUT = sys.argv[1]
CSS = re.search(r'CSS = """(.*?)"""', open(sys.argv[2]).read(), re.S).group(1)
CSS += """
.fr { display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; line-height: 1.05; margin: 0 2px; font-size: 11pt; }
.fr span:first-child { border-bottom: 1.5px solid #111; padding: 0 3px; }
.grid4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px 16px; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 22px; }
.it { display: flex; gap: 6px; align-items: center; }
.it .blank { flex: 1; min-width: 40px; }
.sq { display: inline-block; min-width: 28px; height: 24px; border: 1.5px solid #111; border-radius: 5px; vertical-align: middle; text-align: center; line-height: 22px; font-weight: 700; margin: 0 4px; }
.sq.ans { color: #c0392b; border-color: #c0392b; }
.nums { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: 4px 0 8px; }
.nums span { border: 1.5px solid #111; border-radius: 7px; padding: 2px 12px; font-weight: 700; font-size: 13pt; background: #f2f2f2; }
.order { display: flex; align-items: center; gap: 4px; flex-wrap: wrap; margin: 4px 0; }
.order .blank { min-width: 62px; text-align: center; }
.order b { font-size: 14pt; }
.focus { border: 2.5px solid #111; border-radius: 12px; padding: 10px 14px 12px; margin-top: 14px; break-inside: avoid; }
.focus .tagf { display: inline-block; background: #111; color: #fff; font-family: "Lilita One", sans-serif; padding: 2px 10px; border-radius: 6px; font-size: 11pt; letter-spacing: .04em; }
svg.dg { max-width: 175mm; }
"""
def B(a, K, c=""): return f'<span class="blank filled ans">{a}</span>' if K else f'<span class="blank {c}"></span>'
def F(n, d): return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'
def pts(K, t): return f' <span class="bareme">({t})</span>' if K else ''
def SQ(a, K): return f'<span class="sq ans">{a}</span>' if K else '<span class="sq"></span>'
def v(x): return str(x).replace(".", ",")

def droite(a, b, letters=None, places=None, K=False, ans_color="#c0392b"):
    """Demi-droite graduée en dixièmes de a à b. letters : [(lettre, valeur)] ; places : valeurs à placer (corrigé)."""
    x0, x1, y = 30, 650, 60
    n = round((b - a) * 10)
    s = [f'<svg class="dg" viewBox="0 0 690 {(150 if K else 125) if letters else 110}" role="img" aria-label="Demi-droite graduée">',
         f'<line x1="{x0-10}" y1="{y}" x2="{x1+18}" y2="{y}" stroke="#111" stroke-width="2"/>']
    X = lambda val: x0 + (val - a) / (b - a) * (x1 - x0)
    for i in range(n + 1):
        val = a + i / 10; xx = X(val); big = i % 10 == 0; mid = i % 5 == 0
        s.append(f'<line x1="{xx:.1f}" y1="{y-(14 if big else 9 if mid else 6)}" x2="{xx:.1f}" y2="{y+(14 if big else 9 if mid else 6)}" stroke="#111" stroke-width="{2 if big else 1.3}"/>')
        if big: s.append(f'<text x="{xx:.1f}" y="{y-20}" text-anchor="middle" font-size="17" font-weight="700" fill="#111">{v(round(val))}</text>')
    for l, val in (letters or []):
        xx = X(val)
        s.append(f'<line x1="{xx:.1f}" y1="{y+16}" x2="{xx:.1f}" y2="{y+34}" stroke="#111" stroke-width="2"/><polygon points="{xx:.1f},{y+15} {xx-5:.1f},{y+24} {xx+5:.1f},{y+24}" fill="#111"/>')
        s.append(f'<circle cx="{xx:.1f}" cy="{y+48}" r="12" fill="#fff" stroke="#111" stroke-width="1.8"/><text x="{xx:.1f}" y="{y+54}" text-anchor="middle" font-size="15" font-weight="700" fill="#111">{l}</text>')
        if K: s.append(f'<text x="{xx:.1f}" y="{y+82}" text-anchor="middle" font-size="15" font-weight="700" fill="{ans_color}">{v(val)}</text>')
    if K:
        for val in (places or []):
            xx = X(val)
            s.append(f'<line x1="{xx:.1f}" y1="{y+16}" x2="{xx:.1f}" y2="{y+34}" stroke="{ans_color}" stroke-width="2.5"/><polygon points="{xx:.1f},{y+14} {xx-5:.1f},{y+24} {xx+5:.1f},{y+24}" fill="{ans_color}"/>')
            s.append(f'<text x="{xx:.1f}" y="{y+52}" text-anchor="middle" font-size="15" font-weight="700" fill="{ans_color}">{v(val)}</text>')
    s.append('</svg>')
    return "".join(s)

def doc(K):
    h = [f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{"Corrigé · " if K else ""}Évaluation de mathématiques · Les nombres décimaux</title>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Lilita+One&display=swap">'
         f'<style>{CSS}</style>' + ('<style>body{font-size:10.5pt;line-height:1.38} .ex{margin-top:9px}</style>' if K else '') + '</head><body>']
    h.append('<div class="head"><div><div class="theme">Mathématiques · Nombres · Les nombres décimaux (pages 34 à 43) · Évaluation 2</div>')
    h.append(f'<h1>{"Corrigé et barème &nbsp;<span class=tag>ENSEIGNANT</span>" if K else "Évaluation de mathématiques"}</h1>')
    h.append('<div style="margin-top:6px;font-size:10.5pt">Réponses attendues en <b class="ans">rouge</b>. Le barème est indiqué à droite de chaque titre (total : 20 points).</div>' if K else '<div class="ident"><span>Prénom :</span><span>Date :</span></div>')
    h.append('</div><div class="note"><small>Note</small><b>' + ('<em>20</em>' if K else '&nbsp;&nbsp;&nbsp;') + ' / 20</b></div></div>')
    comps = [("Je passe de l’écriture fractionnaire à l’écriture décimale.", "1 · 2", "4"),
             ("Je lis, j’écris et je décompose les nombres décimaux ; je connais la valeur des chiffres.", "3 · 4 · 5", "5,5"),
             ("Je place, je repère et j’encadre des nombres décimaux sur une demi-droite graduée.", "6 · 7", "4,5"),
             ("Je compare des nombres décimaux.", "8", "2"),
             ("J’ordonne des nombres décimaux (focus : exercice 23 page 43).", "9", "4")]
    if not K:
        h.append('<table class="comp"><tr><th style="text-align:left">Compétences évaluées</th><th>Exercices</th><th class="c">Acquis</th><th class="c">En cours</th><th class="c">Non acquis</th></tr>'
                 + "".join(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td class="c"></td><td class="c"></td><td class="c"></td></tr>' for c, e, _ in comps) + '</table>')

    # 1
    h.append('<section class="ex"><h2><span class="n">1</span>De la fraction décimale au nombre décimal<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Écris chaque fraction décimale sous la forme d’un nombre décimal.' + pts(K, "0,25 point par nombre") + '</p>')
    fr = [(72, 10, "7,2"), (8, 10, "0,8"), (425, 100, "4,25"), (9, 100, "0,09"), (306, 10, "30,6"), (61, 100, "0,61"), ("1 208", 10, "120,8"), (3, 100, "0,03")]
    h.append('<div class="grid4">' + "".join(f'<div class="it">{F(n, d)} = {B(a, K, "s")}</div>' for n, d, a in fr) + '</div></section>')

    # 2
    h.append('<section class="ex"><h2><span class="n">2</span>Décompositions et nombres décimaux<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Écris chaque somme sous la forme d’un nombre décimal.' + pts(K, "0,5 point par nombre") + '</p>')
    so = [(f'5 + {F(2,10)} + {F(9,100)}', "5,29"), (f'41 + {F(3,100)}', "41,03"), (f'18 + {F(6,10)}', "18,6"), (f'{F(4,10)} + {F(1,100)}', "0,41")]
    h.append('<div class="grid2">' + "".join(f'<div class="it"><span>{"abcd"[i]})</span> {e} = {B(a, K, "s")}</div>' for i, (e, a) in enumerate(so)) + '</div>')
    if K: h.append('<p class="bareme">Erreur fréquente : 41 + 3/100 écrit « 41,3 » au lieu de 41,03.</p>')
    h.append('</section>')

    # 3
    h.append('<section class="ex"><h2><span class="n">3</span>La valeur du chiffre 5<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Indique ce que désigne le chiffre 5 dans chaque nombre : unités, dizaines, centaines, dixièmes ou centièmes.' + pts(K, "0,25 point par nombre") + '</p>')
    c7 = [("5,61", "unités"), ("52,08", "dizaines"), ("0,05", "centièmes"), ("24,5", "dixièmes"), ("513,2", "centaines"), ("3,45", "centièmes"), ("0,58", "dixièmes"), ("85,9", "unités")]
    h.append('<div class="grid4">' + "".join(f'<div class="it"><b>{n}</b> → {B(a, K)}</div>' for n, a in c7) + '</div></section>')

    # 4
    h.append('<section class="ex"><h2><span class="n">4</span>Lire et écrire les nombres décimaux<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Écris ces nombres en chiffres.' + pts(K, "0,25 point par nombre") + '</p>')
    ec = [("8 unités et 15 centièmes", "8,15"), ("20 unités et 4 dixièmes", "20,4"), ("Sept dixièmes", "0,7"), ("43 dixièmes", "4,3"),
          ("608 centièmes", "6,08"), ("9 centièmes", "0,09"), (f'14 + {F(5,10)} + {F(2,100)}', "14,52"), ("7 + 0,36", "7,36")]
    h.append('<div class="grid2">' + "".join(f'<div class="it"><span>{"abcdefgh"[i]}) {t} =</span>{B(a, K, "s")}</div>' for i, (t, a) in enumerate(ec)) + '</div></section>')

    # 5
    h.append('<section class="ex"><h2><span class="n">5</span>Égal ou différent ?<span class="pts">… / 1,5</span></h2>')
    h.append('<p class="consigne">Complète avec le signe = ou ≠.' + pts(K, "0,25 point par case") + '</p>')
    eg = [("6,30", "6,3", "="), ("9,4", "9,04", "≠"), ("2,7", "2,70", "="), ("11,03", "11,30", "≠"), ("25", "25,0", "="), ("0,8", "0,08", "≠")]
    h.append('<div class="grid4" style="grid-template-columns:repeat(3,1fr)">' + "".join(f'<div>{"abcdef"[i]}) {x} {SQ(s_, K)} {y}</div>' for i, (x, y, s_) in enumerate(eg)) + '</div>')
    if K: h.append('<p class="bareme">Les 0 à la fin de la partie décimale peuvent être supprimés sans changer la valeur du nombre.</p>')
    h.append('</section>')

    # 6
    h.append('<section class="ex"><h2><span class="n">6</span>La demi-droite graduée<span class="pts">… / 2,5</span></h2>')
    h.append('<p class="consigne">a) Écris le nombre décimal désigné par chaque lettre.' + pts(K, "0,25 point par lettre") + '</p>')
    lt = [("A", 2.2), ("B", 2.7), ("C", 3.1), ("D", 3.4), ("E", 3.6), ("F", 3.9)]
    h.append(droite(2, 4, letters=lt, K=K))
    if not K:
        h.append('<div class="grid4" style="grid-template-columns:repeat(6,1fr)">' + "".join(f'<div class="it"><b>{l}</b> = <span class="blank s"></span></div>' for l, _ in lt) + '</div>')
    h.append('<p class="consigne" style="margin-top:8px">b) Place ces nombres sur la demi-droite avec une flèche : <b>0,3</b> · <b>0,8</b> · <b>1,4</b> · <b>1,9</b>' + pts(K, "0,25 point par nombre bien placé") + '</p>')
    h.append(droite(0, 2, places=[0.3, 0.8, 1.4, 1.9], K=K))
    h.append('</section>')

    # 7
    h.append('<section class="ex"><h2><span class="n">7</span>Encadrer<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">a) Encadre chaque nombre entre deux nombres entiers qui se suivent.' + pts(K, "0,25 point par encadrement") + '</p>')
    e1 = [("4,5", "4", "5"), ("12,13", "12", "13"), ("0,1", "0", "1"), ("9,10", "9", "10")]
    h.append('<div class="grid4">' + "".join(f'<div class="it">{B(lo, K, "s")} &lt; <b>{n}</b> &lt; {B(hi, K, "s")}</div>' for n, lo, hi in e1) + '</div>')
    h.append('<p class="consigne" style="margin-top:8px">b) Encadre chaque nombre au dixième près.' + pts(K, "0,25 point par encadrement") + '</p>')
    e2 = [("5,34", "5,3", "5,4"), ("2,87", "2,8", "2,9"), ("0,45", "0,4", "0,5"), ("6,92", "6,9", "7")]
    h.append('<div class="grid4">' + "".join(f'<div class="it">{B(lo, K, "s")} &lt; <b>{n}</b> &lt; {B(hi, K, "s")}</div>' for n, lo, hi in e2) + '</div>')
    if K: h.append('<p class="bareme">Pour 9,10, l’encadrement attendu est 9 &lt; 9,10 &lt; 10. Pour 6,92, accepter « 7 » ou « 7,0 ».</p>')
    h.append('</section>')

    # 8
    h.append('<section class="ex"><h2><span class="n">8</span>Comparer<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Complète avec &lt;, &gt; ou =.' + pts(K, "0,25 point par case") + '</p>')
    cp = [("4,52", "45,2", "<"), ("7,3", "7,30", "="), ("2,9", "2,19", ">"), ("6,08", "6,8", "<"),
          ("10,1", "10,01", ">"), ("3,45", "3,5", "<"), ("0,7", "0,69", ">"), ("8,25", "8,52", "<")]
    h.append('<div class="grid4">' + "".join(f'<div>{"abcdefgh"[i]}) {x} {SQ(s_.replace("<","&lt;").replace(">","&gt;"), K)} {y}</div>' for i, (x, y, s_) in enumerate(cp)) + '</div></section>')

    # 9 FOCUS
    h.append('<section class="ex focus"><span class="tagf">FOCUS · EXERCICE 23 PAGE 43</span>')
    h.append('<h2 style="margin-top:6px"><span class="n">9</span>Ordonner des nombres décimaux<span class="pts">… / 4</span></h2>')
    rule = "1,25 point si tout est juste ; 0,5 point pour une seule erreur"
    h.append('<p class="consigne">a) Range ces nombres dans l’ordre <u>croissant</u> (du plus petit au plus grand).' + pts(K, rule) + '</p>')
    h.append('<div class="nums">' + "".join(f'<span>{x}</span>' for x in ["0,6", "0,06", "0,66", "0,16", "1,6", "0,61"]) + '</div>')
    ca = ["0,06", "0,16", "0,6", "0,61", "0,66", "1,6"]
    h.append('<div class="order">' + " <b>&lt;</b> ".join(B(x, K) for x in ca) + '</div>')
    h.append('<p class="consigne" style="margin-top:8px">b) Range ces nombres dans l’ordre <u>décroissant</u> (du plus grand au plus petit).' + pts(K, rule) + '</p>')
    h.append('<div class="nums">' + "".join(f'<span>{x}</span>' for x in ["9,4", "9,04", "9,41", "9,14", "8,94", "9,44"]) + '</div>')
    cb = ["9,44", "9,41", "9,4", "9,14", "9,04", "8,94"]
    h.append('<div class="order">' + " <b>&gt;</b> ".join(B(x, K) for x in cb) + '</div>')
    h.append('<p class="consigne" style="margin-top:8px">c) Emma a écrit : « 0,16 &gt; 0,6 car 16 est plus grand que 6. » A-t-elle raison ? Explique.' + pts(K, "0,25 point pour « non », 0,5 point pour l’explication") + '</p>')
    h.append('<div class="answer-box">Non. Les parties entières sont égales (0), on compare les dixièmes : 0,6 a 6 dixièmes et 0,16 a 1 dixième. 6 &gt; 1, donc 0,6 &gt; 0,16. On peut aussi écrire 0,6 = 0,60 : 60 centièmes &gt; 16 centièmes.</div>'
             if K else '<div class="lines"><div class="line"></div><div class="line"></div></div>')
    h.append('<p class="consigne" style="margin-top:8px">d) Entoure le plus grand nombre : <b>3,09</b> ou <b>3,1</b>. Justifie ta réponse.' + pts(K, "0,25 point pour 3,1, 0,5 point pour la justification") + '</p>')
    h.append('<div class="answer-box">3,1 est le plus grand. Les unités sont égales (3), on compare les dixièmes : 1 &gt; 0. Ou bien : 3,1 = 3,10 et 10 centièmes &gt; 9 centièmes.</div>'
             if K else '<div class="lines"><div class="line"></div><div class="line"></div></div>')
    if K: h.append('<p class="bareme">Pièges visés (comme dans l’exercice 23) : 0,6 placé après 0,16 ou 0,61 ; 9,4 placé après 9,14 ; 8,94 placé avant 9,04 parce que « 94 &gt; 4 ».</p>')
    h.append('</section>')

    if K:
        h.append('<section class="ex" style="margin-top:8px"><h2><span class="n">✓</span>Récapitulatif du barème<span class="pts">20</span></h2>'
                 '<table class="comp" style="font-size:9pt;margin-top:4px"><tr><th style="text-align:left">Compétence</th><th>Exercices</th><th>Points</th></tr>' +
                 "".join(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td style="text-align:center">{p}</td></tr>' for c, e, p in comps) +
                 '</table><p class="bareme" style="margin-top:6px">Repère possible : compétence acquise si au moins 75 % des points, en cours entre 40 % et 75 %, non acquise en dessous.</p></section>')
    else:
        h.append('<p class="foot">Relis bien tes réponses avant de rendre ta copie. Bon courage !</p>')
    h.append('</body></html>')
    return "".join(h)

open(os.path.join(OUT, "evaluation-sujet.html"), "w").write(doc(False))
open(os.path.join(OUT, "evaluation-corrige.html"), "w").write(doc(True))
