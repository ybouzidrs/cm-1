# Fiche complémentaire « Focus exercice 23 » : 3 exercices pour ordonner et justifier.
# Usage : python3 generer-focus.py <dossier de sortie> <chemin de sciences/periode-1/evaluation/generer.py (styles communs)>
import sys, os, re
OUT = sys.argv[1]
CSS = re.search(r'CSS = """(.*?)"""', open(sys.argv[2]).read(), re.S).group(1)
CSS += """
.nums { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: 4px 0 8px; }
.nums span { border: 1.5px solid #111; border-radius: 7px; padding: 2px 12px; font-weight: 700; font-size: 13pt; background: #f2f2f2; }
.order { display: flex; align-items: center; gap: 4px; flex-wrap: wrap; margin: 4px 0 6px; }
.order .blank { min-width: 62px; text-align: center; }
.order b { font-size: 14pt; }
.q { margin: 8px 0 2px; font-weight: 700; }
table.res { border-collapse: collapse; margin: 4px auto 8px; }
table.res td, table.res th { border: 1.2px solid #555; padding: 4px 14px; text-align: center; }
table.res th { background: #eee; }
table.rk { width: 100%; border-collapse: collapse; margin-top: 4px; }
table.rk td, table.rk th { border: 1.2px solid #555; padding: 4px 8px; text-align: center; font-size: 10.5pt; }
table.rk th { background: #eee; }
.hint { font-size: 10pt; color: #444; font-style: italic; }
"""
def B(a, K, c=""): return f'<span class="blank filled ans">{a}</span>' if K else f'<span class="blank {c}"></span>'
def pts(K, t): return f' <span class="bareme">({t})</span>' if K else ''
def lines(n): return '<div class="lines">' + '<div class="line"></div>' * n + '</div>'
def ans(K, t, n=2): return f'<div class="answer-box">{t}</div>' if K else lines(n)
def nums(l): return '<div class="nums">' + "".join(f'<span>{x}</span>' for x in l) + '</div>'
def order(l, sign, K): return '<div class="order">' + f" <b>{sign}</b> ".join(B(x, K) for x in l) + '</div>'
RULE = "1,5 point si tout est juste ; 0,75 point pour une seule erreur"

