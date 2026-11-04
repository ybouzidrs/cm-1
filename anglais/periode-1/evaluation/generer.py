import sys, os, re
OUT = sys.argv[1]
src = open(sys.argv[2]).read()  # sciences/periode-1/evaluation/generer.py : styles communs
CSS = re.search(r'CSS = """(.*?)"""', src, re.S).group(1)
CSS += """
table.grid { width: 100%; border-collapse: collapse; }
table.grid td, table.grid th { border: 1.2px solid #555; padding: 6px 8px; vertical-align: middle; }
table.grid th { background: #eee; font-size: 10pt; }
table.grid td.n { width: 30px; text-align: center; font-family: "Lilita One", sans-serif; font-size: 13pt; }
table.grid td.ans { color: #c0392b; font-weight: 700; }
.uk-row { display: grid; grid-template-columns: 72mm 1fr; gap: 14px; align-items: center; }
svg.uk { max-width: 72mm; }
.field { display: flex; gap: 6px; align-items: baseline; margin: 6px 0; }
.field .blank { flex: 1; min-width: 0; }
.cols2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 22px; }
.cols4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px 14px; }
.numcell { display: flex; gap: 8px; align-items: baseline; }
.numcell b { font-family: "Lilita One", sans-serif; font-weight: 400; font-size: 14pt; min-width: 26px; text-align: right; }
.numcell .blank { flex: 1; min-width: 0; }
.writing .line { height: 30px; }
"""

def B(ans, key, cls=""):
    return f'<span class="blank filled ans">{ans}</span>' if key else f'<span class="blank {cls}"></span>'
def pts(K, t): return f' <span class="bareme">({t})</span>' if K else ''

# ---------- Carte schématique du Royaume-Uni (longitude, latitude approximatives) ----------
K_X, LON0, LAT0, SC = 0.58, -11.0, 59.0, 40
def P(lon, lat): return ((lon - LON0) * K_X * SC + 8, (LAT0 - lat) * SC + 6)
def poly(pts_, fill, stroke="#111", w=1.6):
    return '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in (P(*p) for p in pts_)) + f'" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>'
B_EW = [(-2.65,51.6),(-2.7,51.85),(-3.05,52.0),(-3.1,52.3),(-3.0,52.6),(-3.05,52.95),(-2.75,53.0),(-3.0,53.2),(-3.1,53.3)]
B_ES = [(-3.05,54.98),(-2.7,55.1),(-2.35,55.35),(-2.2,55.45),(-2.35,55.6),(-2.0,55.77)]
EAST_ENG = [(-2.0,55.77),(-1.43,55.0),(-0.6,54.5),(-0.08,54.12),(0.12,53.6),(0.35,53.15),(0.2,52.9),(0.5,52.95),(1.3,52.93),(1.75,52.48),(1.35,51.95),(1.15,51.79),(0.6,51.5),(1.4,51.38),(1.33,51.13),(0.6,50.85),(-0.14,50.82),(-1.1,50.78),(-1.9,50.7),(-2.45,50.6),(-2.95,50.72),(-3.4,50.6),(-3.65,50.22),(-4.15,50.36),(-5.2,49.96),(-5.71,50.07),(-5.48,50.21),(-4.95,50.55),(-4.53,51.02),(-4.12,51.21),(-3.47,51.21),(-2.98,51.35),(-2.65,51.6)]
WEST_ENG = [(-3.1,53.3),(-3.05,53.45),(-3.0,53.65),(-3.05,53.82),(-2.9,54.07),(-3.25,54.1),(-3.65,54.5),(-3.57,54.65),(-3.4,54.87),(-3.05,54.98)]
ENGLAND = EAST_ENG + B_EW[1:] + WEST_ENG[1:] + B_ES[1:-1]
WALES = [(-2.65,51.6),(-2.98,51.55),(-3.17,51.45),(-3.95,51.6),(-4.3,51.56),(-4.7,51.67),(-5.3,51.88),(-4.98,52.0),(-4.65,52.1),(-4.08,52.42),(-4.05,52.72),(-4.7,52.8),(-4.3,53.15),(-4.6,53.3),(-4.4,53.42),(-4.05,53.3),(-3.83,53.33),(-3.5,53.33),(-3.1,53.3)] + list(reversed(B_EW))[1:-1]
SCOTLAND = [(-2.0,55.77),(-2.5,56.0),(-3.2,56.0),(-2.58,56.28),(-2.9,56.45),(-2.47,56.7),(-2.08,57.15),(-1.78,57.5),(-2.0,57.69),(-3.3,57.72),(-3.85,57.6),(-4.2,57.48),(-4.0,57.85),(-3.65,58.1),(-3.1,58.4),(-3.05,58.65),(-4.0,58.55),(-5.0,58.6),(-5.3,58.25),(-5.25,57.9),(-5.7,57.73),(-5.8,57.55),(-5.7,57.28),(-5.83,57.0),(-6.2,56.73),(-5.5,56.42),(-5.5,56.2),(-5.6,55.75),(-5.7,55.3),(-5.4,55.6),(-4.85,55.95),(-4.87,55.8),(-4.63,55.46),(-4.86,55.25),(-5.15,55.0),(-5.05,54.9),(-4.86,54.64),(-4.4,54.68),(-4.05,54.8),(-3.6,54.88),(-3.25,54.97),(-3.05,54.98)] + B_ES[1:-1]
NI_BORDER = [(-6.1,54.03),(-6.27,54.1),(-6.65,54.05),(-7.05,54.2),(-7.4,54.15),(-7.6,54.3),(-8.15,54.45),(-7.9,54.65),(-7.55,54.75),(-7.4,55.0),(-7.25,55.05)]
NI = [(-7.25,55.05),(-6.9,55.17),(-6.15,55.22),(-5.95,54.95),(-5.9,54.65),(-5.45,54.45),(-5.55,54.3),(-5.9,54.2),(-6.1,54.03)] + NI_BORDER[1:-1]
IRELAND = [(-6.1,54.03),(-6.15,53.35),(-6.0,52.97),(-6.35,52.2),(-7.0,52.13),(-8.3,51.8),(-9.8,51.45),(-10.3,51.9),(-10.45,52.15),(-9.9,52.6),(-9.4,52.95),(-9.05,53.25),(-10.1,53.45),(-10.2,53.95),(-10.0,54.2),(-8.6,54.3),(-8.15,54.6),(-8.8,54.7),(-8.25,55.15),(-7.37,55.38),(-7.25,55.05)] + list(reversed(NI_BORDER))[1:-1]

