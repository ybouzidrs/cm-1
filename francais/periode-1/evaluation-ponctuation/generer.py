# Usage : python3 generer.py <dossier de sortie> <chemin de sciences/periode-1/evaluation/generer.py (styles communs)>
import sys, os, re
OUT = sys.argv[1]
CSS = re.search(r'CSS = """(.*?)"""', open(sys.argv[2]).read(), re.S).group(1)
CSS += """
table.grid { width: 100%; border-collapse: collapse; }
table.grid td, table.grid th { border: 1.2px solid #555; padding: 5px 8px; }
table.grid th { background: #eee; font-size: 10pt; }
table.grid td.sg { width: 60px; text-align: center; font-size: 20pt; font-weight: 700; font-family: "Times New Roman", serif; }
table.grid td.c { width: 70px; text-align: center; }
.sq { display: inline-block; min-width: 26px; height: 24px; border: 1.5px solid #111; border-radius: 5px; vertical-align: middle; text-align: center; line-height: 22px; margin: 0 3px; font-weight: 700; font-family: "Times New Roman", serif; font-size: 14pt; }
.sq.ans { color: #c0392b; border-color: #c0392b; }
.lines-p { line-height: 2.3; }
.bank.signs { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; }
.chip-s { display: inline-block; min-width: 34px; padding: 0 8px; border: 1.5px solid #111; border-radius: 6px; text-align: center; font-family: "Times New Roman", serif; font-size: 16pt; font-weight: 700; line-height: 28px; background: #fff; }
.sign { font-family: "Times New Roman", serif; font-size: 14pt; font-weight: 700; padding: 0 3px; }
.choice2 { display: grid; grid-template-columns: 22px 1fr; gap: 4px 6px; margin: 2px 0 6px 18px; }
.qcm { display: flex; gap: 18px; flex-wrap: wrap; margin: 2px 0 6px 22px; }
"""
def B(a, K, c=""): return f'<span class="blank filled ans">{a}</span>' if K else f'<span class="blank {c}"></span>'
def pts(K, t): return f' <span class="bareme">({t})</span>' if K else ''
def box(K, on): return f'<span class="box{" x" if (K and on) else ""}"></span>'
def BANK(signs): return '<div class="bank signs">' + "".join(f'<span class="chip-s">{x}</span>' for x in signs) + '</div>'
def SQ(a, K): return f'<span class="sq ans">{a}</span>' if K else '<span class="sq"></span>'

