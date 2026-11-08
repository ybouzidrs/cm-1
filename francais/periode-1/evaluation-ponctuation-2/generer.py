# Usage : python3 generer.py <dossier de sortie> <chemin de sciences/periode-1/evaluation/generer.py (styles communs)>
import sys, os, re
OUT = sys.argv[1]
CSS = re.search(r'CSS = """(.*?)"""', open(sys.argv[2]).read(), re.S).group(1)
CSS += """
table.grid { width: 100%; border-collapse: collapse; }
table.grid td, table.grid th { border: 1.2px solid #555; padding: 5px 8px; }
table.grid th { background: #eee; font-size: 10pt; }
table.grid td.c, table.grid th.c { width: 92px; text-align: center; }
.sq { display: inline-block; min-width: 26px; height: 24px; border: 1.5px solid #111; border-radius: 5px; vertical-align: middle; text-align: center; line-height: 22px; margin: 0 3px; font-weight: 700; font-family: "Times New Roman", serif; font-size: 14pt; }
.sq.ans { color: #c0392b; border-color: #c0392b; }
.num { display: inline-block; width: 18px; height: 18px; border-radius: 50%; background: #111; color: #fff; font-size: 9pt; font-weight: 700; text-align: center; line-height: 18px; vertical-align: super; margin-left: 1px; }
.sign { font-family: "Times New Roman", serif; font-size: 14pt; font-weight: 700; padding: 0 2px; }
.lines-p { line-height: 2.3; }
.field { display: flex; gap: 6px; align-items: baseline; margin: 4px 0; }
.field .blank { flex: 1; min-width: 0; }
.bank.signs { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; }
.chip-s { display: inline-block; min-width: 34px; padding: 0 8px; border: 1.5px solid #111; border-radius: 6px; text-align: center; font-family: "Times New Roman", serif; font-size: 16pt; font-weight: 700; line-height: 28px; background: #fff; }
.texte-doc { border: 1.5px solid #555; border-radius: 8px; padding: 8px 12px; line-height: 2; background: #fafafa; }
"""
def B(a, K, c=""): return f'<span class="blank filled ans">{a}</span>' if K else f'<span class="blank {c}"></span>'
def pts(K, t): return f' <span class="bareme">({t})</span>' if K else ''
def box(K, on): return f'<span class="box{" x" if (K and on) else ""}"></span>'
def SQ(a, K): return f'<span class="sq ans">{a}</span>' if K else '<span class="sq"></span>'
def BANK(signs): return '<div class="bank signs">' + "".join(f'<span class="chip-s">{x}</span>' for x in signs) + '</div>'
def N(i): return f'<span class="num">{i}</span>'

