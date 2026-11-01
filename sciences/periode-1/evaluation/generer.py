import sys, os
OUT = sys.argv[1]

CSS = """
@page { size: A4; margin: 14mm 14mm 14mm 14mm; }
* { box-sizing: border-box; }
html, body { margin: 0; background: #fff; color: #111; }
body { font-family: "Andika", "Verdana", sans-serif; font-size: 11.5pt; line-height: 1.45; }
h1, h2, .disp { font-family: "Lilita One", "Arial Rounded MT Bold", sans-serif; font-weight: 400; letter-spacing: .01em; }
.head { display: grid; grid-template-columns: 1fr auto; gap: 10px 16px; align-items: stretch; border: 2px solid #111; border-radius: 10px; padding: 10px 14px; }
.head h1 { font-size: 20pt; margin: 0; line-height: 1.1; }
.head .theme { font-size: 11pt; color: #444; text-transform: uppercase; letter-spacing: .1em; font-weight: 700; }
.ident { display: flex; gap: 18px; margin-top: 8px; }
.ident span { flex: 1; border-bottom: 1.5px dotted #333; padding-bottom: 2px; }
.note { border: 2px solid #111; border-radius: 10px; width: 92px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.note small { font-size: 9pt; text-transform: uppercase; letter-spacing: .08em; }
.note b { font-family: "Lilita One", sans-serif; font-weight: 400; font-size: 20pt; }
.note b em { font-style: normal; color: #c0392b; }
table.comp { width: 100%; border-collapse: collapse; margin: 10px 0 4px; font-size: 10pt; }
table.comp th, table.comp td { border: 1.2px solid #555; padding: 4px 6px; }
table.comp th { background: #eee; font-weight: 700; }
table.comp td.c { width: 62px; text-align: center; }
.ex { break-inside: avoid; margin-top: 14px; }
.ex h2 { font-size: 13.5pt; margin: 0 0 6px; display: flex; align-items: baseline; gap: 10px; border-bottom: 2px solid #111; padding-bottom: 3px; }
.ex h2 .n { display: inline-grid; place-items: center; width: 24px; height: 24px; border-radius: 50%; background: #111; color: #fff; font-size: 12pt; }
.ex h2 .pts { margin-left: auto; font-family: "Andika", sans-serif; font-size: 10pt; font-weight: 700; border: 1.2px solid #111; border-radius: 6px; padding: 0 6px; }
.consigne { font-weight: 700; margin: 0 0 6px; }
.blank { display: inline-block; min-width: 110px; border-bottom: 1.5px dotted #222; height: 1.15em; vertical-align: baseline; }
.blank.s { min-width: 55px; }
.blank.l { min-width: 170px; }
.ans { color: #c0392b; font-weight: 700; }
.blank.filled { min-width: 0; border-bottom: 1.5px solid #c0392b; height: auto; padding: 0 4px; }
.line { border-bottom: 1.5px dotted #222; height: 26px; }
.lines { margin: 2px 0 8px; }
.answer-box { color: #c0392b; font-weight: 700; border-left: 3px solid #c0392b; padding: 2px 10px; margin: 4px 0 8px; }
.bareme { font-size: 9.5pt; color: #555; font-weight: 400; }
ol.alpha { list-style: none; padding: 0; margin: 0; display: grid; gap: 7px; }
ol.alpha li { display: grid; grid-template-columns: 22px 1fr; gap: 4px; }
.def { display: grid; grid-template-columns: 1fr 190px; gap: 10px; align-items: end; }
.def .blank { width: 100%; min-width: 0; }
.relie { display: grid; grid-template-columns: 1fr 40px 60px 40px 1fr; row-gap: 12px; align-items: center; }
.relie .dot { text-align: center; font-size: 16pt; line-height: 1; }
.bank { border: 1.5px dashed #555; border-radius: 8px; padding: 5px 10px; margin: 4px 0 8px; font-weight: 700; text-align: center; word-spacing: 4px; }
.texte { line-height: 2.2; margin: 0; }
table.vf { width: 100%; border-collapse: collapse; }
table.vf td, table.vf th { border: 1.2px solid #555; padding: 5px 8px; }
table.vf th { background: #eee; }
table.vf td.c, table.vf th.c { width: 54px; text-align: center; }
.box { display: inline-block; width: 15px; height: 15px; border: 1.5px solid #111; border-radius: 3px; vertical-align: middle; }
.box.x { background: #c0392b; border-color: #c0392b; }
svg { display: block; width: 100%; height: auto; margin: 0 auto; }
svg.earth { max-width: 128mm; }
svg.volc { max-width: 165mm; }
svg text { font-family: "Andika", sans-serif; }
.foot { margin-top: 14px; text-align: center; font-size: 9pt; color: #666; }
.tag { display: inline-block; background: #c0392b; color: #fff; font-family: "Lilita One", sans-serif; padding: 2px 10px; border-radius: 6px; font-size: 12pt; letter-spacing: .05em; }
.pagebreak { break-before: page; }
"""

