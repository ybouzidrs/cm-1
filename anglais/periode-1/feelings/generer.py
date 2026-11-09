# Usage : python3 generer.py <dossier de sortie> <chemin de sciences/periode-1/evaluation/generer.py (styles communs)>
# Les smileys (smileys/00.png à 14.png) sont découpés dans la photo de la leçon « Feelings ».
import sys, os, re, base64
OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = re.search(r'CSS = """(.*?)"""', open(sys.argv[2]).read(), re.S).group(1)
CSS += """
.grid15 { display: grid; grid-template-columns: repeat(3, 1fr); border: 2px solid #111; }
.cell { border: 1px solid #111; height: 40mm; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 6px 8px 8px; }
.cell img { max-height: 27mm; max-width: 95%; object-fit: contain; }
.cell .draw { flex: 1; width: 100%; }
.cell .word { font-size: 17pt; font-weight: 700; font-family: Arial, sans-serif; }
.cell .wline { width: 88%; display: flex; gap: 6px; align-items: baseline; font-size: 12pt; }
.cell .wline .blank { flex: 1; min-width: 0; }
.cell .wline .ans { font-size: 14pt; }
.sub { text-align: center; font-size: 13pt; margin: 4px 0 8px; font-style: italic; }
"""
WORDS = ["happy", "sad", "tired", "hot", "cold", "angry", "scared", "thirsty", "hungry", "surprised", "proud", "so-so", "sleepy", "sick", "in love"]
ORDER1 = [6, 12, 0, 10, 3, 8, 14, 1, 11, 4, 9, 2, 7, 13, 5]   # ordre mélangé pour l'exercice 1
ORDER2 = [9, 4, 13, 0, 7, 11, 5, 14, 2, 8, 3, 12, 1, 10, 6]   # ordre mélangé pour l'exercice 2
IMG = [ "data:image/png;base64," + base64.b64encode(open(os.path.join(HERE, "smileys", f"{i:02d}.png"), "rb").read()).decode() for i in range(15)]

def head(K, sub):
    return ('<div class="head"><div><div class="theme">Anglais · Feelings · How are you? I am …</div>'
            f'<h1>{"Corrigé &nbsp;<span class=tag>ENSEIGNANT</span>" if K else "Feelings"}</h1>'
            + ('' if K else '<div class="ident"><span>Name :</span><span>Date :</span></div>') +
            f'</div><div class="note"><small>{sub}</small><b>' + ('<em>15</em>' if K else '&nbsp;&nbsp;&nbsp;') + ' / 15</b></div></div>')

def doc(K):
    h = [f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{"Corrigé · " if K else ""}Feelings · exercices</title>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Lilita+One&display=swap">'
         f'<style>{CSS}</style></head><body>']
    # Page 1
    h.append(head(K, "Exercice 1"))
    h.append('<section class="ex"><h2><span class="n">1</span>How are you? Write the feeling.<span class="pts">… / 15</span></h2>')
    h.append('<p class="consigne">Regarde chaque smiley et écris le sentiment en anglais.' + (' <span class="bareme">(1 point par mot ; 0,5 point si une seule lettre est fausse)</span>' if K else '') + '</p>')
    h.append('<div class="grid15">' + "".join(
        f'<div class="cell"><img src="{IMG[i]}" alt=""><div class="wline"><span>I am</span>'
        + (f'<span class="blank filled ans">{WORDS[i]}</span>' if K else '<span class="blank"></span>') + '</div></div>' for i in ORDER1) + '</div>')
    h.append('</section>')
    # Page 2
    h.append('<div class="pagebreak"></div>')
    h.append(head(K, "Exercice 2"))
    h.append('<section class="ex"><h2><span class="n">2</span>Draw the feeling.<span class="pts">… / 15</span></h2>')
    h.append('<p class="consigne">Lis le mot et dessine le smiley qui correspond dans la case.' + (' <span class="bareme">(1 point par smiley si l’expression correspond bien au mot ; voici les smileys de la leçon pour comparer)</span>' if K else '') + '</p>')
    h.append('<div class="grid15">' + "".join(
        f'<div class="cell">' + (f'<img src="{IMG[i]}" alt="">' if K else '<div class="draw"></div>') + f'<div class="word">{WORDS[i]}</div></div>' for i in ORDER2) + '</div>')
    h.append('</section></body></html>')
    return "".join(h)

open(os.path.join(OUT, "feelings-exercices.html"), "w").write(doc(False))
open(os.path.join(OUT, "feelings-corrige.html"), "w").write(doc(True))