def doc(K):
    h = [f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{"Corrigé · " if K else ""}Évaluation 2 de grammaire · La ponctuation</title>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Lilita+One&display=swap">'
         f'<style>{CSS}</style>' + ('<style>body{font-size:10.5pt;line-height:1.38} .ex{margin-top:9px} .bank{margin:2px 0 4px;padding:3px 8px} table.grid td,table.grid th{padding:3px 8px}</style>' if K else '') + '</head><body>']
    h.append('<div class="head"><div><div class="theme">Français · Grammaire · G4 · La ponctuation · Évaluation 2</div>')
    h.append(f'<h1>{"Corrigé et barème &nbsp;<span class=tag>ENSEIGNANT</span>" if K else "Évaluation de grammaire"}</h1>')
    h.append('<div style="margin-top:6px;font-size:10.5pt">Réponses attendues en <b class="ans">rouge</b>. Le barème est indiqué à droite de chaque titre (total : 20 points).</div>' if K else '<div class="ident"><span>Prénom :</span><span>Date :</span></div>')
    h.append('</div><div class="note"><small>Note</small><b>' + ('<em>20</em>' if K else '&nbsp;&nbsp;&nbsp;') + ' / 20</b></div></div>')
    comps = [("Je connais le nom et le rôle des signes de ponctuation.", "1 · 3", "5,5"),
             ("Je reconnais et j’écris les différents types de phrases.", "2 · 8", "5"),
             ("Je choisis le bon signe de ponctuation dans une phrase.", "4 · 5", "4,5"),
             ("Je corrige et je ponctue un texte (avec les majuscules).", "6 · 7", "5")]
    if not K:
        h.append('<table class="comp"><tr><th style="text-align:left">Compétences évaluées</th><th>Exercices</th><th class="c">Acquis</th><th class="c">En cours</th><th class="c">Non acquis</th></tr>'
                 + "".join(f'<tr><td>{c}</td><td style="text-align:center">{e}</td><td class="c"></td><td class="c"></td><td class="c"></td></tr>' for c, e, _ in comps) + '</table>')

    # 1 Qui suis-je
    h.append('<section class="ex"><h2><span class="n">1</span>Qui suis-je ?<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Écris le nom du signe de ponctuation. Attention, il y a deux noms en trop dans la liste.' + pts(K, "0,5 point par réponse") + '</p>')
    h.append('<div class="bank">les guillemets · la virgule · le point d’interrogation · les parenthèses · le tiret · les deux-points · le point-virgule · les points de suspension</div><ol class="alpha">')
    for l, d, a in [("a)", "Je marque la fin d’une phrase qui pose une question.", "le point d’interrogation"),
                    ("b)", "J’introduis une explication ou une énumération.", "les deux-points"),
                    ("c)", "J’indique une suite possible.", "les points de suspension"),
                    ("d)", "On m’utilise pour donner une précision.", "les parenthèses"),
                    ("e)", "Je marque le début et la fin des paroles d’un personnage.", "les guillemets"),
                    ("f)", "Entre le point et la virgule, je marque une pause plus longue.", "le point-virgule")]:
        h.append(f'<li><span>{l}</span><span class="def"><span>{d}</span>{B(a, K)}</span></li>')
    h.append('</ol>')
    if K: h.append('<p class="bareme">Les deux noms en trop : la virgule et le tiret.</p>')
    h.append('</section>')

    # 2 Types de phrases
    h.append('<section class="ex"><h2><span class="n">2</span>Quel type de phrase ?<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Regarde la ponctuation et coche le type de chaque phrase.' + pts(K, "0,5 point par ligne") + '</p>')
    ty = [("Où habites-tu ?", 1), ("Les feuilles tombent en automne.", 0), ("Comme ce gâteau est bon !", 2),
          ("Est-ce que tu as fini tes devoirs ?", 1), ("Quelle belle journée !", 2), ("Le train part à huit heures.", 0)]
    h.append('<table class="grid"><tr><th style="text-align:left">Phrase</th><th class="c">déclarative</th><th class="c">interrogative</th><th class="c">exclamative</th></tr>' +
             "".join(f'<tr><td>{p}</td>' + "".join(f'<td class="c">{box(K, j == k)}</td>' for j in range(3)) + '</tr>' for p, k in ty) + '</table></section>')

    # 3 Observe le texte
    h.append('<section class="ex"><h2><span class="n">3</span>Le rôle des signes dans un texte<span class="pts">… / 2,5</span></h2>')
    h.append('<p class="consigne">Lis le texte. Pour chaque signe numéroté, écris son rôle en choisissant dans la liste.' + pts(K, "0,5 point par signe") + '</p>')
    h.append('<div class="texte-doc"><span class="sign">«</span>' + N(1) + ' Maman, où est mon cartable <span class="sign">?</span>' + N(2) + ' » demande Lucas.<br>'
             '<span class="sign">—</span>' + N(3) + ' Sous la table, répond-elle.<br>'
             'Dans son cartable, Lucas range tout <span class="sign">:</span>' + N(4) + ' ses cahiers, ses livres et sa trousse. Il est prêt pour une nouvelle journée<span class="sign">…</span>' + N(5) + '</div>')
    h.append('<div class="bank" style="margin-top:6px">la fin d’une question · le changement de personnage · une suite possible · le début des paroles d’un personnage · une énumération</div>')
    roles = ["le début des paroles d’un personnage", "la fin d’une question", "le changement de personnage", "une énumération", "une suite possible"]
    h.append('<div style="display:grid;gap:4px">' + "".join(f'<div class="field"><span>Signe {i + 1} :</span>{B(r, K)}</div>' for i, r in enumerate(roles)) + '</div>')
    h.append('</section>')

    # 4 Choisis le bon signe
    h.append('<section class="ex"><h2><span class="n">4</span>Choisis le bon signe<span class="pts">… / 3</span></h2>')
    h.append('<p class="consigne">Écris dans la case le signe qui convient. Utilise chaque signe une seule fois.' + pts(K, "0,5 point par case") + '</p>')
    h.append(BANK([":", "…", "!", "?", ";", "."]))
    ch = [("J’ai acheté trois fruits", ":", " une pomme, une poire et une banane."), ("Pourquoi le ciel est-il bleu", "?", ""),
          ("Quelle belle surprise", "!", ""), ("Je compte jusqu’à trois : un, deux", "…", ""),
          ("Ma sœur aime la danse", ";", " mon frère préfère le football."), ("Hier, je suis allé au cinéma avec mon oncle", ".", "")]
    h.append('<ol class="alpha">' + "".join(f'<li><span>{"abcdef"[i]})</span><span>{a} {SQ(s_, K)}{b}</span></li>' for i, (a, s_, b) in enumerate(ch)) + '</ol>')
    if K: h.append('<p class="bareme">Pour e), le point-virgule est attendu (pause plus longue entre deux idées). Si l’élève met une virgule, compter 0,25 point.</p>')
    h.append('</section>')

    # 5 Parenthèses
    h.append('<section class="ex"><h2><span class="n">5</span>Les parenthèses<span class="pts">… / 1,5</span></h2>')
    h.append('<p class="consigne">a) Ajoute les parenthèses pour isoler la précision.' + pts(K, "0,5 point par phrase") + '</p>')
    h.append(f'<p class="lines-p">• Mon cousin {SQ("(", K)} il a dix ans {SQ(")", K)} vient passer les vacances chez nous.<br>'
             f'• Paris {SQ("(", K)} la capitale de la France {SQ(")", K)} est une très grande ville.</p>')
    h.append(f'<p class="consigne">b) À quoi servent les parenthèses ? Elles servent à {B("donner une précision", K, "l")}.{pts(K, "0,5 point")}</p>')
    h.append('</section>')

    # 6 Corrige
    h.append('<section class="ex"><h2><span class="n">6</span>Chasse aux erreurs<span class="pts">… / 2,5</span></h2>')
    h.append('<p class="consigne">Chaque phrase contient <u>une</u> erreur de ponctuation ou de majuscule. Recopie la phrase en la corrigeant.' + pts(K, "0,5 point par phrase") + '</p>')
    err = [("Où vas-tu.", "Où vas-tu ?"), ("J’ai deux chats : Ils s’appellent Tom et Lou.", "J’ai deux chats : ils s’appellent Tom et Lou."),
           ("Quelle chance.", "Quelle chance !"), ("Il attendit… puis il partit.", "Il attendit… Puis il partit."),
           ("Le maître dit « Asseyez-vous ! »", "Le maître dit : « Asseyez-vous ! »")]
    for i, (a, b) in enumerate(err):
        h.append(f'<p style="margin:5px 0 0"><b>{"abcde"[i]})</b> {a}</p>')
        h.append(f'<div class="answer-box" style="margin:2px 0 4px">{b}</div>' if K else '<div class="lines" style="margin:0"><div class="line" style="height:24px"></div></div>')
    if K: h.append('<p class="bareme">Rappels : pas de majuscule après les deux-points ; une majuscule après des points de suspension ; les deux-points annoncent les paroles d’un personnage.</p>')
    h.append('</section>')

    # 7 Texte sans ponctuation
    h.append('<section class="ex"><h2><span class="n">7</span>Ponctue le texte<span class="pts">… / 2,5</span></h2>')
    h.append('<p class="consigne">Complète le texte avec les 5 signes de la liste.' + pts(K, "0,5 point par case") + '</p>')
    h.append(BANK(["?", ",", "!", ".", ":"]))
    h.append(f'<p class="lines-p">Ce matin {SQ(",", K)} Zoé se réveille très tôt {SQ(".", K)} Elle court à la fenêtre et s’écrie {SQ(":", K)} « Il neige {SQ("!", K)} » '
             f'Va-t-elle pouvoir faire un bonhomme de neige {SQ("?", K)}</p>')
    h.append('</section>')

    # 8 Transforme
    h.append('<section class="ex"><h2><span class="n">8</span>Transforme les phrases<span class="pts">… / 2</span></h2>')
    h.append('<p class="consigne">Transforme chaque phrase déclarative comme indiqué.' + pts(K, "1 point par phrase : 0,5 point pour la phrase, 0,5 point pour le bon signe") + '</p>')
    h.append('<p style="margin:4px 0 0"><b>a)</b> Tu aimes la piscine. → en phrase <b>interrogative</b> :</p>')
    h.append('<div class="answer-box">Aimes-tu la piscine ? · Est-ce que tu aimes la piscine ? · Tu aimes la piscine ?</div>' if K else '<div class="lines" style="margin:0"><div class="line"></div></div>')
    h.append('<p style="margin:6px 0 0"><b>b)</b> Ce paysage est beau. → en phrase <b>exclamative</b> :</p>')
    h.append('<div class="answer-box">Comme ce paysage est beau ! · Que ce paysage est beau ! · Ce paysage est beau !</div>' if K else '<div class="lines" style="margin:0"><div class="line"></div></div>')
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