def B(ans, key, cls=""):
    if key:
        return f'<span class="blank filled ans">{ans}</span>'
    return f'<span class="blank {cls}"></span>'

def earth(key):
    labels = [("la croûte terrestre", 50, (268, 70)), ("le manteau", 150, (262, 168)), ("le noyau", 250, (196, 182))]
    s = ['<svg class="earth" viewBox="0 0 540 300" role="img" aria-label="Coupe de la Terre">',
         '<defs><pattern id="dots" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#888"/></pattern>'
         '<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#777" stroke-width="2"/></pattern></defs>',
         '<circle cx="170" cy="150" r="132" fill="#6f6f6f" stroke="#111" stroke-width="2"/>',
         '<circle cx="170" cy="150" r="120" fill="#f3f3f3" stroke="#111" stroke-width="1.5"/>',
         '<circle cx="170" cy="150" r="120" fill="url(#dots)"/>',
         '<circle cx="170" cy="150" r="66" fill="#fff" stroke="#111" stroke-width="1.5"/>',
         '<circle cx="170" cy="150" r="66" fill="url(#hatch)"/>']
    for i, (txt, y, (tx, ty)) in enumerate(labels, 1):
        s.append(f'<line x1="{tx}" y1="{ty}" x2="330" y2="{y}" stroke="#111" stroke-width="1.6"/><circle cx="{tx}" cy="{ty}" r="3.2" fill="#111"/>')
        s.append(f'<text x="338" y="{y+5}" font-size="15" font-weight="700" fill="#111">{i}.</text>')
        if key:
            s.append(f'<text x="360" y="{y+5}" font-size="16" font-weight="700" fill="#c0392b">{txt}</text>')
        else:
            s.append(f'<line x1="358" y1="{y+8}" x2="530" y2="{y+8}" stroke="#222" stroke-width="1.4" stroke-dasharray="2 3"/>')
    s.append('</svg>')
    return "".join(s)

