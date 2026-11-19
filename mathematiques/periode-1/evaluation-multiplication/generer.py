# Usage : python3 generer.py <dossier de sortie> <chemin de sciences/periode-1/evaluation/generer.py (styles communs)>
import sys, os, re
OUT = sys.argv[1]
CSS = re.search(r'CSS = """(.*?)"""', open(sys.argv[2]).read(), re.S).group(1)
CSS += """
.grid4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px 16px; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 22px; }
.it { display: flex; gap: 6px; align-items: baseline; white-space: nowrap; }
.it .blank { flex: 1; min-width: 44px; }
.it .blank.s { flex: 0 0 90px; min-width: 90px; }
.chain { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; font-size: 13pt; margin: 6px 0; }
.chain .op { font-size: 10pt; font-weight: 700; text-align: center; line-height: 1; }
.chain .op span { display: block; font-size: 15pt; }
.chain .blank { min-width: 80px; text-align: center; }
table.tb { border-collapse: collapse; margin: 4px auto; }
table.tb td, table.tb th { border: 1.2px solid #555; padding: 5px 22px; text-align: center; min-width: 90px; height: 26px; }
table.tb th { background: #eee; }
table.tb td.ans { color: #c0392b; font-weight: 700; }
.calc { margin: 6px 0; }
.calc .blank { min-width: 150px; }
.pb { margin-top: 8px; }
.pb p { margin: 0 0 2px; }
"""
def B(a, K, c=""): return f'<span class="blank filled ans">{a}</span>' if K else f'<span class="blank {c}"></span>'
def pts(K, t): return f' <span class="bareme">({t})</span>' if K else ''
def ans(K, t, n=2): return f'<div class="answer-box">{t}</div>' if K else '<div class="lines">' + '<div class="line"></div>' * n + '</div>'