def doc(K):
    h = [f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{"Corrigé · " if K else ""}Évaluation de grammaire · La ponctuation</title>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Lilita+One&display=swap">'
         f'<style>{CSS}</style>' + ('<style>body{font-size:10.5pt;line-height:1.38} .ex{margin-top:9px} .bank{margin:2px 0 4px;padding:3px 8px} table.grid td,table.grid th,table.vf td{padding:3px 8px} .lines-p{line-height:2.1}</style>' if K else '') + '</head><body>']
    h.append('<div class="head"><div><div class="theme">Français · Grammaire · G4 · La ponctuation</div>')
    h.append(f'<h1>{"Corrigé et barème &nbsp;<span class=tag>ENSEIGNANT</span>" if K else "Évaluation de grammaire"}</h1>')
    h.append('<div style="margin-top:6px;font-size:10.5pt">Réponses attendues en <b class="ans">rouge</b>. Le barème est indiqué à droite de chaque titre (total : 20 points).</div>' if K else '<div class="ident"><span>Prénom :</span><span>Date :</span></div>')
    h.append('</div><div class="note"><small>Note</small><b>' + ('<em>20</em>' if K else '&nbsp;&nbsp;&nbsp;') + ' / 20</b></div></div>')
    comps = [("Je connais le nom des signes de ponctuation.", "1", "2"),
             ("Je connais le rôle de chaque signe de ponctuation.", "2 · 4", "4,5"),
             ("Je ponctue correctement la fin d’une phrase.", "3 · 9", "5"),
             ("J’utilise la virgule, les deux-points et le point-virgule.", "5 · 6", "4"),
             ("J’applique la règle des majuscules après la ponctuation.", "7", "2"),
             ("Je ponctue un dialogue.", "8", "2,5")]
    if not K:
        h.append('<table class="comp"><tr><th style="text-align:left">Compétences évaluées</th><th>Exercices</th><th class="c">Acquis</th><th class="c">En cours</th><th class="c">Non acquis</th></tr>'
                 + "".join(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td class="c"></td><td class="c"></td><td class="c"></td></tr>' for c, e, _ in comps) + '</table>')

    # 1 Noms
    h.append('<section class="ex"><h2><span class="n">1</span>Le nom des signes<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Écris le nom de chaque signe de ponctuation.' + pts(K, "0,25 point par nom") + '</p>')
    sg = [(";", "le point-virgule"), ("?", "le point d’interrogation"), ("« »", "les guillemets"), ("…", "les points de suspension"),
          (":", "les deux-points"), ("!", "le point d’exclamation"), (",", "la virgule"), (".", "le point")]
    t = '<table class="grid">'
    for i in range(0, 8, 2):
        t += '<tr>' + "".join(f'<td class="sg">{sg[j][0]}</td><td class="{"ans" if K else ""}" style="width:40%;{"color:#c0392b;font-weight:700" if K else ""}">{sg[j][1] if K else ""}</td>' for j in (i, i + 1)) + '</tr>'
    h.append(t + '</table></section>')

    # 2 Rôle
    h.append('<section class="ex"><h2><span class="n">2</span>À quoi sert-il ?<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Écris dans la case le signe qui correspond à chaque rôle. Utilise les signes de la liste.' + pts(K, "0,5 point par signe") + '</p>')
    h.append(BANK(["( )", ";", "—", ".", ":", "…"]))
    roles = [("Il marque la fin d’une phrase déclarative (une information).", "."),
             ("Ils servent à introduire une explication ou une énumération.", ":"),
             ("On les utilise pour donner une précision.", "( )"),
             ("Dans un dialogue, il marque le changement de personnage.", "—"),
             ("Ils indiquent une suite possible.", "…"),
             ("Entre le point et la virgule, il marque une pause plus longue.", ";")]
    h.append('<table class="grid">' + "".join(f'<tr><td>{r}</td><td class="c">{SQ(s_, K)}</td></tr>' for r, s_ in roles) + '</table></section>')

    # 3 Fin de phrase
    h.append('<section class="ex"><h2><span class="n">3</span>La ponctuation en fin de phrase<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Termine chaque phrase par un point <span class="sign">.</span>, un point d’interrogation <span class="sign">?</span> ou un point d’exclamation <span class="sign">!</span>' + pts(K, "0,5 point par phrase") + '</p>')
    fins = [("Quelle heure est-il", "?"), ("Le chat dort sur le canapé", "."), ("Quel magnifique coucher de soleil", "!"),
            ("Est-ce que tu viens à la piscine jeudi", "?"), ("Attention, la route est glissante", "!"), ("Nous partons en vacances demain", ".")]
    h.append('<div class="cols2" style="display:grid;grid-template-columns:1fr 1fr;gap:8px 22px">' + "".join(f'<div>{"abcdef"[i]}) {p} {SQ(s_, K)}</div>' for i, (p, s_) in enumerate(fins)) + '</div>')
    if K: h.append('<p class="bareme">Pour « Attention, la route est glissante », accepter aussi le point. Pour « Nous partons en vacances demain », accepter aussi le point d’exclamation si l’élève l’explique comme une joie.</p>')
    h.append('</section>')

    # 4 Intonation
    h.append('<section class="ex"><h2><span class="n">4</span>La voix et la ponctuation<span class="pts">… / 1,5</span></h2>')
    h.append('<p class="consigne">Quand je lis la phrase à voix haute, mon intonation est… Coche la bonne réponse.' + pts(K, "0,5 point par ligne") + '</p>')
    into = [("une phrase qui se termine par un point <b>.</b>", False), ("une phrase qui se termine par un point d’interrogation <b>?</b>", True), ("une phrase qui se termine par un point d’exclamation <b>!</b>", True)]
    h.append('<table class="grid"><tr><th style="text-align:left">Pour…</th><th class="c">montante</th><th class="c">descendante</th></tr>' +
             "".join(f'<tr><td>{p}</td><td class="c">{box(K, up)}</td><td class="c">{box(K, not up)}</td></tr>' for p, up in into) + '</table></section>')

    # 5 Virgules
    h.append('<section class="ex"><h2><span class="n">5</span>La virgule<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Ces phrases contiennent une énumération. Ajoute les 2 virgules qui manquent dans chaque phrase.' + pts(K, "0,5 point par virgule bien placée") + '</p>')
    h.append(f'<p class="lines-p">a) Dans ma trousse, j’ai un stylo{SQ(",", K)} une gomme{SQ(",", K)} une règle et des ciseaux.<br>'
             f'b) Au marché, maman achète des pommes{SQ(",", K)} des poires{SQ(",", K)} des carottes et du pain.</p>')
    if K: h.append('<p class="bareme">Pas de virgule avant « et ».</p>')
    h.append('</section>')

    # 6 : ou ;
    h.append('<section class="ex"><h2><span class="n">6</span>Deux-points ou point-virgule ?<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Écris les deux-points <span class="sign">:</span> ou le point-virgule <span class="sign">;</span> dans la case.' + pts(K, "0,5 point par case") + '</p>')
    dp = [("Léa ne pourra pas venir", ":", "il est malade.", "explication"), ("J’ai invité trois amis", ":", "Tom, Inès et Hugo.", "énumération"),
          ("Le soleil se couche", ";", "les oiseaux se taisent.", "pause plus longue"), ("Le maître annonce", ":", "« Sortez vos cahiers ! »", "dialogue à venir")]
    h.append('<ol class="alpha">' + "".join(f'<li><span>{"abcd"[i]})</span><span>{a} {SQ(s_, K)} {b}{f" <span class=bareme>({why})</span>" if K else ""}</span></li>' for i, (a, s_, b, why) in enumerate(dp)) + '</ol>')
    h.append('</section>')

    # 7 Majuscules
    h.append('<section class="ex"><h2><span class="n">7</span>Majuscule ou pas ?<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Pour chaque paire, coche la phrase bien écrite.' + pts(K, "0,5 point par paire") + '</p>')
    pairs = [("Elle a tout préparé : les crêpes, le jus et les gâteaux.", "Elle a tout préparé : Les crêpes, le jus et les gâteaux.", 0),
             ("Il hésita… puis il ouvrit la porte.", "Il hésita… Puis il ouvrit la porte.", 1),
             ("Je lis beaucoup ; Ma sœur préfère dessiner.", "Je lis beaucoup ; ma sœur préfère dessiner.", 1),
             ("Le loup approchait… Le petit cochon tremblait.", "Le loup approchait… le petit cochon tremblait.", 0)]
    for i, (a, b, ok) in enumerate(pairs):
        h.append(f'<div style="margin-top:4px"><b>{"abcd"[i]})</b></div><div class="choice2"><span>{box(K, ok == 0)}</span><span>{a}</span><span>{box(K, ok == 1)}</span><span>{b}</span></div>')
    if K: h.append('<p class="bareme">La règle : pas de majuscule après un point-virgule ou des deux-points ; une majuscule après des points de suspension.</p>')
    h.append('</section>')

    # 8 Dialogue
    h.append('<section class="ex"><h2><span class="n">8</span>Ponctuer un dialogue<span class="pts">… / 2,5</span></h2>')
    h.append('<p class="consigne">Complète le dialogue avec les 10 signes de la liste.' + pts(K, "0,25 point par case") + '</p>')
    h.append(BANK([":", "«", "?", "—", ",", ",", ".", "—", "!", "»"]))
    h.append(f'<p class="lines-p">Léo demande à sa maman {SQ(":", K)} {SQ("«", K)} Est-ce qu’on peut aller au parc {SQ("?", K)}<br>'
             f'{SQ("—", K)} Oui{SQ(",", K)} répond maman{SQ(",", K)} mais d’abord, range ta chambre {SQ(".", K)}<br>'
             f'{SQ("—", K)} Super {SQ("!", K)} {SQ("»", K)} s’écrie Léo.</p>')
    if K: h.append('<p class="bareme">Les guillemets ouvrent et ferment tout le dialogue ; le tiret marque le changement de personnage. Pour la réponse de maman, accepter aussi « ! » à la place du point.</p>')
    h.append('</section>')

    # 9 Production
    h.append('<section class="ex"><h2><span class="n">9</span>À toi d’écrire<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Sur le thème de l’école, écris une phrase interrogative, puis une phrase exclamative.' + pts(K, "1 point par phrase : 0,5 point pour une phrase correcte qui commence par une majuscule, 0,5 point pour le bon signe à la fin") + '</p>')
    if K:
        h.append('<div class="answer-box">Réponses personnelles. Exemples : « Est-ce que la récréation commence bientôt ? » · « Quelle belle dictée ! »</div>')
    else:
        h.append('<p style="margin:6px 0 0">Phrase interrogative :</p><div class="lines"><div class="line"></div></div><p style="margin:4px 0 0">Phrase exclamative :</p><div class="lines"><div class="line"></div></div>')
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
