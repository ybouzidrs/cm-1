# Usage : python3 generer.py <dossier de sortie> <chemin de sciences/periode-1/evaluation/generer.py (styles communs)>
import sys, os, re
OUT = sys.argv[1]
CSS = re.search(r'CSS = """(.*?)"""', open(sys.argv[2]).read(), re.S).group(1)
CSS += """
table.grid { width: 100%; border-collapse: collapse; }
table.grid td, table.grid th { border: 1.2px solid #555; padding: 5px 8px; }
table.grid th { background: #eee; font-size: 10pt; }
table.grid td.c, table.grid th.c { width: 70px; text-align: center; }
.field { display: flex; gap: 6px; align-items: baseline; margin: 5px 0; }
.field .blank { flex: 1; min-width: 0; }
.cols2 { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 22px; }
.ticks { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px 14px; margin: 4px 0 6px; }
svg.frise { max-width: 180mm; }
.steps { display: grid; gap: 6px; }
.steps div { display: grid; grid-template-columns: 34px 1fr; gap: 8px; align-items: center; }
.steps .num { border: 1.5px solid #111; border-radius: 6px; height: 26px; text-align: center; font-weight: 700; line-height: 24px; }
.who { display: grid; grid-template-columns: 1fr 40px 40px 160px; row-gap: 10px; align-items: center; }
.who .dot { text-align: center; font-size: 16pt; }
"""
def B(a, K, c=""): return f'<span class="blank filled ans">{a}</span>' if K else f'<span class="blank {c}"></span>'
def pts(K, t): return f' <span class="bareme">({t})</span>' if K else ''
def box(K, on): return f'<span class="box{" x" if (K and on) else ""}"></span>'

def frise(K):
    xs = [48, 170, 315, 460, 590, 718]          # limites : -3 millions, -3000, 476, 1492, 1789, 2020
    dates = ["-3 millions", "-3000", "476", "1492", "1789", "2020"]
    given = {0, 5}
    names = ["Préhistoire", "Antiquité", "Moyen Âge", "Temps modernes", "Époque contemporaine"]
    s = ['<svg class="frise" viewBox="0 0 770 175" role="img" aria-label="Frise chronologique des grandes périodes de l’histoire">',
         '<polygon points="30,70 730,70 760,105 730,140 30,140" fill="#f4f4f4" stroke="#111" stroke-width="2"/>',
         f'<rect x="{xs[2]}" y="70" width="{xs[3]-xs[2]}" height="70" fill="#dcdcdc"/>',
         '<polygon points="30,70 730,70 760,105 730,140 30,140" fill="none" stroke="#111" stroke-width="2"/>']
    for i, x in enumerate(xs):
        s.append(f'<line x1="{x}" y1="58" x2="{x}" y2="140" stroke="#111" stroke-width="{2 if i in given else 1.5}" stroke-dasharray="{"" if i in given else "4 3"}"/>')
        if i in given or K:
            col = "#111" if i in given else "#c0392b"
            s.append(f'<text x="{x}" y="50" text-anchor="middle" font-size="15" font-weight="700" fill="{col}">{dates[i]}</text>')
        else:
            s.append(f'<rect x="{x-32}" y="26" width="64" height="28" rx="5" fill="#fff" stroke="#111" stroke-width="1.5"/>')
    for i, n in enumerate(names):
        cx = (xs[i] + xs[i + 1]) / 2
        if K:
            parts = n.split(" ") if len(n) > 11 else [n]
            for k, p in enumerate(parts):
                s.append(f'<text x="{cx}" y="{110 + (k - (len(parts) - 1) / 2) * 17}" text-anchor="middle" font-size="14" font-weight="700" fill="#c0392b">{p}</text>')
        else:
            s.append(f'<line x1="{cx-55}" y1="114" x2="{cx+55}" y2="114" stroke="#222" stroke-width="1.4" stroke-dasharray="2 3"/>')
        s.append(f'<circle cx="{cx}" cy="160" r="11" fill="#111"/><text x="{cx}" y="165" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">{"ABCDE"[i]}</text>')
    s.append('</svg>')
    return "".join(s)

