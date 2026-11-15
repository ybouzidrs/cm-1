# Usage : python3 generer.py <dossier de sortie> <chemin de sciences/periode-1/evaluation/generer.py (styles communs)>
import sys, os, re
OUT = sys.argv[1]
CSS = re.search(r'CSS = """(.*?)"""', open(sys.argv[2]).read(), re.S).group(1)
CSS += """
table.grid { width: 100%; border-collapse: collapse; }
table.grid td, table.grid th { border: 1.2px solid #555; padding: 5px 8px; }
table.grid th { background: #eee; font-size: 10pt; }
table.grid td.c, table.grid th.c { width: 64px; text-align: center; }
.field { display: flex; gap: 6px; align-items: baseline; margin: 5px 0; }
.field .blank { flex: 1; min-width: 0; }
.qcm { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 22px; }
.qcm .q { font-weight: 700; margin-bottom: 2px; }
.qcm .opts { display: flex; flex-direction: column; gap: 2px; }
.rel { display: grid; grid-template-columns: 170px 30px 50px 30px 1fr; row-gap: 9px; align-items: center; }
.rel .dot { text-align: center; font-size: 16pt; }
.doc { border: 1.5px solid #555; border-radius: 8px; padding: 6px 12px; background: #fafafa; font-size: 10.5pt; line-height: 1.5; margin: 4px 0 6px; }
.doc .src { font-size: 9pt; color: #555; text-align: right; }
"""
def B(a, K, c=""): return f'<span class="blank filled ans">{a}</span>' if K else f'<span class="blank {c}"></span>'
def pts(K, t): return f' <span class="bareme">({t})</span>' if K else ''
def box(K, on): return f'<span class="box{" x" if (K and on) else ""}"></span>'
def ans(K, t, n=2): return f'<div class="answer-box">{t}</div>' if K else '<div class="lines">' + '<div class="line"></div>' * n + '</div>'

def relie(K, left, right, sol, lw=170):
    if K:
        return '<ol class="alpha">' + "".join(f'<li><span>•</span><span><b>{left[i]}</b> → <span class="ans">{right[sol[i]]}</span></span></li>' for i in range(len(left))) + '</ol>'
    n = max(len(left), len(right))
    return (f'<div class="rel" style="grid-template-columns:{lw}px 30px 50px 30px 1fr">' + "".join(
        f'<span><b>{left[i] if i < len(left) else ""}</b></span><span class="dot">{"•" if i < len(left) else ""}</span><span></span>'
        f'<span class="dot">{"•" if i < len(right) else ""}</span><span>{right[i] if i < len(right) else ""}</span>' for i in range(n)) + '</div>')