def doc(K):
    h = [f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{"Corrigé · " if K else ""}Évaluation de mathématiques · Multiplier par 10, 100, 20, 50, 500</title>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Lilita+One&display=swap">'
         f'<style>{CSS}</style>' + ('<style>body{font-size:10.5pt;line-height:1.38} .ex{margin-top:9px}</style>' if K else '') + '</head><body>']
    h.append('<div class="head"><div><div class="theme">Mathématiques · Calcul · Multiplier par 10, 100, 20, 200, 50, 500… (pages 52-53)</div>')
    h.append(f'<h1>{"Corrigé et barème &nbsp;<span class=tag>ENSEIGNANT</span>" if K else "Évaluation de mathématiques"}</h1>')
    h.append('<div style="margin-top:6px;font-size:10.5pt">Réponses attendues en <b class="ans">rouge</b>. Le barème est indiqué à droite de chaque titre (total : 20 points).</div>' if K else '<div class="ident"><span>Prénom :</span><span>Date :</span></div>')
    h.append('</div><div class="note"><small>Note</small><b>' + ('<em>20</em>' if K else '&nbsp;&nbsp;&nbsp;') + ' / 20</b></div></div>')
    comps = [("Je multiplie un nombre par 10 et par 100.", "1 · 2 · 3", "5"),
             ("Je multiplie un nombre par 20, 50, 200, 500… en décomposant le calcul.", "4 · 5 · 6 · 7", "9"),
             ("Je décompose une multiplication pour la calculer (× 21, × 51…).", "8", "2"),
             ("Je résous des problèmes en utilisant ces multiplications.", "9", "4")]
    if not K:
        h.append('<table class="comp"><tr><th style="text-align:left">Compétences évaluées</th><th>Exercices</th><th class="c">Acquis</th><th class="c">En cours</th><th class="c">Non acquis</th></tr>'
                 + "".join(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td class="c"></td><td class="c"></td><td class="c"></td></tr>' for c, e, _ in comps) + '</table>')

    # 1
    h.append('<section class="ex"><h2><span class="n">1</span>Multiplier par 10 et par 100<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Calcule sans poser l’opération.' + pts(K, "0,25 point par calcul") + '</p>')
    c1 = [("8 × 10", "80"), ("47 × 10", "470"), ("9 × 100", "900"), ("36 × 100", "3 600"), ("250 × 10", "2 500"), ("415 × 100", "41 500"), ("100 × 100", "10 000"), ("6 800 × 10", "68 000")]
    h.append('<div class="grid4">' + "".join(f'<div class="it">{"abcdefgh"[i]}) {c} = {B(a, K)}</div>' for i, (c, a) in enumerate(c1)) + '</div></section>')

    # 2 chaîne
    h.append('<section class="ex"><h2><span class="n">2</span>La chaîne des multiplications<span class="pts">… / 1</span></h2>')
    h.append('<p class="consigne">Complète.' + pts(K, "0,25 point par case") + '</p>')
    vals = ["700", "7 000", "70 000", "700 000"]; ops = ["× 100", "× 10", "× 10", "× 10"]
    h.append('<div class="chain"><b>7</b>' + "".join(f'<span class="op">{o}<span>→</span></span>{B(v, K)}' for o, v in zip(ops, vals)) + '</div></section>')

    # 3
    h.append('<section class="ex"><h2><span class="n">3</span>Le nombre manquant<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Complète.' + pts(K, "0,25 point par case") + '</p>')
    c3 = [("34 × ", " = 3 400", "100"), ("190 × ", " = 1 900", "10"), ("60 × ", " = 6 000", "100"), ("2 507 × ", " = 25 070", "10"),
          ("(", " × 4) × 10 = 200", "5"), ("(6 × ", ") × 100 = 4 200", "7"), ("(3 × 9) × 10 = ", "", "270"), ("(5 × 60) × 100 = ", "", "30 000")]
    h.append('<div class="grid2">' + "".join(f'<div class="it">{"abcdefgh"[i]}) {a}{B(r, K, "s")}{b}</div>' for i, (a, b, r) in enumerate(c3)) + '</div></section>')

    # 4 méthode
    h.append('<section class="ex"><h2><span class="n">4</span>Multiplier par 20, 50 et 500<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Calcule en écrivant les étapes, comme dans l’exemple.' + pts(K, "1 point par calcul : 0,5 point pour les étapes, 0,5 point pour le résultat") + '</p>')
    h.append('<p style="margin:2px 0 6px">Exemple : 21 × 50 = (21 × 5) × 10 = 105 × 10 = 1 050</p>')
    c4 = [("14 × 20", "(14 × 2) × 10", "28 × 10", "280"), ("23 × 50", "(23 × 5) × 10", "115 × 10", "1 150"), ("12 × 500", "(12 × 5) × 100", "60 × 100", "6 000")]
    for i, (c, s1, s2, r) in enumerate(c4):
        h.append(f'<div class="calc it">{"abc"[i]}) {c} = {B(s1, K)} = {B(s2, K)} = {B(r, K)}</div>')
    h.append('</section>')

    # 5
    h.append('<section class="ex"><h2><span class="n">5</span>Calcul rapide<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Calcule sans poser l’opération.' + pts(K, "0,25 point par calcul") + '</p>')
    c5 = [("4 × 30", "120"), ("6 × 50", "300"), ("8 × 500", "4 000"), ("50 × 50", "2 500"), ("7 × 200", "1 400"), ("9 × 60", "540"), ("25 × 20", "500"), ("3 × 500", "1 500")]
    h.append('<div class="grid4">' + "".join(f'<div class="it">{"abcdefgh"[i]}) {c} = {B(a, K)}</div>' for i, (c, a) in enumerate(c5)) + '</div></section>')

    # 6
    h.append('<section class="ex"><h2><span class="n">6</span>Complète les multiplications<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Trouve le nombre manquant.' + pts(K, "0,25 point par case") + '</p>')
    c6 = [("40", "800", "20"), ("30", "1 500", "50"), ("50", "3 000", "60"), ("12", "6 000", "500"), ("25", "1 000", "40"), ("20", "1 800", "90"), ("15", "750", "50"), ("80", "4 000", "50")]
    h.append('<div class="grid4">' + "".join(f'<div class="it">{"abcdefgh"[i]}) {a} × {B(r, K, "s")} = {b}</div>' for i, (a, b, r) in enumerate(c6)) + '</div></section>')

    # 7 tableau
    h.append('<section class="ex"><h2><span class="n">7</span>Le tableau des × 50 et des × 500<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Complète le tableau.' + pts(K, "0,25 point par case") + '</p>')
    rows = [("14", "700", "7 000", (1, 2)), ("6", "300", "3 000", (1, 2)), ("9", "450", "4 500", (0, 2)), ("4", "200", "2 000", (0, 1))]
    t = '<table class="tb"><tr><th>Nombre donné</th><th>× 50</th><th>× 500</th></tr>'
    for *v, holes in rows:
        t += '<tr>' + "".join((f'<td class="ans">{x}</td>' if K else '<td></td>') if j in holes else f'<td>{x}</td>' for j, x in enumerate(v)) + '</tr>'
    h.append(t + '</table></section>')

    # 8 décomposer
    h.append('<section class="ex"><h2><span class="n">8</span>Décomposer pour calculer<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Décompose les multiplications pour les calculer, comme dans l’exemple.' + pts(K, "0,5 point par calcul") + '</p>')
    h.append('<p style="margin:2px 0 6px">Exemple : 9 × 51 = (9 × 50) + 9 = 450 + 9 = 459</p>')
    c8 = [("23 × 21", "(23 × 20) + 23", "460 + 23", "483"), ("14 × 51", "(14 × 50) + 14", "700 + 14", "714"),
          ("12 × 31", "(12 × 30) + 12", "360 + 12", "372"), ("42 × 21", "(42 × 20) + 42", "840 + 42", "882")]
    for i, (c, s1, s2, r) in enumerate(c8):
        h.append(f'<div class="calc it">{"abcd"[i]}) {c} = {B(s1, K)} = {B(s2, K)} = {B(r, K)}</div>')
    if K: h.append('<p class="bareme">Accepter un calcul juste fait autrement (par exemple 23 × 21 = (20 × 21) + (3 × 21)), si l’élève a bien décomposé.</p>')
    h.append('</section>')

    # 9 problèmes
    h.append('<section class="ex"><h2><span class="n">9</span>Problèmes<span class="pts">… / 4</span></h2>')
    h.append('<p class="consigne">Pour chaque problème, écris ton calcul et réponds par une phrase.' + pts(K, "1 point par problème : 0,5 point par question") + '</p>')
    pbs = [("a) Une ruche produit environ 20 kg de miel par an. Combien de kilogrammes de miel produisent 10 ruches ? et 50 ruches ?",
            "10 × 20 = 200 : 10 ruches produisent 200 kg de miel. · 50 × 20 = 1 000 : 50 ruches produisent 1 000 kg de miel."),
           ("b) L’entrée au planétarium coûte 6 € par élève. Combien paie la classe de CM1 qui compte 30 élèves ? Combien paient les 100 élèves de l’école ?",
            "30 × 6 = 180 : la classe paie 180 €. · 100 × 6 = 600 : les 100 élèves paient 600 €."),
           ("c) Le cœur d’un enfant bat environ 90 fois par minute. Combien de fois bat-il en 10 minutes ? en 50 minutes ?",
            "90 × 10 = 900 : il bat 900 fois en 10 minutes. · 90 × 50 = (90 × 5) × 10 = 450 × 10 = 4 500 : il bat 4 500 fois en 50 minutes."),
           ("d) Le directeur du centre de loisirs commande 12 boîtes de 500 pièces et 21 boîtes de 200 pièces. Combien de pièces y a-t-il dans les boîtes de 500 ? dans les boîtes de 200 ?",
            "12 × 500 = (12 × 5) × 100 = 6 000 pièces. · 21 × 200 = (21 × 2) × 100 = 4 200 pièces. (Total : 10 200 pièces.)")]
    for q, a in pbs:
        h.append(f'<div class="pb"><p>{q}</p>{ans(K, a, 3)}</div>')
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