def volcano(key):
    ox = 150
    def P(x, y): return f"{x+ox},{y}"
    s = ['<svg class="volc" viewBox="0 0 700 395" role="img" aria-label="Schéma d’un volcan à légender">',
         '<defs><pattern id="vd" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#777"/></pattern></defs>',
         f'<rect x="{20+ox}" y="232" width="360" height="148" fill="#fafafa" stroke="#111" stroke-width="1.5"/>',
         f'<line x1="{20+ox}" y1="272" x2="{380+ox}" y2="272" stroke="#999" stroke-width="1.2"/>',
         f'<line x1="{20+ox}" y1="312" x2="{380+ox}" y2="312" stroke="#999" stroke-width="1.2"/>',
         f'<path d="M{196+ox} 240 C{170+ox} 262 {120+ox} 280 {70+ox} 300" stroke="#555" stroke-width="7" fill="none" stroke-linecap="round"/>',
         f'<path d="M{204+ox} 250 C{235+ox} 275 {280+ox} 290 {335+ox} 296" stroke="#555" stroke-width="7" fill="none" stroke-linecap="round"/>',
         f'<polygon points="{P(40,234)} {P(168,96)} {P(232,96)} {P(360,234)}" fill="#d6d6d6" stroke="#111" stroke-width="2"/>',
         f'<path d="M{168+ox} 96 Q{200+ox} 116 {232+ox} 96 Z" fill="#888" stroke="#111" stroke-width="1.5"/>',
         f'<path d="M{176+ox} 108 C{160+ox} 140 {130+ox} 175 {92+ox} 214" stroke="#555" stroke-width="8" fill="none" stroke-linecap="round"/>',
         f'<path d="M{224+ox} 108 C{240+ox} 145 {270+ox} 180 {312+ox} 220" stroke="#555" stroke-width="8" fill="none" stroke-linecap="round"/>',
         f'<ellipse cx="{200+ox}" cy="356" rx="96" ry="24" fill="#bdbdbd" stroke="#111" stroke-width="1.5"/>',
         f'<ellipse cx="{200+ox}" cy="356" rx="96" ry="24" fill="url(#vd)"/>',
         f'<polygon points="{P(192,350)} {P(208,350)} {P(205,104)} {P(195,104)}" fill="#bdbdbd" stroke="#111" stroke-width="1.2"/>',
         f'<g fill="#fff" stroke="#111" stroke-width="1.5"><circle cx="{170+ox}" cy="50" r="26"/><circle cx="{238+ox}" cy="54" r="24"/><circle cx="{205+ox}" cy="36" r="30"/><circle cx="{200+ox}" cy="64" r="22"/></g>',
         f'<g fill="#fff" stroke="none"><circle cx="{170+ox}" cy="50" r="24.5"/><circle cx="{238+ox}" cy="54" r="22.5"/><circle cx="{205+ox}" cy="36" r="28.5"/><circle cx="{200+ox}" cy="64" r="20.5"/></g>',
         f'<path d="M{200+ox} 100 L{176+ox} 70 M{200+ox} 100 L{200+ox} 62 M{200+ox} 100 L{226+ox} 72 M{200+ox} 100 L{160+ox} 86 M{200+ox} 100 L{242+ox} 88" stroke="#111" stroke-width="3.5" stroke-linecap="round"/>',
         f'<polygon points="{P(200,82)} {P(206,93)} {P(218,92)} {P(209,100)} {P(214,111)} {P(200,105)} {P(186,111)} {P(191,100)} {P(182,92)} {P(194,93)}" fill="#fff" stroke="#111" stroke-width="2"/>']
    boxes = [
        ("lave", 0, 50, 34, (328, 72)),
        ("anciennes coulées|de lave", 0, 158, 46, (276, 178)),
        ("magma", 0, 336, 34, (270, 356)),
        ("nuage de cendres", 540, 24, 34, (412, 48)),
        ("explosion|volcanique", 540, 78, 46, (352, 96)),
        ("cratère", 540, 140, 34, (374, 100)),
        ("cheminée", 540, 246, 34, (351, 262)),
    ]
    for txt, bx, by, bh, (tx, ty) in boxes:
        cy = by + bh / 2
        ax = bx + 160 if bx == 0 else bx
        s.append(f'<line x1="{ax}" y1="{cy}" x2="{tx}" y2="{ty}" stroke="#111" stroke-width="1.6"/><circle cx="{tx}" cy="{ty}" r="3.2" fill="#111"/>')
        s.append(f'<rect x="{bx+1}" y="{by}" width="158" height="{bh}" rx="7" fill="#fff" stroke="#111" stroke-width="1.6"/>')
        if key:
            parts = txt.split("|")
            for k, p in enumerate(parts):
                yy = cy + 5 + (k - (len(parts) - 1) / 2) * 17
                s.append(f'<text x="{bx+80}" y="{yy}" text-anchor="middle" font-size="15" font-weight="700" fill="#c0392b">{p}</text>')
    s.append('</svg>')
    return "".join(s)