def doc(K):
    h = [f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{"Corrigé · " if K else ""}Focus exercice 23 · Ordonner et justifier</title>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Lilita+One&display=swap">'
         f'<style>{CSS}</style></head><body>']
    h.append('<div class="head"><div><div class="theme">Mathématiques · Nombres décimaux · Focus exercice 23 page 43</div>')
    h.append(f'<h1>{"Corrigé &nbsp;<span class=tag>ENSEIGNANT</span>" if K else "Ordonner et justifier"}</h1>')
    h.append('<div style="margin-top:6px;font-size:10.5pt">Réponses attendues en <b class="ans">rouge</b>. Total : 12 points (4 par exercice).</div>' if K else '<div class="ident"><span>Prénom :</span><span>Date :</span></div>')
    h.append('</div><div class="note"><small>Note</small><b>' + ('<em>12</em>' if K else '&nbsp;&nbsp;&nbsp;') + ' / 12</b></div></div>')
    if not K:
        h.append('<p class="hint" style="margin-top:8px">Pour justifier, pense à comparer d’abord les parties entières, puis les dixièmes, puis les centièmes. Tu peux aussi ajouter un 0 à la fin d’un nombre (3,5 = 3,50) sans changer sa valeur.</p>')

    # A
    h.append('<section class="ex"><h2><span class="n">1</span>Ordre croissant<span class="pts">… / 4</span></h2>')
    h.append('<p class="consigne">a) Range ces nombres dans l’ordre <u>croissant</u> (du plus petit au plus grand).' + pts(K, RULE) + '</p>')
    h.append(nums(["3,5", "3,05", "3,55", "3,15", "0,35", "3,51"]))
    h.append(order(["0,35", "3,05", "3,15", "3,5", "3,51", "3,55"], "&lt;", K))
    h.append('<p class="q">b) Pourquoi 0,35 est-il le plus petit de tous ?' + pts(K, "1 point") + '</p>')
    h.append(ans(K, "Sa partie entière est 0, alors que tous les autres nombres ont 3 unités. 0 &lt; 3, donc 0,35 est le plus petit.", 1))
    h.append('<p class="q">c) Compare 3,5 et 3,51. Lequel est le plus grand ? Justifie.' + pts(K, "0,5 point la réponse, 1 point la justification") + '</p>')
    h.append(ans(K, "3,51 est le plus grand. Les parties entières sont égales (3) et les dixièmes aussi (5). On compare les centièmes : 3,5 = 3,50, donc 0 centième &lt; 1 centième. 3,5 &lt; 3,51."))
    h.append('</section>')

    # B
    h.append('<section class="ex"><h2><span class="n">2</span>Ordre décroissant<span class="pts">… / 4</span></h2>')
    h.append('<p class="consigne">a) Range ces nombres dans l’ordre <u>décroissant</u> (du plus grand au plus petit).' + pts(K, RULE) + '</p>')
    h.append(nums(["7,8", "7,08", "7,18", "8,07", "7,81", "7,1"]))
    h.append(order(["8,07", "7,81", "7,8", "7,18", "7,1", "7,08"], "&gt;", K))
    h.append('<p class="q">b) Sami a écrit : « 7,18 &gt; 7,8 car 18 est plus grand que 8. » Explique son erreur.' + pts(K, "1,5 point") + '</p>')
    h.append(ans(K, "Les parties entières sont égales (7), on compare donc les dixièmes : 7,8 a 8 dixièmes et 7,18 a 1 dixième. 8 &gt; 1, donc 7,8 &gt; 7,18. On peut aussi écrire 7,8 = 7,80 : 80 centièmes &gt; 18 centièmes. Ce n’est pas le nombre de chiffres après la virgule qui compte."))
    h.append('<p class="q">c) Pourquoi 8,07 est-il le plus grand, alors qu’il a un 0 après la virgule ?' + pts(K, "1 point") + '</p>')
    h.append(ans(K, "On compare d’abord les parties entières : 8 &gt; 7. Donc 8,07 est plus grand que tous les nombres qui commencent par 7, quels que soient leurs chiffres après la virgule.", 1))
    h.append('</section>')

    # C
    h.append('<section class="ex"><h2><span class="n">3</span>PROBLÈME · Le concours de saut en longueur<span class="pts">… / 4</span></h2>')
    h.append('<p>Voici les sauts de six élèves de CM1 :</p>')
    data = [("Inès", "2,9 m"), ("Tom", "2,09 m"), ("Léa", "2,19 m"), ("Noé", "2,91 m"), ("Ali", "2,1 m"), ("Zoé", "1,99 m")]
    h.append('<table class="res"><tr>' + "".join(f'<th>{n}</th>' for n, _ in data) + '</tr><tr>' + "".join(f'<td>{v}</td>' for _, v in data) + '</tr></table>')
    h.append('<p class="consigne">a) Complète le classement, du saut le plus long (1<sup>er</sup>) au plus court (6<sup>e</sup>).' + pts(K, RULE) + '</p>')
    rk = [("Noé", "2,91 m"), ("Inès", "2,9 m"), ("Léa", "2,19 m"), ("Ali", "2,1 m"), ("Tom", "2,09 m"), ("Zoé", "1,99 m")]
    h.append('<table class="rk"><tr><th>Place</th>' + "".join(f'<th>{i}<sup>{"er" if i == 1 else "e"}</sup></th>' for i in range(1, 7)) + '</tr>'
             '<tr><th>Élève</th>' + "".join(f'<td class="{"ans" if K else ""}" style="height:26px;{"color:#c0392b;font-weight:700" if K else ""}">{n if K else ""}</td>' for n, _ in rk) + '</tr>'
             '<tr><th>Saut</th>' + "".join(f'<td style="{"color:#c0392b;font-weight:700" if K else ""}">{v if K else ""}</td>' for _, v in rk) + '</tr></table>')
    h.append('<p class="q">b) Tom dit : « J’ai sauté plus loin qu’Ali, car 2,09 a plus de chiffres que 2,1. » A-t-il raison ? Justifie en écrivant les deux nombres avec des centièmes.' + pts(K, "0,5 point pour « non », 1 point pour la justification") + '</p>')
    h.append(ans(K, "Non. 2,1 = 2,10. On compare 2,10 et 2,09 : les unités sont égales (2), puis les dixièmes : 1 &gt; 0. Donc 2,10 &gt; 2,09 : c’est Ali qui a sauté plus loin."))
    h.append('<p class="q">c) Noé et Inès ont-ils sauté la même longueur ? Explique.' + pts(K, "1 point") + '</p>')
    h.append(ans(K, "Non. 2,9 = 2,90 et 2,91 = 2,91 : 90 centièmes &lt; 91 centièmes. Noé a sauté 1 centième de mètre (1 cm) plus loin qu’Inès.", 1))
    h.append('</section>')
    if not K: h.append('<p class="foot">Relis bien tes réponses. Bon courage !</p>')
    h.append('</body></html>')
    return "".join(h)

open(os.path.join(OUT, "focus-ex23-exercices.html"), "w").write(doc(False))
open(os.path.join(OUT, "focus-ex23-corrige.html"), "w").write(doc(True))
