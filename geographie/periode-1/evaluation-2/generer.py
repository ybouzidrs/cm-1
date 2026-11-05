# Usage : python3 generer.py <dossier de sortie> <chemin de sciences/periode-1/evaluation/generer.py (styles communs)>
import sys, os, re
OUT = sys.argv[1]
CSS = re.search(r'CSS = """(.*?)"""', open(sys.argv[2]).read(), re.S).group(1)
CSS += """
table.grid { width: 100%; border-collapse: collapse; }
table.grid td, table.grid th { border: 1.2px solid #555; padding: 6px 8px; }
table.grid th { background: #eee; font-size: 10pt; }
table.grid td.c, table.grid th.c { width: 84px; text-align: center; }
table.grid td.ans { color: #c0392b; font-weight: 700; }
.field { display: flex; gap: 6px; align-items: baseline; margin: 5px 0; }
.field .blank { flex: 1; min-width: 0; }
.cols2 { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 22px; }
svg.lim { max-width: 165mm; }
.order { display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; text-align: center; font-weight: 700; }
.order span { border: 1.5px solid #111; border-radius: 8px; padding: 6px 2px; font-size: 10pt; }
.qcm { display: flex; gap: 18px; flex-wrap: wrap; margin: 4px 0 2px 22px; }
"""
def B(a, K, c=""): return f'<span class="blank filled ans">{a}</span>' if K else f'<span class="blank {c}"></span>'
def pts(K, t): return f' <span class="bareme">({t})</span>' if K else ''
def box(K, on): return f'<span class="box{" x" if (K and on) else ""}"></span>'

def lim_map(K):
    cx, cy = 370, 175
    pos = [("Argenteuil", -170, -125), ("Gennevilliers", 170, -125), ("Asnières-sur-Seine", 260, 0), ("Bois-Colombes", 200, 110),
           ("La Garenne-Colombes", 0, 145), ("Nanterre", -200, 110), ("Bezons", -260, 0)]
    s = ['<svg class="lim" viewBox="0 0 740 360" role="img" aria-label="Colombes et ses villes limitrophes">']
    for i, (n, dx, dy) in enumerate(pos, 1):
        x, y = cx + dx, cy + dy
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#888" stroke-width="1.5" stroke-dasharray="5 5"/>')
    s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="78" ry="42" fill="#e6e6e6" stroke="#111" stroke-width="2.5"/><text x="{cx}" y="{cy+7}" text-anchor="middle" font-size="20" font-weight="700" fill="#111">Colombes</text>')
    for i, (n, dx, dy) in enumerate(pos, 1):
        x, y = cx + dx, cy + dy
        s.append(f'<rect x="{x-85}" y="{y-20}" width="170" height="40" rx="7" fill="#fff" stroke="#111" stroke-width="1.6"/>')
        s.append(f'<circle cx="{x-85}" cy="{y-20}" r="11" fill="#111"/><text x="{x-85}" y="{y-15}" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">{i}</text>')
        if K:
            s.append(f'<text x="{x}" y="{y+6}" text-anchor="middle" font-size="{14 if len(n) > 14 else 16}" font-weight="700" fill="#c0392b">{n}</text>')
    s.append('<g transform="translate(700,40)"><line x1="0" y1="22" x2="0" y2="-8" stroke="#111" stroke-width="2.5"/><polygon points="0,-16 -7,-2 7,-2" fill="#111"/><text x="0" y="40" text-anchor="middle" font-size="14" font-weight="700" fill="#111">N</text></g>')
    s.append('</svg>')
    return "".join(s)