def doc(K):
    h = [f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{"Corrigé · " if K else ""}Évaluation d’histoire · Le temps des rois</title>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Lilita+One&display=swap">'
         f'<style>{CSS}</style></head><body>']
    h.append('<div class="head"><div><div class="theme">Histoire · Thème 1 · Le temps des rois · Mérovingiens</div>')
    h.append(f'<h1>{"Corrigé et barème &nbsp;<span class=tag>ENSEIGNANT</span>" if K else "Évaluation d’histoire"}</h1>')
    h.append('<div style="margin-top:6px;font-size:10.5pt">Réponses attendues en <b class="ans">rouge</b>. Le barème est indiqué à droite de chaque titre (total : 20 points).</div>' if K else '<div class="ident"><span>Prénom :</span><span>Date :</span></div>')
    h.append('</div><div class="note"><small>Note</small><b>' + ('<em>20</em>' if K else '&nbsp;&nbsp;&nbsp;') + ' / 20</b></div></div>')
    comps = [("Je sais situer les grandes périodes de l’histoire sur une frise chronologique.", "1", "3"),
             ("Je sais lire une carte et expliquer comment Clovis agrandit le royaume des Francs.", "2", "3"),
             ("Je comprends un récit historique (le vase de Soissons).", "3", "3"),
             ("Je connais les grandes dates et les grands faits du règne de Clovis.", "4", "3,5"),
             ("Je connais les personnages de l’époque mérovingienne.", "5", "2"),
             ("Je connais l’héritage de Clovis et des Mérovingiens.", "6 · 7", "4,5"),
             ("Je connais le vocabulaire de la leçon.", "8", "1")]
    if not K:
        h.append('<table class="comp"><tr><th style="text-align:left">Compétences évaluées</th><th>Exercices</th><th class="c">Acquis</th><th class="c">En cours</th><th class="c">Non acquis</th></tr>'
                 + "".join(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td class="c"></td><td class="c"></td><td class="c"></td></tr>' for c, e, _ in comps) + '</table>')

    # 1 Frise
    h.append('<section class="ex"><h2><span class="n">1</span>La frise chronologique<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">a) Écris les 4 dates qui manquent dans les cases, puis le nom de chaque période sur les pointillés.' + pts(K, "0,25 point par date et par période") + '</p>')
    h.append('<div class="bank">Antiquité · Époque contemporaine · Préhistoire · Moyen Âge · Temps modernes</div>')
    h.append(frise(K))
    h.append('<ol class="alpha">'
             f'<li><span>b)</span><span>Le Moyen Âge commence en {B("476", K, "s")} avec la chute de {B("l’Empire romain", K)}.{pts(K, "0,25 point par case")}</span></li>'
             f'<li><span>c)</span><span>Clovis a vécu pendant la période (lettre) {B("C", K, "s")} : {B("le Moyen Âge", K)}.{pts(K, "0,25 point en tout")}</span></li></ol>')
    if K: h.append('<p class="bareme">Total : 4 dates (1 point) + 5 périodes (1,25 point) + b) 0,5 point + c) 0,25 point = 3 points. Pour c), accepter la lettre ou le nom de la période.</p>')
    h.append('</section>')

    # 2 Carte / conquêtes
    h.append('<section class="ex"><h2><span class="n">2</span>Clovis agrandit le royaume des Francs<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">a) En 481, quand Clovis devient roi, quels peuples se partagent la Gaule ? Coche les 5 bonnes réponses.' + pts(K, "0,25 point par case juste, cochée ou laissée vide") + '</p>')
    peu = [("les Francs", False), ("les Wisigoths", True), ("les Vikings", False), ("les Burgondes", True),
           ("les Ostrogoths", True), ("les Égyptiens", False), ("les Alamans", True), ("le royaume de Syagrius", True)]
    h.append('<div class="ticks">' + "".join(f'<span>{box(K, v)} {n}</span>' for n, v in peu) + '</div>')
    if K: h.append('<p class="bareme">Total : 8 cases (2 points) + b) 0,5 point + c) 0,5 point = 3 points. Les Francs sont le peuple de Clovis : la question porte sur les « autres » peuples. Accepter si l’élève coche aussi « les Francs » en expliquant qu’ils sont en Gaule (0,25 point non retiré).</p>')
    h.append('<ol class="alpha">'
             f'<li><span>b)</span><span>À la mort de Clovis, en 511, la capitale de son royaume est {B("Paris", K)}.{pts(K, "0,5 point")}</span></li>'
             f'<li><span>c)</span><span>Clovis conquiert presque toute la Gaule. Quel royaume ne conquiert-il pas ? Pourquoi ?{pts(K, "0,25 point le royaume, 0,25 point l’explication")}</span></li></ol>')
    h.append('<div class="answer-box">Le royaume des Burgondes, car sa femme, Clotilde, est la princesse de ce royaume.</div>' if K else '<div class="lines"><div class="line"></div><div class="line"></div></div>')
    h.append('</section>')

    # 3 Vase de Soissons
    h.append('<section class="ex"><h2><span class="n">3</span>Le vase de Soissons<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">a) Numérote les événements de 1 à 5 dans l’ordre de l’histoire.' + pts(K, "1,5 point si tout est juste ; 0,75 point pour une seule erreur") + '</p>')
    ev = [("Un soldat frappe le vase avec sa hache : « Tu n’auras que ce que le sort te donnera. »", 3),
          ("Après une bataille, les Francs partagent le butin à Soissons.", 1),
          ("L’année suivante, Clovis jette les armes du soldat par terre.", 4),
          ("Clovis demande qu’on lui donne un vase magnifique pour le rendre à l’évêque.", 2),
          ("Clovis frappe le soldat avec sa hache : « C’est ainsi que tu as fait à Soissons avec le vase. »", 5)]
    h.append('<div class="steps">' + "".join(f'<div><span class="num {"ans" if K else ""}">{r if K else ""}</span><span>{t}</span></div>' for t, r in ev) + '</div>')
    h.append(f'<p class="consigne" style="margin-top:8px">b) Pourquoi Clovis se venge-t-il du soldat ? Que veut-il montrer à ses guerriers ?{pts(K, "1,5 point")}</p>')
    h.append('<div class="answer-box">Le soldat lui a désobéi devant tous ses guerriers. Clovis veut montrer que c’est lui le chef (le roi) et que tout le monde doit lui obéir.<br><span class="bareme">0,5 point pour la désobéissance du soldat, 1 point pour l’idée que Clovis montre qu’il est le chef et qu’on doit lui obéir.</span></div>' if K
             else '<div class="lines"><div class="line"></div><div class="line"></div><div class="line"></div></div>')
    h.append('</section>')

    # 4 Texte à trous
    h.append('<section class="ex"><h2><span class="n">4</span>Clovis, le premier roi catholique<span class="pts">… / 3,5</span></h2>')
    h.append('<p class="consigne">Complète le texte avec les mots de la liste.' + pts(K, "0,5 point par mot") + '</p>')
    h.append('<div class="bank">VIII<sup>e</sup> · Tolbiac · 481 · Mérovingiens · Reims · catholiques · 496</div>')
    h.append('<p class="texte">Quand Clovis monte sur le trône en ' + B("481", K, "s") + ', il devient le roi des Francs. En ' + B("496", K, "s") +
             ', Clovis se fait baptiser à ' + B("Reims", K) + ' par l’évêque Rémi. Il avait promis de se convertir si Dieu lui accordait la victoire lors de la bataille de ' + B("Tolbiac", K) +
             '. Les rois de France qui succéderont à Clovis seront ' + B("catholiques", K) + '. Clovis fonde la première dynastie de France : les ' + B("Mérovingiens", K) +
             ', qui régneront du V<sup>e</sup> au ' + B("VIII<sup>e</sup>", K, "s") + ' siècle.</p>')
    if K: h.append('<p class="bareme">Attention : Rémi est un évêque (l’évêque de Reims), pas un pape. Dans le cahier, l’illustration est légendée « le pape Rémi » : c’est à corriger avec l’élève.</p>')
    h.append('</section>')

    # 5 Personnages
    h.append('<section class="ex"><h2><span class="n">5</span>Qui est-ce ?<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Relie chaque personnage à sa description. Attention, il y a une description en trop.' + pts(K, "0,5 point par liaison juste") + '</p>')
    left = ["Clotilde", "Rémi", "Dagobert", "Brunehaut"]
    right = ["Roi mérovingien très populaire : il fit des conquêtes, créa des monastères et rendit la justice.",
             "Reine accusée d’avoir tué plus de dix rois.",
             "Femme de Clovis, princesse burgonde et chrétienne : elle pousse Clovis à se convertir.",
             "Chef romain dont Clovis conquiert le royaume.",
             "Évêque de Reims qui baptise Clovis et lui conseille de bien s’entendre avec les évêques."]
    sol = {0: 2, 1: 4, 2: 0, 3: 1}
    if K:
        h.append('<ol class="alpha">' + "".join(f'<li><span>•</span><span><b>{left[i]}</b> → <span class="ans">{right[sol[i]]}</span></span></li>' for i in range(4)) + '</ol>')
        h.append('<p class="bareme">La description en trop : le chef romain (Syagrius).</p>')
    else:
        rows = []
        for i in range(5):
            l = f'<b>{left[i]}</b>' if i < 4 else ''
            d1 = '<span class="dot">•</span>' if i < 4 else '<span></span>'
            rows.append(f'<span>{l}</span>{d1}<span class="dot">•</span><span style="grid-column:4/5"></span>')
        h.append('<div style="display:grid;grid-template-columns:130px 30px 70px 30px 1fr;row-gap:10px;align-items:center">' +
                 "".join(f'<span><b>{left[i] if i < 4 else ""}</b></span><span class="dot" style="text-align:center;font-size:16pt">{"•" if i < 4 else ""}</span><span></span><span class="dot" style="text-align:center;font-size:16pt">•</span><span style="font-size:10.5pt">{right[i]}</span>' for i in range(5)) + '</div>')
    h.append('</section>')

    # 6 Héritage VF
    h.append('<section class="ex"><h2><span class="n">6</span>L’héritage des Mérovingiens<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Coche la bonne case.' + pts(K, "0,5 point par ligne") + '</p>')
    vf = [("D’après la loi salique, les filles peuvent hériter de la terre de leur père.", False, "Ce sont les garçons qui héritent de toute la terre."),
          ("La loi salique ne concerne pas la succession des rois.", True, ""),
          ("Le prix du sang est une amende à payer quand on a commis un crime ou une injure.", True, ""),
          ("Pour le meurtre d’un noble franc, il fallait payer 30 sous d’or.", False, "600 sous d’or (30 sous d’or pour une blessure grave)."),
          ("Le roi Dagobert créa de nombreux monastères ; saint Éloi était l’un de ses conseillers.", True, ""),
          ("L’époque mérovingienne fut une époque calme, sans violence.", False, "Elle est marquée par la violence, les meurtres et les pillages.")]
    h.append('<table class="vf"><tr><th style="text-align:left">Affirmation</th><th class="c">Vrai</th><th class="c">Faux</th></tr>')
    for t, v, why in vf:
        h.append(f'<tr><td>{t}{f"<br><span class=bareme>{why}</span>" if (K and why) else ""}</td><td class="c">{box(K, v)}</td><td class="c">{box(K, not v)}</td></tr>')
    h.append('</table></section>')

    # 7 Mort de Clovis
    h.append('<section class="ex"><h2><span class="n">7</span>Après Clovis<span class="pts">… / 1,5</span></h2>')
    h.append('<p class="consigne">Complète.' + pts(K, "0,5 point par case") + '</p>')
    h.append('<p class="texte">Clovis meurt en ' + B("511", K, "s") + '. Ses quatre fils se ' + B("partagent son royaume", K, "l") +
             ', mais très vite ils se font la guerre. Plus tard, c’est la période des « rois ' + B("fainéants", K) + ' », qui laissent leur pouvoir aux chefs de leur cour.</p>')
    h.append('</section>')

    # 8 Lexique
    h.append('<section class="ex"><h2><span class="n">8</span>Le vocabulaire<span class="pts">… / 1</span></h2>')
    h.append('<p class="consigne">Complète les définitions.' + pts(K, "0,5 point par définition") + '</p><ol class="alpha">'
             f'<li><span>•</span><span><b>Une monarchie</b> : système de gouvernement dans lequel le pouvoir est entre les mains d’{B("une seule personne", K, "l")}, le plus souvent un roi.</span></li>'
             f'<li><span>•</span><span><b>Un royaume</b> : au début du Moyen Âge, c’est un territoire gouverné par {B("un roi", K)}.</span></li></ol>')
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
