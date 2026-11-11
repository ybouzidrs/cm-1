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
    h.append('<div class="head"><div><div class="theme">Mathématiques · Nombres · Les nombres décimaux (pages 34 à 43)</div>')
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
    fr = [(54, 10, "5,4"), (3, 10, "0,3"), (356, 100, "3,56"), (4, 100, "0,04"), (109, 10, "10,9"), (19, 100, "0,19"), ("2 543", 10, "254,3"), (7, 100, "0,07")]
    h.append('<div class="grid4">' + "".join(f'<div class="it">{F(n, d)} = {B(a, K, "s")}</div>' for n, d, a in fr) + '</div></section>')

    # 2
    h.append('<section class="ex"><h2><span class="n">2</span>Décompositions et nombres décimaux<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Écris chaque somme sous la forme d’un nombre décimal.' + pts(K, "0,5 point par nombre") + '</p>')
    so = [(f'3 + {F(4,10)} + {F(7,100)}', "3,47"), (f'25 + {F(6,100)}', "25,06"), (f'12 + {F(9,10)}', "12,9"), (f'{F(8,10)} + {F(5,100)}', "0,85")]
    h.append('<div class="grid2">' + "".join(f'<div class="it"><span>{"abcd"[i]})</span> {e} = {B(a, K, "s")}</div>' for i, (e, a) in enumerate(so)) + '</div>')
    if K: h.append('<p class="bareme">Erreur fréquente : 25 + 6/100 écrit « 25,6 » au lieu de 25,06.</p>')
    h.append('</section>')

    # 3
    h.append('<section class="ex"><h2><span class="n">3</span>La valeur du chiffre 7<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Indique ce que désigne le chiffre 7 dans chaque nombre : unités, dizaines, centaines, dixièmes ou centièmes.' + pts(K, "0,25 point par nombre") + '</p>')
    c7 = [("7,42", "unités"), ("74,51", "dizaines"), ("0,07", "centièmes"), ("13,7", "dixièmes"), ("709,25", "centaines"), ("1,27", "centièmes"), ("0,75", "dixièmes"), ("47,89", "unités")]
    h.append('<div class="grid4">' + "".join(f'<div class="it"><b>{n}</b> → {B(a, K)}</div>' for n, a in c7) + '</div></section>')

    # 4
    h.append('<section class="ex"><h2><span class="n">4</span>Lire et écrire les nombres décimaux<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Écris ces nombres en chiffres.' + pts(K, "0,25 point par nombre") + '</p>')
    ec = [("6 unités et 42 centièmes", "6,42"), ("12 unités et 9 dixièmes", "12,9"), ("Trois dixièmes", "0,3"), ("25 dixièmes", "2,5"),
          ("925 centièmes", "9,25"), ("2 centièmes", "0,02"), (f'31 + {F(7,10)} + {F(9,100)}', "31,79"), ("5 + 0,24", "5,24")]
    h.append('<div class="grid2">' + "".join(f'<div class="it"><span>{"abcdefgh"[i]}) {t} =</span>{B(a, K, "s")}</div>' for i, (t, a) in enumerate(ec)) + '</div></section>')

    # 5
    h.append('<section class="ex"><h2><span class="n">5</span>Égal ou différent ?<span class="pts">… / 1,5</span></h2>')
    h.append('<p class="consigne">Complète avec le signe = ou ≠.' + pts(K, "0,25 point par case") + '</p>')
    eg = [("12,50", "12,5", "="), ("14,2", "14,02", "≠"), ("1,8", "1,80", "="), ("15,02", "15,20", "≠"), ("14", "14,00", "="), ("0,5", "0,05", "≠")]
    h.append('<div class="grid4" style="grid-template-columns:repeat(3,1fr)">' + "".join(f'<div>{"abcdef"[i]}) {x} {SQ(s_, K)} {y}</div>' for i, (x, y, s_) in enumerate(eg)) + '</div>')
    if K: h.append('<p class="bareme">Les 0 à la fin de la partie décimale peuvent être supprimés sans changer la valeur du nombre.</p>')
    h.append('</section>')

    # 6
    h.append('<section class="ex"><h2><span class="n">6</span>La demi-droite graduée<span class="pts">… / 2,5</span></h2>')
    h.append('<p class="consigne">a) Écris le nombre décimal désigné par chaque lettre.' + pts(K, "0,25 point par lettre") + '</p>')
    lt = [("A", 4.3), ("B", 4.6), ("C", 4.8), ("D", 5.1), ("E", 5.5), ("F", 5.9)]
    h.append(droite(4, 6, letters=lt, K=K))
    if not K:
        h.append('<div class="grid4" style="grid-template-columns:repeat(6,1fr)">' + "".join(f'<div class="it"><b>{l}</b> = <span class="blank s"></span></div>' for l, _ in lt) + '</div>')
    h.append('<p class="consigne" style="margin-top:8px">b) Place ces nombres sur la demi-droite avec une flèche : <b>0,5</b> · <b>1,2</b> · <b>1,7</b> · <b>0,9</b>' + pts(K, "0,25 point par nombre bien placé") + '</p>')
    h.append(droite(0, 2, places=[0.5, 1.2, 1.7, 0.9], K=K))
    h.append('</section>')

    # 7
    h.append('<section class="ex"><h2><span class="n">7</span>Encadrer<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">a) Encadre chaque nombre entre deux nombres entiers qui se suivent.' + pts(K, "0,25 point par encadrement") + '</p>')
    e1 = [("5,3", "5", "6"), ("9,9", "9", "10"), ("0,09", "0", "1"), ("13,89", "13", "14")]
    h.append('<div class="grid4">' + "".join(f'<div class="it">{B(lo, K, "s")} &lt; <b>{n}</b> &lt; {B(hi, K, "s")}</div>' for n, lo, hi in e1) + '</div>')
    h.append('<p class="consigne" style="margin-top:8px">b) Encadre chaque nombre au dixième près.' + pts(K, "0,25 point par encadrement") + '</p>')
    e2 = [("7,61", "7,6", "7,7"), ("1,56", "1,5", "1,6"), ("2,44", "2,4", "2,5"), ("3,98", "3,9", "4")]
    h.append('<div class="grid4">' + "".join(f'<div class="it">{B(lo, K, "s")} &lt; <b>{n}</b> &lt; {B(hi, K, "s")}</div>' for n, lo, hi in e2) + '</div>')
    if K: h.append('<p class="bareme">Pour 3,98, accepter « 4 » ou « 4,0 ».</p>')
    h.append('</section>')

    # 8
    h.append('<section class="ex"><h2><span class="n">8</span>Comparer<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Complète avec &lt;, &gt; ou =.' + pts(K, "0,25 point par case") + '</p>')
    cp = [("3,41", "31,4", "<"), ("5,15", "6,15", "<"), ("0,2", "0,20", "="), ("8,2", "8,02", ">"),
          ("7,7", "7,65", ">"), ("6,01", "6,2", "<"), ("1,01", "1,10", "<"), ("3,25", "3,26", "<")]
    h.append('<div class="grid4">' + "".join(f'<div>{"abcdefgh"[i]}) {x} {SQ(s_.replace("<","&lt;").replace(">","&gt;"), K)} {y}</div>' for i, (x, y, s_) in enumerate(cp)) + '</div></section>')

    # 9 FOCUS
    h.append('<section class="ex focus"><span class="tagf">FOCUS · EXERCICE 23 PAGE 43</span>')
    h.append('<h2 style="margin-top:6px"><span class="n">9</span>Ordonner des nombres décimaux<span class="pts">… / 4</span></h2>')
    rule = "1,25 point si tout est juste ; 0,5 point pour une seule erreur"
    h.append('<p class="consigne">a) Range ces nombres dans l’ordre <u>croissant</u> (du plus petit au plus grand).' + pts(K, rule) + '</p>')
    h.append('<div class="nums">' + "".join(f'<span>{x}</span>' for x in ["0,34", "0,44", "0,04", "0,14", "1,04", "0,4"]) + '</div>')
    ca = ["0,04", "0,14", "0,34", "0,4", "0,44", "1,04"]
    h.append('<div class="order">' + " <b>&lt;</b> ".join(B(x, K) for x in ca) + '</div>')
    h.append('<p class="consigne" style="margin-top:8px">b) Range ces nombres dans l’ordre <u>décroissant</u> (du plus grand au plus petit).' + pts(K, rule) + '</p>')
    h.append('<div class="nums">' + "".join(f'<span>{x}</span>' for x in ["5,22", "5,3", "5,12", "4,02", "5,02", "4,2"]) + '</div>')
    cb = ["5,3", "5,22", "5,12", "5,02", "4,2", "4,02"]
    h.append('<div class="order">' + " <b>&gt;</b> ".join(B(x, K) for x in cb) + '</div>')
    h.append('<p class="consigne" style="margin-top:8px">c) Même travail avec de nouveaux nombres : range-les dans l’ordre <u>croissant</u>.' + pts(K, "0,75 point si tout est juste ; 0,25 point pour une seule erreur") + '</p>')
    h.append('<div class="nums">' + "".join(f'<span>{x}</span>' for x in ["2,3", "2,03", "3,02", "0,23", "2,33", "2,13"]) + '</div>')
    cc = ["0,23", "2,03", "2,13", "2,3", "2,33", "3,02"]
    h.append('<div class="order">' + " <b>&lt;</b> ".join(B(x, K) for x in cc) + '</div>')
    h.append('<p class="consigne" style="margin-top:8px">d) Léo dit : « 0,34 est plus grand que 0,4, car 34 est plus grand que 4. » A-t-il raison ? Explique.' + pts(K, "0,25 point pour « non », 0,5 point pour l’explication") + '</p>')
    h.append('<div class="answer-box">Non. Les parties entières sont égales (0), on compare donc les dixièmes : 4 dixièmes &gt; 3 dixièmes, donc 0,4 &gt; 0,34. On peut aussi écrire 0,4 = 0,40 et comparer 40 centièmes et 34 centièmes. Ce n’est pas le nombre de chiffres après la virgule qui compte, mais la valeur de ces chiffres.</div>'
             if K else '<div class="lines"><div class="line"></div><div class="line"></div></div>')
    if K: h.append('<p class="bareme">Pièges visés (comme dans l’exercice 23) : 0,4 placé après 0,34 ou 0,44 ; 4,2 placé après 4,02 ; 5,3 placé après 5,22 parce que « 3 &lt; 22 ».</p>')
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