def doc(K):
    h = [f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{"Corrigé · " if K else ""}Évaluation 2 · Les lieux où j’habite</title>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Lilita+One&display=swap">'
         f'<style>{CSS}</style>' + ('<style>body{font-size:10.5pt;line-height:1.38} svg.lim{max-width:110mm} .ex{margin-top:9px} .bank{margin:2px 0 4px;padding:3px 8px} table.grid td,table.grid th,table.vf td{padding:3px 8px} .texte{line-height:1.9}</style>' if K else '') + '</head><body>']
    h.append('<div class="head"><div><div class="theme">Géographie · Thème 1 · Les lieux où j’habite · Évaluation 2</div>')
    h.append(f'<h1>{"Corrigé et barème &nbsp;<span class=tag>ENSEIGNANT</span>" if K else "Évaluation de géographie"}</h1>')
    h.append('<div style="margin-top:6px;font-size:10.5pt">Réponses attendues en <b class="ans">rouge</b>. Le barème est indiqué à droite de chaque titre (total : 20 points).</div>' if K else '<div class="ident"><span>Prénom :</span><span>Date :</span></div>')
    h.append('</div><div class="note"><small>Note</small><b>' + ('<em>20</em>' if K else '&nbsp;&nbsp;&nbsp;') + ' / 20</b></div></div>')
    comps = [("Je connais mon quartier et les quartiers de ma commune.", "1", "2"),
             ("Je connais les communes limitrophes et je sais situer Colombes.", "2", "2,5"),
             ("Je connais les départements d’Île-de-France (nom et numéro), la petite et la grande couronne.", "3", "3"),
             ("Je connais les collectivités, ceux qui les dirigent et leurs missions.", "4 · 8", "3,5"),
             ("Je range les lieux du plus petit au plus grand.", "6", "1,5"),
             ("Je connais ma commune.", "5 · 7", "3,5"),
             ("Je connais mon pays et l’Union européenne.", "9", "2"),
             ("Je connais le vocabulaire et les nombres clés.", "10", "2")]
    if not K:
        h.append('<table class="comp"><tr><th style="text-align:left">Compétences évaluées</th><th>Exercices</th><th class="c">Acquis</th><th class="c">En cours</th><th class="c">Non acquis</th></tr>'
                 + "".join(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td class="c"></td><td class="c"></td><td class="c"></td></tr>' for c, e, _ in comps) + '</table>')

    # 1 Quartiers
    h.append('<section class="ex"><h2><span class="n">1</span>Les quartiers de Colombes<span class="pts">… / 2</span></h2>')
    h.append('<ol class="alpha">'
             f'<li><span>a)</span><span>Colombes est découpée en {B("9", K, "s")} quartiers.{pts(K, "0,5 point")}</span></li>'
             f'<li><span>b)</span><span>Le quartier de mon école s’appelle {B("la Petite-Garenne", K, "l")}.{pts(K, "0,5 point")}</span></li>'
             f'<li><span>c)</span><span>C’est un quartier : {box(K, False)} d’immeubles &nbsp; {box(K, True)} pavillonnaire &nbsp; {box(K, False)} rural{pts(K, "0,5 point")}</span></li>'
             f'<li><span>d)</span><span>Cite deux autres quartiers de Colombes.{pts(K, "0,25 point par quartier")}</span></li></ol>')
    h.append('<div class="answer-box">Deux quartiers parmi : Centre, Europe, Fossés-Jean, Agent-Sarre, Stade-Arc sportif, Vallées, Grèves-Petit-Colombes, Victor-Basch.</div>' if K
             else '<div class="cols2"><div class="line"></div><div class="line"></div></div>')
    h.append('</section>')

    # 2 Limitrophes
    h.append('<section class="ex"><h2><span class="n">2</span>Les villes limitrophes<span class="pts">… / 2,5</span></h2>')
    h.append('<p class="consigne">a) Une ville limitrophe, c’est une ville…' + pts(K, "0,25 point") + '</p>')
    h.append(f'<div class="qcm"><span>{box(K, False)} très loin de Colombes</span><span>{box(K, True)} à la frontière de Colombes</span><span>{box(K, False)} plus grande que Colombes</span></div>')
    h.append('<p class="consigne" style="margin-top:8px">b) Écris le nom des 7 villes limitrophes au bon endroit sur le schéma. Attention, il y a 3 villes en trop dans la liste.' + pts(K, "0,25 point par ville bien placée") + '</p>')
    h.append('<div class="bank">Nanterre · Paris · Bezons · Asnières-sur-Seine · Versailles · Argenteuil · La Garenne-Colombes · Gennevilliers · Saint-Denis · Bois-Colombes</div>')
    h.append(lim_map(K))
    h.append(f'<p class="consigne">c) Colombes est située au {B("nord-ouest", K)} de Paris.{pts(K, "0,5 point")}</p>')
    if K: h.append('<p class="bareme">Les 3 intrus : Paris, Versailles, Saint-Denis. Si l’élève a trouvé les 7 villes mais en a mal placé quelques-unes, on peut compter 0,25 point par ville citée.</p>')
    h.append('</section>')

    # 3 IDF
    h.append('<section class="ex"><h2><span class="n">3</span>Les départements d’Île-de-France<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Complète le tableau : écris le numéro ou le nom qui manque, puis coche la bonne couronne.' + pts(K, "nom ou numéro : 0,25 point par case ; couronnes : 1 point si tout est juste, 0,5 point pour une ou deux erreurs") + '</p>')
    deps = [("Paris", "75", None, "num"), ("Hauts-de-Seine", "92", "p", "num"), ("Seine-Saint-Denis", "93", "p", "nom"), ("Val-de-Marne", "94", "p", "num"),
            ("Seine-et-Marne", "77", "g", "nom"), ("Yvelines", "78", "g", "num"), ("Essonne", "91", "g", "nom"), ("Val-d’Oise", "95", "g", "nom")]
    t = '<table class="grid"><tr><th style="text-align:left">Nom du département</th><th class="c">Numéro</th><th class="c">Petite couronne</th><th class="c">Grande couronne</th></tr>'
    for nom, num, cr, hole in deps:
        cn = (f'<td class="ans">{nom}</td>' if K else '<td style="height:28px"></td>') if hole == "nom" else f'<td>{nom}</td>'
        cnum = (f'<td class="c ans">{num}</td>' if K else '<td class="c"></td>') if hole == "num" else f'<td class="c">{num}</td>'
        if cr is None:
            ccr = '<td class="c" colspan="2" style="font-size:9.5pt;color:#555">au centre de la région</td>'
        else:
            ccr = f'<td class="c">{box(K, cr == "p")}</td><td class="c">{box(K, cr == "g")}</td>'
        t += f'<tr>{cn}{cnum}{ccr}</tr>'
    h.append(t + '</table>')
    if K: h.append('<p class="bareme">Total : 8 noms ou numéros (2 points) + les couronnes (1 point) = 3 points. Petite couronne : les 3 départements qui touchent Paris (92, 93, 94).</p>')
    h.append('</section>')

    # 4 Qui suis-je
    h.append('<section class="ex"><h2><span class="n">4</span>Qui suis-je ?<span class="pts">… / 1,5</span></h2>')
    h.append('<p class="consigne">Écris la réponse.' + pts(K, "0,25 point par réponse") + '</p>')
    h.append('<div class="bank">une commune · un village · un département · une région · un quartier · l’Union européenne</div><ol class="alpha">')
    for l, d, a in [("a)", "Je suis dirigée par le maire et le conseil municipal.", "une commune"),
                    ("b)", "J’ai moins de 2 000 habitants.", "un village"),
                    ("c)", "Je suis dirigé par le Conseil départemental, sous l’autorité du préfet.", "un département"),
                    ("d)", "Je suis dirigée par le Conseil régional.", "une région"),
                    ("e)", "Je suis une partie de la commune avec des caractères communs.", "un quartier"),
                    ("f)", "Je regroupe 27 pays membres.", "l’Union européenne")]:
        h.append(f'<li><span>{l}</span><span class="def"><span>{d}</span>{B(a, K)}</span></li>')
    h.append('</ol></section>')

    # 5 Vrai faux
    h.append('<section class="ex"><h2><span class="n">5</span>Vrai ou faux ?<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Coche la bonne case.' + pts(K, "0,5 point par ligne") + '</p>')
    vf = [("Colombes compte environ 91 000 habitants.", True, "91 053 habitants."),
          ("Colombes est un village.", False, "C’est une ville : elle a plus de 2 000 habitants."),
          ("La commune de Colombes s’étend sur 78 km².", False, "Elle s’étend sur 7,81 km²."),
          ("Le maire de Colombes s’appelle Joakim Giacomoni.", True, "")]
    h.append('<table class="vf"><tr><th style="text-align:left">Affirmation</th><th class="c">Vrai</th><th class="c">Faux</th></tr>')
    for s_, v, why in vf:
        h.append(f'<tr><td>{s_}{f"<br><span class=bareme>{why}</span>" if (K and why) else ""}</td><td class="c">{box(K, v)}</td><td class="c">{box(K, not v)}</td></tr>')
    h.append('</table></section>')

    # 6 Ordre
    h.append('<section class="ex"><h2><span class="n">6</span>Du plus petit au plus grand<span class="pts">… / 1,5</span></h2>')
    h.append('<p class="consigne">Numérote de 1 (le plus petit) à 6 (le plus grand).' + pts(K, "1,5 point si tout est juste ; 0,75 point pour une seule erreur") + '</p>')
    items = [("la France", 5), ("Colombes", 2), ("l’Europe", 6), ("la Petite-Garenne", 1), ("l’Île-de-France", 4), ("les Hauts-de-Seine", 3)]
    h.append('<div class="order">' + "".join(f'<span>{n}<br><b class="{"ans" if K else ""}" style="font-size:13pt">{r if K else "…"}</b></span>' for n, r in items) + '</div>')
    h.append('</section>')

    # 7 Ma commune
    h.append('<section class="ex"><h2><span class="n">7</span>Ma commune : Colombes<span class="pts">… / 1,5</span></h2>')
    h.append('<p class="consigne">Complète.' + pts(K, "0,25 point par réponse") + '</p><div class="cols2">')
    for a, b, c in [("Code postal", "92700", "s"), ("Chef-lieu du département", "Nanterre", ""), ("Nom des habitants", "les Colombiens et les Colombiennes", ""),
                    ("Type de paysage", "urbain", ""), ("Types d’habitations", "des pavillons et des immeubles", ""), ("Petite, moyenne ou grande ville ?", "moyenne", "")]:
        h.append(f'<div class="field"><span>{a} :</span>{B(b, K, c)}</div>')
    h.append('</div></section>')

    # 8 Missions
    h.append('<section class="ex"><h2><span class="n">8</span>Qui s’en occupe ?<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Coche la collectivité qui s’occupe de chaque mission.' + pts(K, "0,25 point par ligne") + '</p>')
    miss = [("L’école primaire", 0), ("Les collèges", 1), ("Les lycées", 2), ("L’état civil (naissances, mariages)", 0),
            ("Les routes et les transports du département", 1), ("Les transports régionaux", 2), ("La collecte des déchets", 0), ("L’action sociale et la santé", 1)]
    h.append('<table class="grid"><tr><th style="text-align:left">Mission</th><th class="c">Commune</th><th class="c">Département</th><th class="c">Région</th></tr>'
             + "".join(f'<tr><td>{m}</td>' + "".join(f'<td class="c">{box(K, j == k)}</td>' for j in range(3)) + '</tr>' for m, k in miss) + '</table>')
    h.append('</section>')

    # 9 France et Europe
    h.append('<section class="ex"><h2><span class="n">9</span>Mon pays et l’Europe<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Complète le texte avec les mots de la liste.' + pts(K, "0,25 point par mot") + '</p>')
    h.append('<div class="bank">Égalité · président · Métropole · démocratie · République · l’Union européenne · 27 · Outre-Mer</div>')
    h.append('<p class="texte">La France est constituée d’une ' + B("Métropole", K) + ' et de départements, régions et collectivités situés en ' + B("Outre-Mer", K) +
             '. Sa devise est : Liberté, ' + B("Égalité", K) + ', Fraternité. Notre pays est une ' + B("République", K) + ' dirigée par un ' + B("président", K) +
             ' élu par le peuple : c’est une ' + B("démocratie", K) + ', les citoyens participent par le vote. Certains pays d’Europe se sont regroupés pour former ' +
             B("l’Union européenne", K) + ', avec ' + B("27", K, "s") + ' pays membres.</p>')
    h.append('</section>')

    # 10 Vocabulaire et nombres
    h.append('<section class="ex"><h2><span class="n">10</span>Le vocabulaire et les nombres clés<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Complète.' + pts(K, "0,25 point par case") + '</p><ol class="alpha">'
             f'<li><span>a)</span><span>En France, une ville est une commune d’au moins {B("2 000", K, "s")} habitants. S’il y en a moins, on parle de {B("village", K)}.</span></li>'
             f'<li><span>b)</span><span>Une commune est un territoire dirigé par un {B("maire", K)} et un {B("conseil municipal", K)}, élus pour {B("6", K, "s")} ans.</span></li>'
             f'<li><span>c)</span><span>En France, il y a environ {B("36 000", K, "s")} communes, {B("101", K, "s")} départements et {B("18", K, "s")} régions.</span></li></ol>')
    if K: h.append('<p class="bareme">Le cahier donne 36 000 communes : accepter aussi 35 000 (le chiffre actuel est d’environ 34 900).</p>')
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
