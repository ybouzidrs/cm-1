import sys, os, re
OUT = sys.argv[1]
src = open(sys.argv[2]).read()
CSS = re.search(r'CSS = """(.*?)"""', src, re.S).group(1)
CSS += """
table.grid { width: 100%; border-collapse: collapse; }
table.grid td, table.grid th { border: 1.2px solid #555; padding: 5px 8px; }
table.grid th { background: #eee; }
table.grid td.c, table.grid th.c { width: 92px; text-align: center; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 18px; }
.field { display: flex; gap: 6px; align-items: baseline; }
.field .blank { flex: 1; min-width: 0; }
.field .blank.filled { flex: 1; }
.rose-row { display: grid; grid-template-columns: 52mm 1fr; gap: 14px; align-items: center; }
svg.nest { max-width: 175mm; }
svg.rose { max-width: 50mm; }
"""

def B(ans, key, cls=""):
    return f'<span class="blank filled ans">{ans}</span>' if key else f'<span class="blank {cls}"></span>'

def nest(key):
    levels = [("un continent", "l’Europe"), ("un pays", "la France"), ("une région", "l’Île-de-France"),
              ("un département", "les Hauts-de-Seine"), ("une commune", "Colombes"), ("un quartier", "la Petite-Garenne")]
    fills = ["#f2f2f2", "#ffffff", "#f2f2f2", "#ffffff", "#f2f2f2", "#ffffff"]
    s = ['<svg class="nest" viewBox="0 0 640 380" role="img" aria-label="Les échelles emboîtées">']
    for i, (sc, ex) in enumerate(levels):
        x = 10 + i * 16; y = 10 + i * 56; w = 620 - i * 32; h = 360 - i * 56 - i * 6
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fills[i]}" stroke="#111" stroke-width="1.8"/>')
        ty = y + 33
        s.append(f'<text x="{x+12}" y="{ty}" font-size="14" fill="#444">Échelle :</text>')
        s.append(f'<text x="{x+222}" y="{ty}" font-size="14" fill="#444">Chez moi :</text>')
        if key:
            s.append(f'<text x="{x+82}" y="{ty}" font-size="16" font-weight="700" fill="#c0392b">{sc}</text>')
            s.append(f'<text x="{x+296}" y="{ty}" font-size="16" font-weight="700" fill="#c0392b">{ex}</text>')
        else:
            s.append(f'<line x1="{x+82}" y1="{ty+3}" x2="{x+210}" y2="{ty+3}" stroke="#222" stroke-width="1.4" stroke-dasharray="2 3"/>')
            s.append(f'<line x1="{x+296}" y1="{ty+3}" x2="{x+w-14}" y2="{ty+3}" stroke="#222" stroke-width="1.4" stroke-dasharray="2 3"/>')
    s.append('</svg>')
    return "".join(s)

def rose(key):
    c = 100
    s = ['<svg class="rose" viewBox="0 0 200 200" role="img" aria-label="Rose des vents">',
         f'<circle cx="{c}" cy="{c}" r="62" fill="none" stroke="#111" stroke-width="2"/>',
         f'<polygon points="100,38 110,90 162,100 110,110 100,162 90,110 38,100 90,90" fill="#555" stroke="#111" stroke-width="1.5"/>',
         f'<polygon points="100,100 140,60 106,96" fill="#fff" stroke="#111"/><polygon points="100,100 140,140 104,106" fill="#fff" stroke="#111"/>',
         f'<polygon points="100,100 60,140 94,104" fill="#fff" stroke="#111"/><polygon points="100,100 60,60 96,94" fill="#fff" stroke="#111"/>']
    for t, x, y in [("NE", 150, 52), ("NO", 50, 52), ("SE", 150, 156), ("SO", 50, 156)]:
        s.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-size="13" font-weight="700" fill="#111">{t}</text>')
    for t, x, y in [("N", 100, 22), ("S", 100, 192), ("E", 184, 106), ("O", 16, 106)]:
        s.append(f'<rect x="{x-14}" y="{y-17}" width="28" height="24" rx="4" fill="#fff" stroke="#111" stroke-width="1.5"/>')
        if key:
            s.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-size="16" font-weight="700" fill="#c0392b">{t}</text>')
    s.append('</svg>')
    return "".join(s)

def pts(K, txt):
    return f' <span class="bareme">({txt})</span>' if K else ''

