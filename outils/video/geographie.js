/* Vidéo « Les lieux où j'habite » avec Colombo, la colombe du blason de Colombes (géographie, CM1). */
"use strict";
const BOX = { x: 230, y: 34, w: 860 }, TAIL = { x: 175, y: 150 };
function colomboNarr(S) { S.actor("colombo", (g, t, k) => drawDove(g, 110, 210, 0.5, t, k)); }
const say = (S, text, o) => S.say("colombo", text, null, BOX, TAIL, o);

/* ---------- dessins ---------- */
function blason(g, x, y, s, t) {
  g.save(); g.translate(x, y); g.scale(s, s); g.lineWidth = 6; g.strokeStyle = INK; g.lineJoin = "round";
  g.fillStyle = "#2b3150"; g.beginPath(); g.moveTo(-150, -190); g.lineTo(150, -190); g.lineTo(150, 40); g.quadraticCurveTo(150, 160, 0, 210); g.quadraticCurveTo(-150, 160, -150, 40); g.closePath(); g.fill(); g.stroke();
  g.save(); g.clip();
  g.fillStyle = "#f4f4f4"; g.fillRect(-160, 70, 320, 160);
  g.strokeStyle = "#2b3150"; g.lineWidth = 3;
  for (let r = 0; r < 6; r++) { g.beginPath(); g.moveTo(-160, 70 + r * 26); g.lineTo(160, 70 + r * 26); g.stroke(); for (let c = -6; c < 7; c++) { const xx = c * 46 + (r % 2) * 23; g.beginPath(); g.moveTo(xx, 70 + r * 26); g.lineTo(xx, 96 + r * 26); g.stroke(); } }
  g.restore();
  g.fillStyle = "#f4f4f4"; for (let i = -2; i <= 2; i++) { g.fillRect(i * 62 - 18, 44, 36, 28); g.strokeStyle = "#2b3150"; g.lineWidth = 3; g.strokeRect(i * 62 - 18, 44, 36, 28); }
  g.fillStyle = "#f4f4f4"; g.fillRect(-30, -95, 60, 170); g.strokeStyle = "#2b3150"; g.lineWidth = 3;
  for (let r = 0; r < 7; r++) { g.beginPath(); g.moveTo(-30, -95 + r * 24); g.lineTo(30, -95 + r * 24); g.stroke(); }
  g.fillStyle = "#2b3150"; g.beginPath(); g.moveTo(-13, 75); g.lineTo(-13, 40); g.arc(0, 40, 13, Math.PI, 0); g.lineTo(13, 75); g.closePath(); g.fill();
  g.fillStyle = "#f4f4f4"; g.beginPath(); g.moveTo(-40, -95); g.lineTo(0, -175); g.lineTo(40, -95); g.closePath(); g.fill();
  g.restore();
  g.save(); g.translate(x - 85 * s, y - 40 * s); drawDove(g, 0, 0, 0.3 * s, t + 0.5, false); g.restore();
  g.save(); g.translate(x + 85 * s, y - 40 * s); g.scale(-1, 1); drawDove(g, 0, 0, 0.3 * s, t, false); g.restore();
}
function house(g, x, y, s, wall, roof) {
  g.save(); g.translate(x, y); g.scale(s, s); g.lineWidth = 5; g.strokeStyle = INK; g.lineJoin = "round";
  g.fillStyle = wall; g.fillRect(-60, -90, 120, 90); g.strokeRect(-60, -90, 120, 90);
  g.fillStyle = roof; g.beginPath(); g.moveTo(-75, -88); g.lineTo(0, -150); g.lineTo(75, -88); g.closePath(); g.fill(); g.stroke();
  g.fillStyle = "#8fd3ff"; g.fillRect(-45, -70, 30, 26); g.strokeRect(-45, -70, 30, 26); g.fillRect(15, -70, 30, 26); g.strokeRect(15, -70, 30, 26);
  g.fillStyle = "#8a5a36"; g.fillRect(-14, -44, 28, 44); g.strokeRect(-14, -44, 28, 44);
  g.restore();
}
function shop(g, x, y, s) {
  g.save(); g.translate(x, y); g.scale(s, s); g.lineWidth = 5; g.strokeStyle = INK;
  g.fillStyle = "#fff1d6"; g.fillRect(-70, -110, 140, 110); g.strokeRect(-70, -110, 140, 110);
  for (let i = 0; i < 7; i++) { g.fillStyle = i % 2 ? "#fff" : "#e5484d"; g.fillRect(-70 + i * 20, -110, 20, 26); }
  g.strokeRect(-70, -110, 140, 26);
  g.fillStyle = "#8fd3ff"; g.fillRect(-55, -70, 60, 50); g.strokeRect(-55, -70, 60, 50);
  g.fillStyle = "#8a5a36"; g.fillRect(18, -64, 34, 64); g.strokeRect(18, -64, 34, 64);
  g.restore();
  txt(g, "BOULANGERIE", x, y - 116 * s, { size: 15 * s * 1.6, font: FONT_T });
}
function school(g, x, y, s) {
  g.save(); g.translate(x, y); g.scale(s, s); g.lineWidth = 5; g.strokeStyle = INK;
  g.fillStyle = "#ffe08a"; g.fillRect(-120, -130, 240, 130); g.strokeRect(-120, -130, 240, 130);
  g.fillStyle = "#e5484d"; g.beginPath(); g.moveTo(-135, -128); g.lineTo(0, -180); g.lineTo(135, -128); g.closePath(); g.fill(); g.stroke();
  g.fillStyle = "#8fd3ff"; for (const xx of [-95, -45, 25, 75]) { g.fillRect(xx, -100, 30, 30); g.strokeRect(xx, -100, 30, 30); }
  g.fillStyle = "#8a5a36"; g.fillRect(-20, -56, 40, 56); g.strokeRect(-20, -56, 40, 56);
  g.restore();
  txt(g, "ÉCOLE", x, y - 140 * s, { size: 34 * s, font: FONT_T, color: "#fff", stroke: INK, strokeW: 6 });
}
function tree(g, x, y, s) {
  g.save(); g.translate(x, y); g.scale(s, s); g.lineWidth = 5; g.strokeStyle = INK;
  g.fillStyle = "#8a5a36"; g.fillRect(-10, -60, 20, 60); g.strokeRect(-10, -60, 20, 60);
  g.fillStyle = "#4caf50"; g.beginPath(); g.arc(0, -90, 44, 0, 7); g.fill(); g.stroke();
  g.restore();
}
function mairie(g, x, y, s) {
  g.save(); g.translate(x, y); g.scale(s, s); g.lineWidth = 5; g.strokeStyle = INK; g.lineJoin = "round";
  g.fillStyle = "#f3ead8"; g.fillRect(-180, -170, 360, 170); g.strokeRect(-180, -170, 360, 170);
  g.beginPath(); g.moveTo(-200, -168); g.lineTo(0, -250); g.lineTo(200, -168); g.closePath(); g.fill(); g.stroke();
  g.fillStyle = "#fff"; g.beginPath(); g.arc(0, -200, 22, 0, 7); g.fill(); g.stroke();
  g.beginPath(); g.moveTo(0, -200); g.lineTo(0, -214); g.moveTo(0, -200); g.lineTo(10, -196); g.stroke();
  g.fillStyle = "#e9dcc0"; for (let i = -3; i <= 3; i++) { if (i === 0) continue; g.fillRect(i * 48 - 12, -150, 24, 150); g.strokeRect(i * 48 - 12, -150, 24, 150); }
  g.fillStyle = "#6b4a2b"; g.beginPath(); g.moveTo(-26, 0); g.lineTo(-26, -70); g.arc(0, -70, 26, Math.PI, 0); g.lineTo(26, 0); g.closePath(); g.fill(); g.stroke();
  g.fillStyle = "#2b3150"; g.fillRect(-90, -166, 180, 30); g.strokeRect(-90, -166, 180, 30);
  g.restore();
  txt(g, "MAIRIE", x, y - 143 * s, { size: 24 * s, font: FONT_T, color: "#fff" });
  // drapeau
  g.save(); g.translate(x, y - 250 * s); g.lineWidth = 4; g.strokeStyle = INK; g.beginPath(); g.moveTo(0, 0); g.lineTo(0, -70 * s); g.stroke();
  ["#1f3f9a", "#fff", "#d62839"].forEach((c, i) => { g.fillStyle = c; g.fillRect(i * 18 * s, -70 * s, 18 * s + 1, 36 * s); }); g.strokeRect(0, -70 * s, 54 * s, 36 * s); g.restore();
}
function frFlag(g, x, y, w, h) { ["#1f3f9a", "#ffffff", "#d62839"].forEach((c, i) => { g.fillStyle = c; g.fillRect(x + i * w / 3, y, w / 3 + 1, h); }); g.lineWidth = 5; g.strokeStyle = INK; g.strokeRect(x, y, w, h); }
function euFlag(g, x, y, w, h, t) {
  g.fillStyle = "#1f3f9a"; g.fillRect(x, y, w, h); g.lineWidth = 5; g.strokeStyle = INK; g.strokeRect(x, y, w, h);
  const cx = x + w / 2, cy = y + h / 2, R = h * 0.33;
  for (let i = 0; i < 12; i++) {
    const a = i / 12 * Math.PI * 2, sx = cx + Math.cos(a) * R, sy = cy + Math.sin(a) * R;
    g.save(); g.translate(sx, sy); g.fillStyle = "#ffd21f"; g.beginPath();
    for (let k = 0; k < 10; k++) { const rr2 = k % 2 ? h * 0.018 : h * 0.045, b = k / 10 * Math.PI * 2 - Math.PI / 2; k ? g.lineTo(Math.cos(b) * rr2, Math.sin(b) * rr2) : g.moveTo(Math.cos(b) * rr2, Math.sin(b) * rr2); }
    g.closePath(); g.fill(); g.restore();
  }
}
function compass(g, x, y, r) {
  g.save(); g.translate(x, y); g.lineWidth = 3; g.strokeStyle = INK;
  g.fillStyle = "#fff"; g.beginPath(); g.arc(0, 0, r, 0, 7); g.fill(); g.stroke();
  g.fillStyle = "#555"; g.beginPath(); g.moveTo(0, -r * 0.9); g.lineTo(r * 0.16, 0); g.lineTo(0, r * 0.9); g.lineTo(-r * 0.16, 0); g.closePath(); g.fill(); g.stroke();
  g.beginPath(); g.moveTo(-r * 0.9, 0); g.lineTo(0, r * 0.16); g.lineTo(r * 0.9, 0); g.lineTo(0, -r * 0.16); g.closePath(); g.fill(); g.stroke();
  g.restore();
  [["N", 0, -1], ["S", 0, 1], ["E", 1, 0], ["O", -1, 0]].forEach(([l, a, b]) => txt(g, l, x + a * (r + 18), y + b * (r + 18) + 9, { size: 26, font: FONT_T }));
  [["NO", -1, -1], ["NE", 1, -1], ["SO", -1, 1], ["SE", 1, 1]].forEach(([l, a, b]) => txt(g, l, x + a * r * 0.85, y + b * r * 0.85 + 6, { size: 15, font: FONT_T, color: "#666" }));
}
function ballot(g, x, y, s, t) {
  g.save(); g.translate(x, y); g.scale(s, s); g.lineWidth = 5; g.strokeStyle = INK;
  const drop = (t * 0.8) % 1;
  g.fillStyle = "#fff"; g.save(); g.translate(0, -60 + drop * 50); rr(g, -30, -40, 60, 40, 4); g.fill(); g.stroke(); g.restore();
  g.fillStyle = "rgba(200,230,255,.85)"; rr(g, -70, -40, 140, 110, 8); g.fill(); g.stroke();
  g.fillStyle = INK; g.fillRect(-36, -42, 72, 8);
  g.restore();
  txt(g, "VOTE", x, y + 40 * s, { size: 26 * s, font: FONT_T, color: "#1f3f9a" });
}
const FRANCE = [[1.58,50.87],[2.55,51.08],[4.15,50.0],[4.85,50.15],[5.9,49.5],[6.4,49.45],[7.6,49.05],[8.2,48.97],[7.6,47.6],[6.9,47.5],[6.05,46.4],[6.8,46.0],[7.0,45.5],[6.6,45.1],[7.0,44.25],[7.5,43.8],[6.6,43.15],[5.4,43.2],[4.6,43.4],[3.2,43.0],[3.15,42.45],[1.7,42.5],[0.0,42.7],[-1.78,43.35],[-1.45,43.6],[-1.25,44.6],[-1.15,45.6],[-1.25,46.15],[-2.15,47.0],[-2.5,47.3],[-4.4,47.8],[-4.75,48.35],[-4.1,48.7],[-3.0,48.8],[-2.0,48.6],[-1.6,48.65],[-1.95,49.7],[-1.25,49.7],[-1.1,49.35],[0.2,49.45],[1.4,50.05]];
const CORSE = [[9.4,43.0],[9.55,42.1],[9.2,41.37],[8.6,41.9],[8.7,42.6]];
function france(g, x0, y0, k, t) {
  const P = ([lon, lat]) => [x0 + (lon + 5) * 0.68 * k, y0 + (51.2 - lat) * k];
  g.save(); g.lineWidth = 5; g.strokeStyle = INK; g.lineJoin = "round"; g.fillStyle = "#cfe3ff";
  for (const poly of [FRANCE, CORSE]) { g.beginPath(); poly.forEach((p, i) => { const [x, y] = P(p); i ? g.lineTo(x, y) : g.moveTo(x, y); }); g.closePath(); g.fill(); g.stroke(); }
  const [px, py] = P([2.35, 48.86]);
  g.fillStyle = "#d62839"; g.beginPath(); g.arc(px, py, 7 + Math.sin(t * 6) * 2, 0, 7); g.fill(); g.stroke();
  g.restore();
  txt(g, "Paris", px + 14, py - 8, { size: 22, font: FONT_T, align: "left" });
}
/* schéma de l'Île-de-France : Paris, petite couronne, grande couronne */
function sectorPath(g, cx, cy, r1, r2, a1, a2) {
  const P = (r, a) => [cx + r * Math.sin(a * Math.PI / 180), cy - r * Math.cos(a * Math.PI / 180)];
  g.beginPath(); const steps = 30;
  for (let i = 0; i <= steps; i++) { const [x, y] = P(r2, a1 + (a2 - a1) * i / steps); i ? g.lineTo(x, y) : g.moveTo(x, y); }
  for (let i = steps; i >= 0; i--) { const [x, y] = P(r1, a1 + (a2 - a1) * i / steps); g.lineTo(x, y); }
  g.closePath();
}
const IDF = [
  ["Val-d’Oise", "95", 124, 205, 300, 420, "g"], ["Seine-et-Marne", "77", 124, 205, 60, 160, "g"], ["Essonne", "91", 124, 205, 160, 230, "g"], ["Yvelines", "78", 124, 205, 230, 300, "g"],
  ["Seine-Saint-Denis", "93", 46, 124, 330, 460, "p"], ["Val-de-Marne", "94", 46, 124, 100, 210, "p"], ["Hauts-de-Seine", "92", 46, 124, 210, 330, "p"],
];
function idf(g, cx, cy, a, t) {
  // a : 0 = Paris seul, 1 = + petite couronne, 2 = + grande couronne
  const lvl = (ring) => ring === "p" ? clamp(a, 0, 1) : clamp(a - 1, 0, 1);
  for (const [name, num, r1, r2, a1, a2, ring] of IDF) {
    const v = lvl(ring); if (v <= 0) continue;
    g.save(); g.globalAlpha = v; sectorPath(g, cx, cy, r1, r2, a1, a2);
    g.fillStyle = ring === "p" ? (num === "92" ? "#ffd34d" : "#ffb38a") : "#bfe3b4"; g.fill(); g.lineWidth = 4; g.strokeStyle = INK; g.stroke();
    const am = (a1 + a2) / 2 * Math.PI / 180, rm = (r1 + r2) / 2, x = cx + rm * Math.sin(am), y = cy - rm * Math.cos(am);
    txt(g, num, x, y + 4, { size: ring === "p" ? 30 : 34, font: FONT_T });
    const parts = name.length > 12 && ring === "p" ? name.replace("-de-", "-de- ").replace("-Saint-", "- Saint-").split(" ") : [name];
    parts.forEach((p, i) => txt(g, p, x, y + 26 + i * 17, { size: 15, weight: "bold" }));
    g.restore();
  }
  g.save(); g.fillStyle = "#fff"; g.lineWidth = 4; g.strokeStyle = INK; g.beginPath(); g.arc(cx, cy, 46, 0, 7); g.fill(); g.stroke(); g.restore();
  txt(g, "75", cx, cy + 4, { size: 30, font: FONT_T }); txt(g, "Paris", cx, cy + 26, { size: 15, weight: "bold" });
}
function chip(g, x, y, w, h, fill, label, age, o = {}) {
  const a = card(g, x, y, w, h, fill, age, o);
  if (age > 0.2) txt(g, label, x + w / 2, y + h / 2 + (o.size || 26) * 0.35, { size: o.size || 26, font: o.font || FONT_B, weight: o.weight || "bold", color: o.color || INK });
  return a;
}
function chips(S, items, x0, y0, cols, w, h, gap, fill, dt, o) {
  S.show((g, a) => items.forEach((it, i) => {
    const age = a - i * dt; if (age < 0) return;
    const col = i % cols, row = Math.floor(i / cols);
    chip(g, x0 + col * (w + gap), y0 + row * (h + gap), w, h, typeof fill === "function" ? fill(i) : fill, it, age, o);
  }), items.length * dt + 0.4);
}