def doc(key):
    K = key
    title = "Corrigé et barème" if K else "Évaluation de sciences"
    h = []
    h.append(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
             f'<title>{"Corrigé · " if K else ""}Évaluation · La Terre et les volcans</title>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Lilita+One&display=swap">'
             f'<style>{CSS}</style>' + ('<style>svg.earth{max-width:100mm} svg.volc{max-width:145mm}</style>' if K else '') + '</head><body>')
    h.append('<div class="head"><div>')
    h.append(f'<div class="theme">Sciences · Thème 1 · La Terre et les volcans</div><h1>{title}{" &nbsp;<span class=tag>ENSEIGNANT</span>" if K else ""}</h1>')
    if not K:
        h.append('<div class="ident"><span>Prénom :</span><span>Date :</span></div>')
    else:
        h.append('<div style="margin-top:6px;font-size:10.5pt">Réponses attendues en <b class="ans">rouge</b>. Le barème de chaque exercice est indiqué dans le cadre à droite du titre (total : 20 points).</div>')
    h.append('</div><div class="note"><small>Note</small><b>' + ('<em>20</em>' if K else '&nbsp;&nbsp;&nbsp;') + ' / 20</b></div></div>')

    if not K:
        h.append('<table class="comp"><tr><th style="text-align:left">Compétences évaluées</th><th>Exercices</th><th class="c">Acquis</th><th class="c">En cours</th><th class="c">Non acquis</th></tr>')
        for c, e in [("Je connais la structure de la Terre.", "1 · 2"),
                     ("Je sais expliquer le mouvement des plaques et ses conséquences.", "3 · 4"),
                     ("Je connais les parties d’un volcan.", "6"),
                     ("Je sais expliquer une éruption volcanique.", "7"),
                     ("Je mobilise mes connaissances.", "5")]:
            h.append(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td class="c"></td><td class="c"></td><td class="c"></td></tr>')
        h.append('</table>')

    # Ex 1
    h.append('<section class="ex"><h2><span class="n">1</span>La structure de la Terre<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">a) Écris le nom des trois couches de la Terre.' + (' <span class="bareme">(0,5 point par couche)</span>' if K else '') + '</p>')
    h.append(earth(K))
    h.append('<p class="consigne">b) Complète avec les bons nombres.' + (' <span class="bareme">(0,5 point par phrase)</span>' if K else '') + '</p>')
    h.append('<ol class="alpha">'
             f'<li><span>•</span><span>La croûte terrestre est épaisse de {B("6", K, "s")} à {B("70", K, "s")} km.</span></li>'
             f'<li><span>•</span><span>Le manteau mesure environ {B("2800", K, "s")} km d’épaisseur.</span></li>'
             f'<li><span>•</span><span>Le rayon de la Terre mesure environ {B("6400", K, "s")} km.</span></li></ol>')
    h.append('</section>')

    # Ex 2
    h.append('<section class="ex"><h2><span class="n">2</span>Qui suis-je ?<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Trouve à quoi correspondent ces définitions.' + (' <span class="bareme">(0,5 point par réponse)</span>' if K else '') + '</p><ol class="alpha">')
    for l, d, a in [("a)", "Il se trouve au centre de la Terre et il est formé surtout de fer.", "le noyau"),
                    ("b)", "C’est la « peau » de la Terre, faite de roches solides.", "la croûte terrestre"),
                    ("c)", "C’est la « chair » de la Terre, faite de roches très chaudes et comprimées.", "le manteau"),
                    ("d)", "Ce sont les roches très chaudes et partiellement fondues qui remontent dans un volcan.", "le magma")]:
        h.append(f'<li><span>{l}</span><span class="def"><span>{d}</span>{B(a, K)}</span></li>')
    h.append('</ol></section>')

    # Ex 3
    h.append('<section class="ex"><h2><span class="n">3</span>Relie<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Relie chaque phrase au mot qui convient.' + (' <span class="bareme">(0,5 point par liaison juste)</span>' if K else '') + '</p>')
    left = ["Elles se déplacent de quelques centimètres par an.", "Chaîne de montagnes au nord de l’Inde.",
            "Chaîne de montagnes en Amérique du Sud.", "Secousses provoquées par le mouvement des plaques."]
    right = ["l’Himalaya", "les tremblements de terre", "les plaques", "la cordillère des Andes"]
    sol = {0: 2, 1: 0, 2: 3, 3: 1}
    if K:
        h.append('<ol class="alpha">')
        for i, t in enumerate(left):
            h.append(f'<li><span>{"abcd"[i]})</span><span>{t} → <span class="ans">{right[sol[i]]}</span></span></li>')
        h.append('</ol>')
    else:
        h.append('<div class="relie">')
        for i in range(4):
            h.append(f'<span>{"abcd"[i]}) {left[i]}</span><span class="dot">•</span><span></span><span class="dot">•</span><span>{right[i]}</span>')
        h.append('</div>')
    h.append('</section>')

    # Ex 4
    h.append('<section class="ex"><h2><span class="n">4</span>Des plaques qui bougent<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Réponds aux questions par une phrase.' + (' <span class="bareme">(1 point par réponse)</span>' if K else '') + '</p>')
    qs = [("a) De quoi est constituée la croûte terrestre ?",
           "Elle est constituée de grandes plaques qui « flottent » sur le manteau.",
           "Accepter « de plaques tectoniques ». Mot-clé attendu : plaques."),
          ("b) Que se passe-t-il quand deux plaques se rencontrent et que l’une passe sous l’autre ?",
           "Le bord de la plaque du dessus est soulevé, fissuré et plissé : des montagnes se forment.",
           "Mot-clé attendu : montagnes. Accepter « des montagnes ou des volcans se forment »."),
          ("c) Que provoquent les mouvements des plaques vers leurs bords ?",
           "Ils provoquent des secousses (des tremblements de terre) et des fissures de la croûte terrestre, à l’origine du volcanisme.",
           "0,5 point pour « secousses / tremblements de terre », 0,5 point pour « fissures / volcanisme».")]
    for q, a, note in qs:
        h.append(f'<p style="margin:6px 0 2px">{q}</p>')
        if K:
            h.append(f'<div class="answer-box">{a}<br><span class="bareme">{note}</span></div>')
        else:
            h.append('<div class="lines"><div class="line"></div><div class="line"></div></div>')
    h.append('</section>')


    # Ex 7
    h.append('<section class="ex"><h2><span class="n">5</span>Vrai ou faux ?<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Coche la bonne case.' + (' <span class="bareme">(0,5 point par ligne)</span>' if K else '') + '</p>')
    vf = [("La croûte terrestre est très épaisse par rapport au rayon de la Terre.", False, "Elle est très mince : 6 à 70 km pour un rayon de 6400 km."),
          ("Le noyau est formé surtout de fer.", True, ""),
          ("Les plaques de la croûte terrestre ne bougent jamais.", False, "Elles bougent de quelques centimètres par an."),
          ("Beaucoup de volcans sont situés à la limite des grandes plaques.", True, ""),
          ("Quand le magma arrive à la surface, on l’appelle la lave.", True, ""),
          ("La lave reste liquide quand elle refroidit.", False, "En refroidissant, elle devient de la roche solide.")]
    h.append('<table class="vf"><tr><th style="text-align:left">Affirmation</th><th class="c">Vrai</th><th class="c">Faux</th></tr>')
    for t, v, why in vf:
        extra = f'<br><span class="bareme">{why}</span>' if (K and why) else ''
        bv = '<span class="box x"></span>' if (K and v) else '<span class="box"></span>'
        bf = '<span class="box x"></span>' if (K and not v) else '<span class="box"></span>'
        h.append(f'<tr><td>{t}{extra}</td><td class="c">{bv}</td><td class="c">{bf}</td></tr>')
    h.append('</table></section>')

    # Ex 5
    h.append('<section class="ex"><h2><span class="n">6</span>Le schéma du volcan<span class="pts">… / 3,5</span></h2>')
    h.append('<p class="consigne">Complète le schéma avec les mots de la liste.' + (' <span class="bareme">(0,5 point par étiquette)</span>' if K else '') + '</p>')
    h.append('<div class="bank">magma · cheminée · cratère · lave · nuage de cendres · explosion volcanique · anciennes coulées de lave</div>')
    h.append(volcano(K))
    h.append('</section>')

    # Ex 6
    h.append('<section class="ex"><h2><span class="n">7</span>Qu’est-ce qu’un volcan ?<span class="pts">… / 3,5</span></h2>')
    h.append('<p class="consigne">Complète le texte avec les mots de la liste.' + (' <span class="bareme">(0,5 point par mot)</span>' if K else '') + '</p>')
    h.append('<div class="bank">lave · cratère · solide · éruption · montagne · cheminée · magma</div>')
    h.append('<p class="texte">Un volcan se présente sous l’aspect d’une ' + B("montagne", K) + ' avec un ' + B("cratère", K) +
             ' à son sommet. Il est formé autour d’une fissure de la croûte terrestre, la ' + B("cheminée", K) +
             ', par laquelle remontent des roches très chaudes et partiellement fondues : le ' + B("magma", K) +
             '. Une ' + B("éruption", K) + ' volcanique a lieu lorsque ce magma est éjecté en surface. Il prend alors le nom de ' +
             B("lave", K) + ' et, en refroidissant, devient de la roche ' + B("solide", K) + '.</p>')
    h.append('</section>')

    if K:
        h.append('<section class="ex" style="margin-top:8px"><h2><span class="n">✓</span>Récapitulatif du barème<span class="pts">20</span></h2>'
                 '<table class="comp" style="font-size:9pt;margin-top:4px"><tr><th style="text-align:left">Compétence</th><th>Exercices</th><th>Points</th></tr>'
                 '<tr><td>Je connais la structure de la Terre.</td><td style="text-align:center">1 · 2</td><td style="text-align:center">5</td></tr>'
                 '<tr><td>Je sais expliquer le mouvement des plaques et ses conséquences.</td><td style="text-align:center">3 · 4</td><td style="text-align:center">5</td></tr>'
                 '<tr><td>Je connais les parties d’un volcan.</td><td style="text-align:center">6</td><td style="text-align:center">3,5</td></tr>'
                 '<tr><td>Je sais expliquer une éruption volcanique.</td><td style="text-align:center">7</td><td style="text-align:center">3,5</td></tr>'
                 '<tr><td>Je mobilise mes connaissances.</td><td style="text-align:center">5</td><td style="text-align:center">3</td></tr></table>'
                 '<p class="bareme" style="margin-top:6px">Repère possible : compétence acquise si au moins 75 % des points, en cours entre 40 % et 75 %, non acquise en dessous.</p></section>')
    else:
        h.append('<p class="foot">Relis bien tes réponses avant de rendre ta copie. Bon courage !</p>')
    h.append('</body></html>')
    return "".join(h)

open(os.path.join(OUT, "evaluation-sujet.html"), "w").write(doc(False))
open(os.path.join(OUT, "evaluation-corrige.html"), "w").write(doc(True))
