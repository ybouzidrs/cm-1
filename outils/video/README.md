# Vidéos en bande dessinée

Le programme qui fabrique les vidéos MP4 des leçons, image par image.

- `engine.js` : le moteur (personnages, bulles, sous-titres, décors)
- `anglais.js`, `geographie.js` : les scènes de chaque vidéo
- `render.js` : fabrique la vidéo (`node render.js anglais sortie.mp4`). Il faut Playwright et ffmpeg.
- `voix.js` : ajoute la voix de robot (`node voix.js anglais sortie.mp4`). Il faut aussi `espeak-ng` et les voix MBROLA `mbrola-fr1` et `mbrola-en1`. Il écrit `voix-<film>.js`, qui allonge les bulles quand la voix parle plus longtemps.