/* ---------- les scènes ---------- */
const SCENES = [
  S => { S.bg((g, t) => { titleCard(g, t, "Les lieux où j’habite", "Géographie · Thème 1 · CM1", "#2f8f5b"); drawDove(g, 1080, 560, 0.6, t, false); }); S.wait(3.8); },

  // Colombo se présente
  S => {
    S.bg((g, t) => { sky(g, "day"); ground(g); blason(g, 960, 360, 0.95, t); });
    S.actor("colombo", (g, t, k) => drawDove(g, 330, 430, 1.1, t, k));
    S.wait(0.5);
    S.say("colombo", "Bonjour ! Je suis Colombo, la colombe du blason de Colombes.", null, { x: 60, y: 50, w: 640 }, { x: 400, y: 330 });
    S.say("colombo", "Sur le blason, il y a une tour et deux colombes, comme moi !", null, { x: 60, y: 50, w: 640 }, { x: 400, y: 330 });
    S.say("colombo", "Aujourd’hui, on révise les lieux où tu habites, du plus petit au plus grand.", null, { x: 60, y: 50, w: 640 }, { x: 400, y: 330 }, { extra: 0.6 });
  },

  // L'emboîtement
  S => {
    S.bg(g => sky(g, "paper")); colomboNarr(S);
    say(S, "Les lieux s’emboîtent, comme des poupées russes !");
    const lv = [["un continent", "l’Europe", "#d6e8ff"], ["un pays", "la France", "#ffd6d6"], ["une région", "l’Île-de-France", "#d9f5d0"], ["un département", "les Hauts-de-Seine (92)", "#fff0b3"], ["une commune", "Colombes", "#e9dcff"], ["un quartier", "la Petite-Garenne", "#ffffff"]];
    S.show((g, a) => {
      for (let i = 0; i <= 5; i++) {
        const age = a - (5 - i) * 1.3; if (age < 0) continue;
        const x = 250 + i * 32, y = 180 + i * 62, w = 990 - i * 64, h = 420 - i * 62 - i * 6;
        const s = ease(clamp(age / 0.5, 0, 1));
        g.save(); g.globalAlpha = s; g.fillStyle = lv[i][2]; g.lineWidth = 4; g.strokeStyle = INK; rr(g, x, y, w, h, 14); g.fill(); g.stroke(); g.restore();
      }
      for (let i = 0; i < 6; i++) {
        const age = a - (5 - i) * 1.3; if (age < 0.3) continue;
        const x = 250 + i * 32, y = 180 + i * 62;
        txt(g, lv[i][0], x + 18, y + 40, { size: 30, font: FONT_T, align: "left" });
        txt(g, lv[i][1], x + 330, y + 40, { size: 28, align: "left", color: "#2a5bd7", weight: "bold" });
      }
    }, 6 * 1.3 + 0.5);
    say(S, "Du plus petit au plus grand : quartier, commune, département, région, pays, continent.", { extra: 2 });
  },

  // Le quartier
  S => {
    S.bg(g => { sky(g, "day"); ground(g, "#9bd17f", 600); });
    S.actor("deco", g => { house(g, 330, 600, 0.9, "#ffe0c7", "#c2452d"); shop(g, 540, 600, 0.9); house(g, 740, 600, 0.9, "#d6e8ff", "#5a4a8a"); school(g, 1010, 600, 0.9); tree(g, 1210, 600, 0.9); tree(g, 640, 600, 0.6); });
    colomboNarr(S);
    say(S, "Le quartier est une partie de la commune qui a des caractères communs.");
    say(S, "Le quartier de l’école, c’est la Petite-Garenne. C’est un quartier pavillonnaire.");
    say(S, "On y trouve des maisons, quelques commerces et des écoles.", { extra: 1 });
    S.newPage();
    S.bg(g => sky(g, "paper")); colomboNarr(S);
    say(S, "Colombes est découpée en 9 quartiers. Le nôtre, c’est la Petite-Garenne !");
    const q = ["Centre", "Europe", "Fossés-Jean", "Agent-Sarre", "Stade-Arc sportif", "Vallées", "Petite-Garenne", "Grèves-Petit-Colombes", "Victor-Basch"];
    chips(S, q, 270, 200, 3, 300, 90, 26, i => i === 6 ? "#ffd34d" : ["#d6e8ff", "#ffd6d6", "#d9f5d0"][i % 3], 0.5, { size: 25 });
    S.wait(2.5);
  },

  // La commune
  S => {
    S.bg(g => { sky(g, "mint"); ground(g, "#9bd17f", 620); });
    S.actor("deco", g => mairie(g, 860, 620, 1.05));
    colomboNarr(S);
    say(S, "La commune est la plus petite collectivité territoriale.");
    say(S, "Elle est dirigée par le maire et le conseil municipal, élus par les habitants pour 6 ans.", { extra: 0.5 });
    S.newPage();
    S.bg(g => sky(g, "paper")); colomboNarr(S);
    say(S, "Les missions de la commune :");
    chips(S, ["l’état civil", "l’école primaire", "l’eau", "la collecte des déchets", "les bâtiments publics", "les constructions"], 260, 200, 3, 310, 96, 24, "#e9dcff", 0.7, { size: 26 });
    say(S, "Il y a environ 36 000 communes en France.", { extra: 1 });
    S.newPage();
    S.bg(g => sky(g, "paper")); colomboNarr(S);
    S.show((g, a) => {
      chip(g, 270, 230, 440, 150, "#ffd6d6", "", a); chip(g, 780, 230, 440, 150, "#d6e8ff", "", a - 0.6);
      if (a > 0.3) { txt(g, "une ville", 490, 290, { size: 44, font: FONT_T }); txt(g, "au moins 2 000 habitants", 490, 340, { size: 26 }); }
      if (a > 0.9) { txt(g, "un village", 1000, 290, { size: 44, font: FONT_T }); txt(g, "moins de 2 000 habitants", 1000, 340, { size: 26 }); }
      if (a > 1.2) { house(g, 420, 560, 0.7, "#ffe0c7", "#c2452d"); house(g, 500, 560, 0.7, "#d6e8ff", "#5a4a8a"); house(g, 580, 560, 0.7, "#fff0b3", "#2f8f5b"); house(g, 1000, 560, 0.7, "#ffe0c7", "#c2452d"); }
    }, 1.5);
    say(S, "Une ville, c’est une commune d’au moins 2 000 habitants. Avec moins d’habitants, c’est un village.", { extra: 1 });
  },

  // Carte d'identité de Colombes
  S => {
    S.bg((g, t) => { sky(g, "paper"); blason(g, 1165, 400, 0.36, t); }); colomboNarr(S);
    say(S, "Voici la carte d’identité de ma ville, Colombes !");
    const rows = [["Département", "les Hauts-de-Seine (92)"], ["Région", "l’Île-de-France"], ["Code postal", "92700"], ["Habitants", "91 053 : les Colombiens et les Colombiennes"], ["Superficie", "7,81 km²"], ["Paysage", "urbain : des pavillons et des immeubles"]];
    S.show((g, a) => {
      card(g, 245, 180, 840, 420, "#ffffff", a);
      if (a < 0.3) return;
      txt(g, "Carte d’identité de Colombes", 665, 228, { size: 34, font: FONT_T, color: "#2f8f5b" });
      rows.forEach(([k, v], i) => {
        const age = a - 0.5 - i * 0.9; if (age < 0) return;
        g.save(); g.globalAlpha = clamp(age / 0.3, 0, 1);
        txt(g, k + " :", 280, 290 + i * 52, { size: 27, font: FONT_T, align: "left" });
        txt(g, v, 470, 290 + i * 52, { size: 27, align: "left", color: "#2a5bd7", weight: "bold" });
        g.restore();
      });
    }, 0.5 + rows.length * 0.9 + 1);
    say(S, "Colombes est une ville moyenne, dans un paysage urbain.", { extra: 1.5 });
  },

  // Situer Colombes
  S => {
    S.bg(g => sky(g, "paper")); colomboNarr(S);
    say(S, "Les villes limitrophes sont à la frontière de Colombes.");
    const around = [["Argenteuil", -0.55, -1], ["Gennevilliers", 0.95, -0.8], ["Asnières-sur-Seine", 1.15, 0.05], ["Bois-Colombes", 0.85, 0.75], ["La Garenne-Colombes", 0, 1.05], ["Nanterre", -0.95, 0.8], ["Bezons", -1.15, -0.1]];
    S.show((g, a) => {
      const cx = 620, cy = 395;
      chip(g, cx - 120, cy - 45, 240, 90, "#ffd34d", "Colombes", a, { size: 34, font: FONT_T, weight: "" });
      around.forEach(([n, dx, dy], i) => {
        const age = a - 0.6 - i * 0.6; if (age < 0) return;
        const x = cx + dx * 300, y = cy + dy * 150;
        g.save(); g.globalAlpha = clamp(age / 0.3, 0, 1); g.strokeStyle = "#888"; g.lineWidth = 3; g.setLineDash([8, 8]); g.beginPath(); g.moveTo(cx + dx * 120, cy + dy * 45); g.lineTo(x - dx * 40, y - dy * 20); g.stroke(); g.restore();
        g.font = `bold 23px ${FONT_B}`; const w = g.measureText(n).width + 30;
        chip(g, x - w / 2, y - 26, w, 52, "#d6e8ff", n, age, { size: 23 });
      });
      compass(g, 1130, 250, 60);
    }, 0.6 + around.length * 0.6 + 0.6);
    say(S, "Il y en a sept : Argenteuil, Gennevilliers, Asnières-sur-Seine, Bois-Colombes, La Garenne-Colombes, Nanterre et Bezons.", { extra: 1 });
    S.newPage();
    S.bg((g, t) => { sky(g, "paper"); france(g, 330, 190, 40, t); compass(g, 1130, 280, 70); }); colomboNarr(S);
    S.show((g, a) => {
      // zoom : Paris et Colombes
      card(g, 760, 400, 300, 200, "#ffffff", a);
      if (a < 0.3) return;
      g.save(); g.strokeStyle = INK; g.lineWidth = 4; g.beginPath(); g.ellipse(950, 525, 60, 42, 0, 0, 7); g.fillStyle = "#ffd6d6"; g.fill(); g.stroke(); g.restore();
      txt(g, "Paris", 950, 533, { size: 24, font: FONT_T });
      g.fillStyle = "#ffd34d"; g.strokeStyle = INK; g.lineWidth = 4; g.beginPath(); g.arc(835, 445, 14, 0, 7); g.fill(); g.stroke();
      txt(g, "Colombes", 835, 482, { size: 22, font: FONT_T });
      if (a > 1) { g.save(); g.strokeStyle = "#d62839"; g.lineWidth = 5; g.beginPath(); g.moveTo(905, 500); g.lineTo(856, 458); g.stroke(); g.fillStyle = "#d62839"; g.beginPath(); g.moveTo(850, 452); g.lineTo(872, 456); g.lineTo(860, 470); g.closePath(); g.fill(); g.restore(); }
    }, 1.2);
    say(S, "Avec la rose des vents : Colombes est située au nord-ouest de Paris.", { extra: 2 });
  },

  // Le département
  S => {
    S.bg(g => sky(g, "sun")); colomboNarr(S);
    say(S, "Le département est dirigé par le Conseil départemental, sous l’autorité du préfet.");
    say(S, "Ses missions :");
    chips(S, ["les collèges", "les routes et les transports", "l’action sociale et la santé", "la culture et le sport", "la sécurité incendie"], 260, 200, 2, 470, 90, 24, "#fff0b3", 0.7, { size: 27 });
    say(S, "Il y a 101 départements en France. Le nôtre : les Hauts-de-Seine, numéro 92. Son chef-lieu est Nanterre.", { extra: 1.5 });
  },

  // La région et l'Île-de-France
  S => {
    S.bg(g => sky(g, "mint")); colomboNarr(S);
    say(S, "La région est dirigée par le Conseil régional, dont les membres sont élus.");
    say(S, "Ses missions :");
    chips(S, ["les lycées", "les transports régionaux", "les ports et les aéroports", "le développement durable", "l’emploi"], 260, 200, 2, 470, 90, 24, "#d9f5d0", 0.7, { size: 27 });
    say(S, "Il y a 18 régions en France. La nôtre, c’est l’Île-de-France.", { extra: 1 });
    S.newPage();
    S.bg(g => sky(g, "paper")); colomboNarr(S);
    let st = 0;
    S.show((g, a) => {
      const t1 = readTime("L’Île-de-France compte 8 départements. Au centre : Paris, le 75."), t2 = t1 + readTime("Autour de Paris, la petite couronne : 92 Hauts-de-Seine, 93 Seine-Saint-Denis, 94 Val-de-Marne.");
      const lvl = a < t1 ? 0 : a < t2 ? clamp((a - t1) / 1, 0, 1) : 1 + clamp((a - t2) / 1, 0, 1);
      idf(g, 680, 405, lvl, a);
      g.save(); g.globalAlpha = clamp(a - t1 - 0.5, 0, 1); txt(g, "petite couronne", 1030, 300, { size: 28, font: FONT_T, color: "#c2452d", align: "left" }); txt(g, "92 · 93 · 94", 1030, 335, { size: 26, align: "left", weight: "bold" }); g.restore();
      g.save(); g.globalAlpha = clamp(a - t2 - 0.5, 0, 1); txt(g, "grande couronne", 1030, 470, { size: 28, font: FONT_T, color: "#2f8f5b", align: "left" }); txt(g, "77 · 78 · 91 · 95", 1030, 505, { size: 26, align: "left", weight: "bold" }); g.restore();
    });
    void st;
    say(S, "L’Île-de-France compte 8 départements. Au centre : Paris, le 75.");
    say(S, "Autour de Paris, la petite couronne : 92 Hauts-de-Seine, 93 Seine-Saint-Denis, 94 Val-de-Marne.");
    say(S, "Puis la grande couronne : 77 Seine-et-Marne, 78 Yvelines, 91 Essonne, 95 Val-d’Oise.", { extra: 2.5 });
  },

  // Le pays
  S => {
    S.bg((g, t) => { sky(g, "pink"); france(g, 260, 200, 40, t); }); colomboNarr(S);
    S.show((g, a) => {
      const s = pop(clamp(a / 0.5, 0, 1)); g.save(); g.translate(950, 270); g.scale(s, s); frFlag(g, -120, -75, 240, 150); g.restore();
      if (a > 0.6) { txt(g, "Liberté", 950, 400, { size: 38, font: FONT_T, color: "#1f3f9a" }); }
      if (a > 1.2) { txt(g, "Égalité", 950, 448, { size: 38, font: FONT_T, color: "#555" }); }
      if (a > 1.8) { txt(g, "Fraternité", 950, 496, { size: 38, font: FONT_T, color: "#d62839" }); }
    }, 2.2);
    say(S, "Le pays : la France. Sa devise : Liberté, Égalité, Fraternité.");
    say(S, "La France est formée d’une Métropole, de départements et régions d’Outre-Mer (DROM) et de collectivités d’Outre-Mer (COM).", { extra: 0.5 });
    S.newPage();
    S.bg(g => sky(g, "paper")); colomboNarr(S);
    S.actor("urne", (g, t) => ballot(g, 640, 430, 1.6, t));
    say(S, "Notre pays est une République, dirigée par un président élu par le peuple.");
    say(S, "C’est une démocratie : les citoyens participent par le vote.", { extra: 1.5 });
  },

  // Continent et Union européenne
  S => {
    S.bg((g, t) => { sky(g, "lilac"); euFlag(g, 720, 220, 420, 280, t); }); colomboNarr(S);
    say(S, "La France est en Europe. Le continent européen compte 50 pays.");
    say(S, "Certains pays se sont regroupés pour former l’Union européenne, avec 27 pays membres.");
    say(S, "C’est une communauté politique et économique. Voici son drapeau !", { extra: 1.5 });
  },

  // Récapitulatif
  S => {
    S.bg(g => sky(g, "paper")); colomboNarr(S);
    const lv = [["un quartier", "la Petite-Garenne", "maisons, commerces, écoles"], ["une commune", "Colombes", "le maire et le conseil municipal"], ["un département", "les Hauts-de-Seine (92)", "le Conseil départemental"], ["une région", "l’Île-de-France", "le Conseil régional"], ["un pays", "la France", "le président de la République"], ["un continent / une union", "l’Europe / l’UE", "50 pays / 27 pays membres"]];
    say(S, "On récapitule ! Du plus petit au plus grand :");
    S.show((g, a) => lv.forEach(([n, ex, who], i) => {
      const age = a - i * 0.9; if (age < 0) return;
      const y = 180 + i * 70;
      card(g, 260, y, 980, 60, ["#ffffff", "#e9dcff", "#fff0b3", "#d9f5d0", "#ffd6d6", "#d6e8ff"][i], age);
      if (age > 0.2) { txt(g, n, 280, y + 40, { size: 27, font: FONT_T, align: "left" }); txt(g, ex, 640, y + 40, { size: 25, align: "left", weight: "bold", color: "#2a5bd7" }); txt(g, who, 1225, y + 40, { size: 21, align: "right", color: "#444" }); }
    }), lv.length * 0.9 + 1);
    say(S, "Bravo ! Tu connais maintenant tous les lieux où tu habites. À bientôt !", { extra: 3 });
  },
];