def doc(K):
    h = [f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{"Corrigé · " if K else ""}Évaluation 2 d’histoire · Le temps des rois</title>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Lilita+One&display=swap">'
         f'<style>{CSS}</style>' + ('<style>body{font-size:10.5pt;line-height:1.38} .ex{margin-top:9px}</style>' if K else '') + '</head><body>']
    h.append('<div class="head"><div><div class="theme">Histoire · Thème 1 · Le temps des rois · Mérovingiens · Évaluation 2</div>')
    h.append(f'<h1>{"Corrigé et barème &nbsp;<span class=tag>ENSEIGNANT</span>" if K else "Évaluation d’histoire"}</h1>')
    h.append('<div style="margin-top:6px;font-size:10.5pt">Réponses attendues en <b class="ans">rouge</b>. Le barème est indiqué à droite de chaque titre (total : 20 points).</div>' if K else '<div class="ident"><span>Prénom :</span><span>Date :</span></div>')
    h.append('</div><div class="note"><small>Note</small><b>' + ('<em>20</em>' if K else '&nbsp;&nbsp;&nbsp;') + ' / 20</b></div></div>')
    comps = [("Je connais les grandes dates de l’époque de Clovis et je les situe dans le temps.", "1", "3"),
             ("Je sais expliquer comment Clovis agrandit le royaume des Francs.", "2", "3"),
             ("Je comprends un document historique (le serment de Clovis, la lettre de Rémi).", "3", "3"),
             ("Je connais les grands faits du règne de Clovis.", "4 · 5", "5"),
             ("Je connais l’héritage des Mérovingiens.", "6 · 7", "4"),
             ("Je connais le vocabulaire de la leçon.", "8", "2")]
    if not K:
        h.append('<table class="comp"><tr><th style="text-align:left">Compétences évaluées</th><th>Exercices</th><th class="c">Acquis</th><th class="c">En cours</th><th class="c">Non acquis</th></tr>'
                 + "".join(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td class="c"></td><td class="c"></td><td class="c"></td></tr>' for c, e, _ in comps) + '</table>')

    # 1 Dates
    h.append('<section class="ex"><h2><span class="n">1</span>Les grandes dates<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">a) Relie chaque date à l’événement qui lui correspond.' + pts(K, "0,5 point par liaison juste") + '</p>')
    h.append(relie(K, ["476", "481", "496", "511"],
                   ["Clovis se fait baptiser à Reims.", "Clovis meurt ; ses quatre fils se partagent le royaume.", "Chute de l’Empire romain : début du Moyen Âge.", "Clovis devient roi des Francs."],
                   {0: 2, 1: 3, 2: 0, 3: 1}, lw=90))
    h.append('<ol class="alpha" style="margin-top:8px">'
             f'<li><span>b)</span><span>Le Moyen Âge commence en {B("476", K, "s")} et se termine en {B("1492", K, "s")}.{pts(K, "0,25 point par date")}</span></li>'
             f'<li><span>c)</span><span>Clovis devient roi en 481 et meurt en 511. Pendant combien d’années a-t-il régné ? {B("30 ans", K, "s")}{pts(K, "0,5 point")}</span></li></ol>')
    h.append('</section>')

    # 2 Cartes VF
    h.append('<section class="ex"><h2><span class="n">2</span>Le royaume des Francs s’agrandit<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Souviens-toi des cartes de la Gaule en 481 et en 511. Coche Vrai ou Faux.' + pts(K, "0,5 point par ligne") + '</p>')
    vf = [("En 481, quand Clovis devient roi, le royaume des Francs se trouve au nord de la Gaule.", True, ""),
          ("En 481, la Gaule est occupée par plusieurs peuples : Wisigoths, Burgondes, Alamans, Ostrogoths…", True, ""),
          ("Clovis conquiert le royaume de Syagrius.", True, ""),
          ("Clovis conquiert le royaume des Burgondes.", False, "Il ne le conquiert pas : sa femme Clotilde est une princesse burgonde."),
          ("À la mort de Clovis, en 511, la capitale du royaume est Soissons.", False, "La capitale est Paris."),
          ("En 511, le royaume de Clovis s’étend sur presque toute la Gaule.", True, "")]
    h.append('<table class="vf"><tr><th style="text-align:left">Affirmation</th><th class="c">Vrai</th><th class="c">Faux</th></tr>')
    for t, v, why in vf:
        h.append(f'<tr><td>{t}{f"<br><span class=bareme>{why}</span>" if (K and why) else ""}</td><td class="c">{box(K, v)}</td><td class="c">{box(K, not v)}</td></tr>')
    h.append('</table></section>')

    # 3 Documents
    h.append('<section class="ex"><h2><span class="n">3</span>Le serment de Clovis et la lettre de Rémi<span class="pts">… / 3</span></h2>')
    h.append('<div class="doc">« Ô Jésus-Christ que Clotilde proclame fils du Dieu vivant… Si tu m’accordes la victoire sur ces ennemis, je croirai en toi et me ferai baptiser en ton nom. »<div class="src">Le serment de Clovis, d’après Jonas de Bobbio, VII<sup>e</sup> siècle</div></div>')
    h.append(f'<p class="consigne">a) Qui incite Clovis à invoquer Jésus-Christ ? {B("Clotilde, sa femme", K)}{pts(K, "0,5 point")}</p>')
    h.append('<p class="consigne">b) Que promet Clovis s’il gagne la bataille ?' + pts(K, "1 point") + '</p>')
    h.append(ans(K, "Il promet de croire en Jésus-Christ et de se faire baptiser (de devenir chrétien).", 1))
    h.append('<p class="consigne">c) Dans sa lettre, l’évêque Rémi donne des conseils à Clovis. Coche les 3 bons conseils.' + pts(K, "0,25 point par case juste, cochée ou laissée vide") + '</p>')
    cons = [("s’entourer de conseillers", True), ("faire la guerre aux évêques", False), ("bien s’entendre avec les évêques", True),
            ("piller les églises", False), ("aider les veuves et nourrir les orphelins", True), ("ne jamais écouter personne", False)]
    h.append('<div class="qcm">' + "".join(f'<span>{box(K, v)} {t}</span>' for t, v in cons) + '</div></section>')

    # 4 QCM
    h.append('<section class="ex"><h2><span class="n">4</span>Le règne de Clovis<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Coche la bonne réponse.' + pts(K, "0,5 point par question") + '</p>')
    qs = [("Clovis est le roi…", ["des Francs", "des Romains", "des Burgondes"], 0),
          ("Clovis promet de se convertir pendant la bataille de…", ["Soissons", "Tolbiac", "Reims"], 1),
          ("Clovis est baptisé à…", ["Paris", "Soissons", "Reims"], 2),
          ("Clovis est baptisé par…", ["l’évêque Rémi", "le roi Dagobert", "saint Éloi"], 0),
          ("Les rois qui succèdent à Clovis seront…", ["romains", "catholiques", "burgondes"], 1),
          ("La dynastie fondée par Clovis s’appelle…", ["les Carolingiens", "les Romains", "les Mérovingiens"], 2)]
    h.append('<div class="qcm">' + "".join(
        f'<div><div class="q">{"abcdef"[i]}) {q}</div><div class="opts">' + "".join(f'<span>{box(K, j == k)} {o}</span>' for j, o in enumerate(opts)) + '</div></div>'
        for i, (q, opts, k) in enumerate(qs)) + '</div></section>')

    # 5 Vase
    h.append('<section class="ex"><h2><span class="n">5</span>Le vase de Soissons<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Complète le résumé avec les mots de la liste.' + pts(K, "0,25 point par mot") + '</p>')
    h.append('<div class="bank">hache · évêque · butin · soldat · Soissons · vase</div>')
    h.append('<p class="texte">Après une bataille, les Francs partagent le ' + B("butin", K) + ' à ' + B("Soissons", K) + '. Clovis demande un ' + B("vase", K) +
             ' magnifique pour le rendre à l’' + B("évêque", K) + '. Mais un ' + B("soldat", K) + ' frappe le vase avec sa hache. L’année suivante, Clovis tue ce soldat avec sa ' + B("hache", K) + '.</p>')
    h.append(f'<p class="consigne">Que montre cette histoire ? Clovis est un roi {B("guerrier", K)} qui veut être {B("obéi", K)} de tous.{pts(K, "0,25 point par mot")}</p>')
    if K: h.append('<p class="bareme">Accepter « chef », « respecté » ou un mot de même sens.</p>')
    h.append('</section>')

    # 6 Héritage relie
    h.append('<section class="ex"><h2><span class="n">6</span>L’héritage des Mérovingiens<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Relie chaque mot à son explication.' + pts(K, "0,5 point par liaison juste") + '</p>')
    h.append(relie(K, ["la loi salique", "le prix du sang", "Dagobert", "saint Éloi", "Brunehaut", "les « rois fainéants »"],
                   ["Reine accusée d’avoir tué plus de dix rois ; elle fut attachée à la queue d’un cheval.",
                    "Rois qui laissent leur pouvoir aux chefs de leur cour.",
                    "Loi des Francs : les filles ne peuvent pas hériter de la terre de leur père.",
                    "Conseiller du roi Dagobert.",
                    "Amende à payer quand on a commis un crime ou prononcé une injure.",
                    "Roi mérovingien très populaire ; une monnaie le représente."],
                   {0: 2, 1: 4, 2: 5, 3: 3, 4: 0, 5: 1}))
    h.append('</section>')

    # 7 Prix du sang
    h.append('<section class="ex"><h2><span class="n">7</span>Histoire et calcul : le prix du sang<span class="pts">… / 1</span></h2>')
    h.append('<p>Pour une blessure grave, il fallait payer <b>30 sous d’or</b>. Pour le meurtre d’un noble franc, il fallait payer <b>600 sous d’or</b>.</p>')
    h.append(f'<ol class="alpha"><li><span>a)</span><span>Un homme blesse gravement deux personnes. Combien doit-il payer ? {B("60 sous d’or", K)}{pts(K, "0,5 point")}</span></li>'
             f'<li><span>b)</span><span>Le meurtre d’un noble franc coûte combien de fois plus cher qu’une blessure grave ? {B("20 fois", K, "s")}{pts(K, "0,5 point")}</span></li></ol>')
    if K: h.append('<p class="bareme">a) 30 × 2 = 60 ; b) 600 ÷ 30 = 20 (ou 30 × 20 = 600). Pour b), la question montre que « le prix à payer dépendait de l’importance de la victime ».</p>')
    h.append('</section>')

    # 8 Lexique
    h.append('<section class="ex"><h2><span class="n">8</span>Le vocabulaire<span class="pts">… / 2</span></h2>')
    h.append('<ol class="alpha">'
             f'<li><span>a)</span><span>Système de gouvernement dans lequel le pouvoir est entre les mains d’une seule personne, le plus souvent un roi : {B("la monarchie", K)}{pts(K, "0,5 point")}</span></li>'
             f'<li><span>b)</span><span>Au début du Moyen Âge, territoire gouverné par un roi : {B("un royaume", K)}{pts(K, "0,5 point")}</span></li>'
             f'<li><span>c)</span><span>Le mot « royaume » désigne aussi l’ensemble des {B("habitants du royaume", K)}.{pts(K, "0,5 point")}</span></li>'
             f'<li><span>d)</span><span>Le royaume des Francs est-il une monarchie ? Justifie.{pts(K, "0,5 point")}</span></li></ol>')
    h.append(ans(K, "Oui, car le pouvoir est entre les mains d’une seule personne : le roi (Clovis).", 1))
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