def uk_map(key):
    w = (2.0 - LON0) * K_X * SC + 16; h = (LAT0 - 49.8) * SC + 12
    s = [f'<svg class="uk" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="Carte simplifiée du Royaume-Uni">',
         '<defs><pattern id="hz" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#bbb" stroke-width="1.2"/></pattern></defs>',
         poly(IRELAND, "url(#hz)", "#888", 1.2),
         poly(SCOTLAND, "#e6e6e6"), poly(ENGLAND, "#ffffff"), poly(WALES, "#cfcfcf"), poly(NI, "#cfcfcf")]
    for n, (lon, lat) in enumerate([(-1.6, 52.6), (-4.3, 57.0), (-3.7, 52.25), (-6.65, 54.62)], 1):
        x, y = P(lon, lat)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="#111"/><text x="{x:.1f}" y="{y+5:.1f}" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">{n}</text>')
    x, y = P(-8.7, 52.6)
    s.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" font-size="10" fill="#666">Irlande</text><text x="{x:.1f}" y="{y+12:.1f}" text-anchor="middle" font-size="8.5" fill="#666">(pas dans le R.-U.)</text>')
    s.append('</svg>')
    return "".join(s)

def doc(K):
    title = "Corrigé et barème" if K else "English test"
    h = [f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
         f'<title>{"Corrigé · " if K else ""}Évaluation d’anglais · Période 1</title>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Lilita+One&display=swap">'
         f'<style>{CSS}</style></head><body>']
    h.append('<div class="head"><div><div class="theme">Anglais · Période 1 · Bilan</div>')
    h.append(f'<h1>{title}{" &nbsp;<span class=tag>ENSEIGNANT</span>" if K else ""}</h1>')
    if K:
        h.append('<div style="margin-top:6px;font-size:10.5pt">Réponses attendues en <b class="ans">rouge</b>. Le barème de chaque exercice est indiqué à droite du titre (total : 20 points).</div>')
    else:
        h.append('<div class="ident"><span>Name :</span><span>Date :</span></div>')
    h.append('</div><div class="note"><small>Note</small><b>' + ('<em>20</em>' if K else '&nbsp;&nbsp;&nbsp;') + ' / 20</b></div></div>')
    comps = [("Je connais les pays du Royaume-Uni, je sais les placer et je connais leur emblème.", "1", "4"),
             ("Je sais me présenter en 3 phrases.", "2", "3"),
             ("Je connais les nombres jusqu’à 20.", "3", "4"),
             ("Je connais les jours de la semaine.", "4", "3"),
             ("Je connais les couleurs.", "5", "3"),
             ("Je connais le vocabulaire d’Halloween.", "6", "3")]
    if not K:
        h.append('<table class="comp"><tr><th style="text-align:left">Compétences évaluées</th><th>Exercice</th><th class="c">Acquis</th><th class="c">En cours</th><th class="c">Non acquis</th></tr>')
        for c, e, _ in comps:
            h.append(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td class="c"></td><td class="c"></td><td class="c"></td></tr>')
        h.append('</table>')

    # 1 UK
    h.append('<section class="ex"><h2><span class="n">1</span>The United Kingdom<span class="pts">… / 4</span></h2>')
    h.append('<p class="consigne">Le Royaume-Uni est formé de 4 pays. Pour chaque numéro de la carte, écris le nom du pays <u>en anglais</u>, sa capitale et son emblème.' + pts(K, "pays 0,5 point · capitale 0,25 · emblème 0,25") + '</p>')
    h.append('<div class="bank">Capitales : London · Edinburgh · Cardiff · Belfast &nbsp;&nbsp;|&nbsp;&nbsp; Emblèmes : la rose · le chardon · le poireau · le trèfle</div>')
    rows = [("England", "London", "la rose"), ("Scotland", "Edinburgh", "le chardon"), ("Wales", "Cardiff", "le poireau"), ("Northern Ireland", "Belfast", "le trèfle")]
    t = '<table class="grid"><tr><th></th><th>Country (en anglais)</th><th>Capital</th><th>Emblème</th></tr>'
    for i, (c, cap, em) in enumerate(rows, 1):
        if K:
            t += f'<tr><td class="n">{i}</td><td class="ans">{c}</td><td class="ans">{cap}</td><td class="ans">{em}</td></tr>'
        else:
            t += f'<tr><td class="n">{i}</td><td style="height:34px"></td><td></td><td></td></tr>'
    t += '</table>'
    h.append(f'<div class="uk-row"><div>{uk_map(K)}</div><div>{t}</div></div>')
    if K:
        h.append('<p class="bareme">Orthographe attendue : England, Scotland, Wales, Northern Ireland (majuscules). Pour le pays de Galles, accepter aussi « la jonquille ». Le trèfle (shamrock) est l’emblème de l’Irlande du Nord, le chardon (thistle) celui de l’Écosse.</p>')
    h.append('</section>')

    # 2 Introduce yourself
    h.append('<section class="ex"><h2><span class="n">2</span>Introduce yourself<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Présente-toi en 3 phrases : ton prénom, ton âge (écris le nombre en lettres) et ta couleur préférée.' + pts(K, "1 point par phrase") + '</p>')
    if K:
        h.append('<div class="answer-box">Réponse personnelle. Exemple : My name is Lina. I’m nine years old. My favourite colour is blue.<br>'
                 '<span class="bareme">1 point par phrase si la structure est juste : « My name is… », « I’m … years old » avec le nombre écrit en lettres, « My favourite colour is… » avec une couleur en anglais. Accepter « favorite » et « I am ». Retirer 0,5 point si le nombre est écrit en chiffres.</span></div>')
    else:
        h.append('<div class="writing"><div class="field"><span>1.</span><span class="blank"></span></div><div class="field"><span>2.</span><span class="blank"></span></div><div class="field"><span>3.</span><span class="blank"></span></div></div>')
    h.append('</section>')

    # 3 Numbers
    h.append('<section class="ex"><h2><span class="n">3</span>Numbers<span class="pts">… / 4</span></h2>')
    h.append('<p class="consigne">a) Écris les nombres en lettres.' + pts(K, "0,25 point par nombre") + '</p>')
    nums = [(3, "three"), (8, "eight"), (11, "eleven"), (12, "twelve"), (13, "thirteen"), (15, "fifteen"), (18, "eighteen"), (20, "twenty")]
    h.append('<div class="cols2">' + "".join(f'<div class="numcell"><b>{n}</b>{B(w, K)}</div>' for n, w in nums) + '</div>')
    h.append('<p class="consigne" style="margin-top:10px">b) Écris le nombre en chiffres.' + pts(K, "0,25 point par nombre") + '</p>')
    words = [("seven", "7"), ("fourteen", "14"), ("nineteen", "19"), ("sixteen", "16")]
    h.append('<div class="cols4">' + "".join(f'<div class="field"><span>{w} =</span>{B(n, K, "s")}</div>' for w, n in words) + '</div>')
    h.append('<p class="consigne" style="margin-top:10px">c) Calcule et écris le résultat en lettres.' + pts(K, "0,25 point par calcul") + '</p>')
    calc = [("two + four", "six"), ("ten + seven", "seventeen"), ("five + five", "ten"), ("twelve − three", "nine")]
    h.append('<div class="cols2">' + "".join(f'<div class="field"><span>{a} =</span>{B(r, K)}</div>' for a, r in calc) + '</div>')
    h.append('</section>')

    # 4 Days
    h.append('<section class="ex"><h2><span class="n">4</span>Days of the week<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">a) Complète avec les jours qui manquent.' + pts(K, "0,25 point par jour") + '</p>')
    h.append('<p class="texte">Monday – ' + B("Tuesday", K) + ' – Wednesday – ' + B("Thursday", K) + ' – Friday – ' + B("Saturday", K) + ' – ' + B("Sunday", K) + '</p>')
    h.append('<p class="consigne">b) Complète le tableau.' + pts(K, "0,25 point par case") + '</p>')
    tbl = [("Sunday", "Monday", "Tuesday", (0,)), ("Wednesday", "Thursday", "Friday", (2,)), ("Friday", "Saturday", "Sunday", (0,)), ("Monday", "Tuesday", "Wednesday", (1,))]
    t = '<table class="grid"><tr><th>Yesterday</th><th>Today</th><th>Tomorrow</th></tr>'
    for a, b, c, holes in tbl:
        cells = []
        for j, v in enumerate((a, b, c)):
            if j in holes:
                cells.append(f'<td class="ans" style="text-align:center">{v}</td>' if K else '<td style="height:30px"></td>')
            else:
                cells.append(f'<td style="text-align:center">{v}</td>')
        t += '<tr>' + "".join(cells) + '</tr>'
    t += '</table>'
    h.append(t)
    h.append('<p class="consigne" style="margin-top:8px">c) Les jours du week-end : The week-end days are ' + B("Saturday", K) + ' and ' + B("Sunday", K) + '.' + pts(K, "0,5 point par jour") + '</p>')
    if K:
        h.append('<p class="bareme">Accepter les jours sans majuscule, mais signaler qu’en anglais les jours prennent toujours une majuscule.</p>')
    h.append('</section>')

    # 5 Colours
    h.append('<section class="ex"><h2><span class="n">5</span>Colours<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">a) Écris la couleur en anglais.' + pts(K, "0,25 point par couleur") + '</p>')
    cols = [("rouge", "red"), ("bleu", "blue"), ("vert", "green"), ("jaune", "yellow"), ("noir", "black"), ("blanc", "white"), ("rose", "pink"), ("marron", "brown")]
    h.append('<div class="cols2">' + "".join(f'<div class="field"><span style="min-width:62px">{f} =</span>{B(e, K)}</div>' for f, e in cols) + '</div>')
    h.append('<p class="consigne" style="margin-top:10px">b) What colour is it? Réponds avec « It’s … ».' + pts(K, "0,25 point par réponse") + '</p>')
    qs = [("a pumpkin", "It’s orange."), ("a ghost", "It’s white."), ("a black cat", "It’s black."), ("the cross of the English flag", "It’s red.")]
    h.append('<div class="cols2">' + "".join(f'<div class="field"><span>{q} →</span>{B(a, K)}</div>' for q, a in qs) + '</div>')
    if K:
        h.append('<p class="bareme">Accepter la couleur seule (« orange » au lieu de « It’s orange. ») avec 0,25 point quand même si la couleur est juste.</p>')
    h.append('</section>')

    # 6 Halloween
    h.append('<section class="ex"><h2><span class="n">6</span>Halloween<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Écris le mot anglais. Attention, il y a deux mots en trop dans la liste.' + pts(K, "0,5 point par mot") + '</p>')
    h.append('<div class="bank">a ghost · a witch · a pumpkin · a bat · a spider · a skeleton · a haunted house · a vampire</div>')
    hal = [("une sorcière", "a witch"), ("une citrouille", "a pumpkin"), ("une chauve-souris", "a bat"), ("une araignée", "a spider"), ("un squelette", "a skeleton"), ("une maison hantée", "a haunted house")]
    h.append('<div class="cols2">' + "".join(f'<div class="field"><span style="min-width:128px">{f} =</span>{B(e, K)}</div>' for f, e in hal) + '</div>')
    if K:
        h.append('<p class="bareme">Les deux mots en trop : a ghost (un fantôme) et a vampire (un vampire). Accepter le mot sans « a ».</p>')
    h.append('</section>')

    if K:
        h.append('<section class="ex" style="margin-top:8px"><h2><span class="n">✓</span>Récapitulatif du barème<span class="pts">20</span></h2>'
                 '<table class="comp" style="font-size:9pt;margin-top:4px"><tr><th style="text-align:left">Compétence</th><th>Exercice</th><th>Points</th></tr>' +
                 "".join(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td style="text-align:center">{p}</td></tr>' for c, e, p in comps) +
                 '</table><p class="bareme" style="margin-top:6px">Repère possible : compétence acquise si au moins 75 % des points, en cours entre 40 % et 75 %, non acquise en dessous.</p></section>')
    else:
        h.append('<p class="foot">Check your answers! Good luck!</p>')
    h.append('</body></html>')
    return "".join(h)

open(os.path.join(OUT, "evaluation-sujet.html"), "w").write(doc(False))
open(os.path.join(OUT, "evaluation-corrige.html"), "w").write(doc(True))