def doc(K):
    title = "Corrigé et barème" if K else "Évaluation de géographie"
    h = [f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
         f'<title>{"Corrigé · " if K else ""}Évaluation · Les lieux où j’habite</title>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Lilita+One&display=swap">'
         f'<style>{CSS}</style></head><body>']
    h.append('<div class="head"><div><div class="theme">Géographie · Thème 1 · Les lieux où j’habite</div>')
    h.append(f'<h1>{title}{" &nbsp;<span class=tag>ENSEIGNANT</span>" if K else ""}</h1>')
    if K:
        h.append('<div style="margin-top:6px;font-size:10.5pt">Réponses attendues en <b class="ans">rouge</b>. Le barème de chaque exercice est indiqué à droite du titre (total : 20 points).</div>')
    else:
        h.append('<div class="ident"><span>Prénom :</span><span>Date :</span></div>')
    h.append('</div><div class="note"><small>Note</small><b>' + ('<em>20</em>' if K else '&nbsp;&nbsp;&nbsp;') + ' / 20</b></div></div>')
    comps = [("Je connais les différentes échelles des lieux où j’habite.", "1", "3"),
             ("Je connais qui dirige les collectivités et leurs missions.", "2 · 3", "5"),
             ("Je connais les nombres clés.", "4", "3"),
             ("Je connais ma commune et je sais la situer.", "5 · 6 · 7", "7"),
             ("Je connais mon pays.", "8", "2")]
    if not K:
        h.append('<table class="comp"><tr><th style="text-align:left">Compétences évaluées</th><th>Exercices</th><th class="c">Acquis</th><th class="c">En cours</th><th class="c">Non acquis</th></tr>')
        for c, e, _ in comps:
            h.append(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td class="c"></td><td class="c"></td><td class="c"></td></tr>')
        h.append('</table>')

    # 1
    h.append('<section class="ex"><h2><span class="n">1</span>Du plus grand au plus petit<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Écris les échelles, de la plus grande (à l’extérieur) à la plus petite (au centre). Puis écris le nom du lieu où tu habites pour chaque échelle.' + pts(K, "0,25 point par case") + '</p>')
    h.append('<div class="bank">une commune · un pays · un quartier · une&nbsp;région · un&nbsp;continent · un&nbsp;département</div>')
    h.append(nest(K) + '</section>')

    # 2
    h.append('<section class="ex"><h2><span class="n">2</span>Qui dirige ?<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Relie chaque lieu à ceux qui le dirigent.' + pts(K, "0,5 point par liaison juste") + '</p>')
    left = ["La commune", "Le département", "La région", "Le pays (la France)"]
    right = ["le Conseil régional", "le président de la République", "le maire et le conseil municipal", "le Conseil départemental"]
    sol = {0: 2, 1: 3, 2: 0, 3: 1}
    if K:
        h.append('<ol class="alpha">' + "".join(f'<li><span>•</span><span>{left[i]} → <span class="ans">{right[sol[i]]}</span></span></li>' for i in range(4)) + '</ol>')
        h.append('<p class="bareme">Rappel du cahier : le maire et le conseil municipal sont élus par les habitants pour 6 ans ; le département est dirigé par le Conseil départemental sous l’autorité du préfet.</p>')
    else:
        h.append('<div class="relie">' + "".join(f'<span>{left[i]}</span><span class="dot">•</span><span></span><span class="dot">•</span><span>{right[i]}</span>' for i in range(4)) + '</div>')
    h.append('</section>')

    # 3
    h.append('<section class="ex"><h2><span class="n">3</span>Qui s’en occupe ?<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Coche la collectivité qui s’occupe de chaque mission.' + pts(K, "0,5 point par ligne") + '</p>')
    missions = [("L’école primaire", 0), ("Les lycées", 2), ("Les collèges", 1), ("La collecte des déchets", 0),
                ("Les ports et les aéroports", 2), ("L’action sociale et la santé", 1)]
    h.append('<table class="grid"><tr><th style="text-align:left">Mission</th><th class="c">Commune</th><th class="c">Département</th><th class="c">Région</th></tr>')
    for m, k in missions:
        cells = "".join(f'<td class="c"><span class="box{" x" if (K and j == k) else ""}"></span></td>' for j in range(3))
        h.append(f'<tr><td>{m}</td>{cells}</tr>')
    h.append('</table></section>')

    # 4
    h.append('<section class="ex"><h2><span class="n">4</span>Les nombres à retenir<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Complète avec le bon nombre.' + pts(K, "0,5 point par nombre") + '</p>')
    h.append('<div class="bank">8 · 18 · 27 · 50 · 101 · 36 000</div>')
    h.append('<ol class="alpha">'
             f'<li><span>•</span><span>Il y a environ {B("36 000", K, "s")} communes en France.</span></li>'
             f'<li><span>•</span><span>Il y a {B("101", K, "s")} départements en France, dont certains en Outre-Mer.</span></li>'
             f'<li><span>•</span><span>Il y a {B("18", K, "s")} régions en France, dont certaines en Outre-Mer.</span></li>'
             f'<li><span>•</span><span>La région Île-de-France compte {B("8", K, "s")} départements.</span></li>'
             f'<li><span>•</span><span>Le continent européen est constitué de {B("50", K, "s")} pays.</span></li>'
             f'<li><span>•</span><span>L’Union européenne compte {B("27", K, "s")} pays membres.</span></li></ol>')
    h.append('</section>')

    # 5
    h.append('<section class="ex"><h2><span class="n">5</span>La carte d’identité de Colombes<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Complète la carte d’identité de ta ville.' + pts(K, "0,5 point par ligne") + '</p>')
    rows = [("Département", "les Hauts-de-Seine"), ("Numéro du département", "92"), ("Région", "l’Île-de-France"),
            ("Chef-lieu du département", "Nanterre"), ("Nom des habitants", "les Colombiens et les Colombiennes"),
            ("Type de paysage (rural ou urbain ?)", "urbain")]
    h.append('<div style="display:grid;gap:8px">' + "".join(f'<div class="field"><span>{a} :</span>{B(b, K)}</div>' for a, b in rows) + '</div>')
    if K:
        h.append('<p class="bareme">Accepter « 92 » ou « Hauts-de-Seine (92) » pour le département. Attention : le nom des habitants ne va pas dans « type d’habitations » (pavillons et immeubles).</p>')
    h.append('</section>')

    # 6
    h.append('<section class="ex"><h2><span class="n">6</span>Un peu de vocabulaire<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Complète les phrases.' + pts(K, "0,5 point par mot") + '</p>')
    h.append('<p class="texte">En France, une ville est une commune d’au moins ' + B("2000", K, "s") + ' habitants. Lorsqu’il y en a moins, on parle de ' + B("village", K) +
             '. Un quartier est une partie de la ' + B("commune", K) + ' qui présente un ensemble de caractères communs. Une ville limitrophe est une ville qui est à la ' + B("frontière", K) + ' de ma commune.</p>')
    if K:
        h.append('<p class="bareme">Accepter « une ville voisine qui touche Colombes » pour « à la frontière ».</p>')
    h.append('</section>')

    # 7
    h.append('<section class="ex"><h2><span class="n">7</span>Situer Colombes<span class="pts">… / 2</span></h2>')
    h.append('<div class="rose-row"><div>' + rose(K) + '</div><div style="display:flex;flex-direction:column;gap:10px">')
    h.append('<p><b>a)</b> Complète la rose des vents avec N, S, E et O.' + pts(K, "0,25 point par lettre") + '</p>')
    h.append('<p><b>b)</b> Colombes est située au ' + B("nord-ouest", K, "l") + ' de Paris.' + pts(K, "0,5 point") + '</p>')
    h.append('<p><b>c)</b> Cite deux villes limitrophes de Colombes.' + pts(K, "0,25 point par ville") + '</p>')
    if K:
        h.append('<div class="answer-box">Deux villes parmi : La Garenne-Colombes, Bois-Colombes, Argenteuil, Gennevilliers, Asnières-sur-Seine, Bezons, Nanterre.</div>')
    else:
        h.append('<div class="two"><div class="line"></div><div class="line"></div></div>')
    h.append('</div></div></section>')

    # 8
    h.append('<section class="ex"><h2><span class="n">8</span>Mon pays : la France<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Complète les phrases.' + pts(K, "0,5 point par case ; la devise compte pour 1 point") + '</p>')
    h.append('<ol class="alpha">'
             f'<li><span>•</span><span>La France est constituée d’une {B("Métropole", K)} et de départements, régions et collectivités d’Outre-Mer.</span></li>'
             f'<li><span>•</span><span>La devise de la France : {B("Liberté", K, "s")}, {B("Égalité", K, "s")}, {B("Fraternité", K, "s")}.</span></li>'
             f'<li><span>•</span><span>Notre pays est une République dirigée par un président élu par le peuple : c’est une {B("démocratie", K)}. Les citoyens participent par le vote.</span></li></ol>')
    h.append('</section>')

    if K:
        h.append('<section class="ex"><h2><span class="n">✓</span>Récapitulatif du barème<span class="pts">20</span></h2>'
                 '<table class="comp" style="font-size:9pt;margin-top:4px"><tr><th style="text-align:left">Compétence</th><th>Exercices</th><th>Points</th></tr>' +
                 "".join(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td style="text-align:center">{p}</td></tr>' for c, e, p in comps) +
                 '</table><p class="bareme" style="margin-top:6px">Repère possible : compétence acquise si au moins 75 % des points, en cours entre 40 % et 75 %, non acquise en dessous.</p></section>')
    else:
        h.append('<p class="foot">Relis bien tes réponses avant de rendre ta copie. Bon courage !</p>')
    h.append('</body></html>')
    return "".join(h)

open(os.path.join(OUT, "evaluation-sujet.html"), "w").write(doc(False))
open(os.path.join(OUT, "evaluation-corrige.html"), "w").write(doc(True))
