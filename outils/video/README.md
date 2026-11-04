# Vidéos en bande dessinée

Le programme qui fabrique les vidéos MP4 des leçons, image par image.

- `engine.js` : le moteur (personnages, bulles, sous-titres, décors)
- `anglais.js`, `geographie.js` : les scènes de chaque vidéo
- `render.js` : fabrique la vidéo (`node render.js anglais sortie.mp4`). Il faut Playwright et ffmpeg.
