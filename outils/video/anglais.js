/* Vidéo « English with Amy » : bilan d'anglais de la période 1 (CM1). */
"use strict";
const AMY = { skin: "#ffe0c7", hair: "#e3a33b", hairStyle: "pony", shirt: "#e5484d", pants: "#2d3e73", bow: "#2a5bd7", phase: 0 };
const TOM = { skin: "#c98d5e", hair: "#2b1d14", hairStyle: "short", shirt: "#2a7de1", stripe: "#ffd34d", pants: "#454545", phase: 1.3 };

/* positions : deux enfants en grand, ou Amy en narratrice dans le coin */
const BIG = { amy: [260, 650, 0.95], tom: [1030, 650, 0.95] };
const BOX_BIG = { x: 330, y: 60, w: 620 };
const T_AMY = { x: 300, y: 350 }, T_TOM = { x: 990, y: 350 };
const BOX_N = { x: 220, y: 34, w: 860 }, T_N = { x: 170, y: 168 };
function amyBig(S, wave) { S.actor("amy", (g, t, k) => drawKid(g, ...BIG.amy, { ...AMY, wave }, t, k)); }
function tomBig(S, wave) { S.actor("tom", (g, t, k) => drawKid(g, ...BIG.tom, { ...TOM, wave }, t, k)); }
function amyNarr(S) { S.actor("amy", (g, t, k) => drawKid(g, 112, 330, 0.55, AMY, t, k)); }
const sayA = (S, en, fr, o) => S.say("amy", en, fr, BOX_BIG, T_AMY, o);
const sayT = (S, en, fr, o) => S.say("tom", en, fr, BOX_BIG, T_TOM, o);
const sayN = (S, en, fr, o) => S.say("amy", en, fr, BOX_N, T_N, o);

/* ---------- carte schématique du Royaume-Uni ---------- */
const B_EW = [[-2.65,51.6],[-2.7,51.85],[-3.05,52.0],[-3.1,52.3],[-3.0,52.6],[-3.05,52.95],[-2.75,53.0],[-3.0,53.2],[-3.1,53.3]];
const B_ES = [[-3.05,54.98],[-2.7,55.1],[-2.35,55.35],[-2.2,55.45],[-2.35,55.6],[-2.0,55.77]];
const EAST_ENG = [[-2.0,55.77],[-1.43,55.0],[-0.6,54.5],[-0.08,54.12],[0.12,53.6],[0.35,53.15],[0.2,52.9],[0.5,52.95],[1.3,52.93],[1.75,52.48],[1.35,51.95],[1.15,51.79],[0.6,51.5],[1.4,51.38],[1.33,51.13],[0.6,50.85],[-0.14,50.82],[-1.1,50.78],[-1.9,50.7],[-2.45,50.6],[-2.95,50.72],[-3.4,50.6],[-3.65,50.22],[-4.15,50.36],[-5.2,49.96],[-5.71,50.07],[-5.48,50.21],[-4.95,50.55],[-4.53,51.02],[-4.12,51.21],[-3.47,51.21],[-2.98,51.35],[-2.65,51.6]];
const WEST_ENG = [[-3.1,53.3],[-3.05,53.45],[-3.0,53.65],[-3.05,53.82],[-2.9,54.07],[-3.25,54.1],[-3.65,54.5],[-3.57,54.65],[-3.4,54.87],[-3.05,54.98]];
const ENGLAND = EAST_ENG.concat(B_EW.slice(1), WEST_ENG.slice(1), B_ES.slice(1, -1));
const WALES = [[-2.65,51.6],[-2.98,51.55],[-3.17,51.45],[-3.95,51.6],[-4.3,51.56],[-4.7,51.67],[-5.3,51.88],[-4.98,52.0],[-4.65,52.1],[-4.08,52.42],[-4.05,52.72],[-4.7,52.8],[-4.3,53.15],[-4.6,53.3],[-4.4,53.42],[-4.05,53.3],[-3.83,53.33],[-3.5,53.33],[-3.1,53.3]].concat(B_EW.slice().reverse().slice(1, -1));
const SCOTLAND = [[-2.0,55.77],[-2.5,56.0],[-3.2,56.0],[-2.58,56.28],[-2.9,56.45],[-2.47,56.7],[-2.08,57.15],[-1.78,57.5],[-2.0,57.69],[-3.3,57.72],[-3.85,57.6],[-4.2,57.48],[-4.0,57.85],[-3.65,58.1],[-3.1,58.4],[-3.05,58.65],[-4.0,58.55],[-5.0,58.6],[-5.3,58.25],[-5.25,57.9],[-5.7,57.73],[-5.8,57.55],[-5.7,57.28],[-5.83,57.0],[-6.2,56.73],[-5.5,56.42],[-5.5,56.2],[-5.6,55.75],[-5.7,55.3],[-5.4,55.6],[-4.85,55.95],[-4.87,55.8],[-4.63,55.46],[-4.86,55.25],[-5.15,55.0],[-5.05,54.9],[-4.86,54.64],[-4.4,54.68],[-4.05,54.8],[-3.6,54.88],[-3.25,54.97],[-3.05,54.98]].concat(B_ES.slice(1, -1));
const NI_B = [[-6.1,54.03],[-6.27,54.1],[-6.65,54.05],[-7.05,54.2],[-7.4,54.15],[-7.6,54.3],[-8.15,54.45],[-7.9,54.65],[-7.55,54.75],[-7.4,55.0],[-7.25,55.05]];
const NIRL = [[-7.25,55.05],[-6.9,55.17],[-6.15,55.22],[-5.95,54.95],[-5.9,54.65],[-5.45,54.45],[-5.55,54.3],[-5.9,54.2],[-6.1,54.03]].concat(NI_B.slice(1, -1));
const IRL = [[-6.1,54.03],[-6.15,53.35],[-6.0,52.97],[-6.35,52.2],[-7.0,52.13],[-8.3,51.8],[-9.8,51.45],[-10.3,51.9],[-10.45,52.15],[-9.9,52.6],[-9.4,52.95],[-9.05,53.25],[-10.1,53.45],[-10.2,53.95],[-10.0,54.2],[-8.6,54.3],[-8.15,54.6],[-8.8,54.7],[-8.25,55.15],[-7.37,55.38],[-7.25,55.05]].concat(NI_B.slice().reverse().slice(1, -1));
const COUNTRIES = [
  { id: "eng", poly: ENGLAND, en: "England", fr: "l’Angleterre", cap: "London", capFr: "Londres", emb: "rose", embEn: "the rose", embFr: "la rose", color: "#ff8a80", city: [-0.12, 51.5], at: [-1.5, 52.6] },
  { id: "sco", poly: SCOTLAND, en: "Scotland", fr: "l’Écosse", cap: "Edinburgh", capFr: "Édimbourg", emb: "thistle", embEn: "the thistle", embFr: "le chardon", color: "#8fb8ff", city: [-3.19, 55.95], at: [-4.3, 57.1] },
  { id: "wal", poly: WALES, en: "Wales", fr: "le pays de Galles", cap: "Cardiff", capFr: "Cardiff", emb: "leek", embEn: "the leek", embFr: "le poireau", color: "#8ee08e", city: [-3.18, 51.48], at: [-3.75, 52.3] },
  { id: "nir", poly: NIRL, en: "Northern Ireland", fr: "l’Irlande du Nord", cap: "Belfast", capFr: "Belfast", emb: "shamrock", embEn: "the shamrock", embFr: "le trèfle", color: "#ffd166", city: [-5.93, 54.6], at: [-6.7, 54.62] },
];
function drawUK(g, x0, y0, k, hi, t, showAll) {
  const P = ([lon, lat]) => [x0 + (lon + 10.6) * 0.58 * k, y0 + (58.8 - lat) * k];
  const path = (poly) => { g.beginPath(); poly.forEach((p, i) => { const [x, y] = P(p); i ? g.lineTo(x, y) : g.moveTo(x, y); }); g.closePath(); };
  g.save(); g.lineJoin = "round";
  path(IRL); g.fillStyle = "#e9e4d8"; g.fill(); g.lineWidth = 2; g.strokeStyle = "#9a9a9a"; g.stroke();
  for (const c of COUNTRIES) {
    path(c.poly);
    const on = showAll || c.id === hi;
    g.fillStyle = on ? c.color : "#f4f4f4"; g.fill(); g.lineWidth = 3; g.strokeStyle = INK; g.stroke();
  }
  for (const c of COUNTRIES) {
    if (!(showAll || c.id === hi)) continue;
    const [x, y] = P(c.city);
    const r = c.id === hi ? 7 + Math.sin(t * 6) * 2 : 6;
    g.fillStyle = INK; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill();
    g.fillStyle = "#fff"; g.beginPath(); g.arc(x, y, r * 0.45, 0, 7); g.fill();
  }
  g.restore();
}

/* ---------- emblèmes ---------- */
function emblem(g, kind, x, y, s) {
  g.save(); g.translate(x, y); g.scale(s, s); g.lineWidth = 4; g.strokeStyle = INK; g.lineJoin = "round"; g.lineCap = "round";
  if (kind === "rose") {
    g.strokeStyle = "#2f7a2f"; g.lineWidth = 7; g.beginPath(); g.moveTo(0, 10); g.quadraticCurveTo(-8, 60, 0, 95); g.stroke();
    g.fillStyle = "#4caf50"; g.strokeStyle = INK; g.lineWidth = 4; g.beginPath(); g.ellipse(-24, 55, 22, 11, -0.5, 0, 7); g.fill(); g.stroke();
    g.fillStyle = "#e0303a";
    [[-22, -6], [22, -6], [-14, -30], [14, -30], [0, 8]].forEach(([a, b]) => { g.beginPath(); g.arc(a, b - 20, 24, 0, 7); g.fill(); g.stroke(); });
    g.fillStyle = "#c2182a"; g.beginPath(); g.arc(0, -28, 18, 0, 7); g.fill(); g.stroke();
    g.beginPath(); g.arc(0, -28, 8, 0.5, 5); g.stroke();
  } else if (kind === "thistle") {
    g.strokeStyle = "#2f7a2f"; g.lineWidth = 7; g.beginPath(); g.moveTo(0, 10); g.lineTo(0, 95); g.stroke();
    g.strokeStyle = INK; g.lineWidth = 4; g.fillStyle = "#4caf50";
    g.beginPath(); g.moveTo(0, 60); g.lineTo(-40, 40); g.lineTo(-30, 55); g.lineTo(-52, 62); g.lineTo(-28, 70); g.lineTo(0, 75); g.closePath(); g.fill(); g.stroke();
    g.beginPath(); g.moveTo(0, 60); g.lineTo(40, 40); g.lineTo(30, 55); g.lineTo(52, 62); g.lineTo(28, 70); g.lineTo(0, 75); g.closePath(); g.fill(); g.stroke();
    g.fillStyle = "#6fbf5f"; g.beginPath(); g.ellipse(0, 0, 28, 30, 0, 0, 7); g.fill(); g.stroke();
    g.beginPath(); g.moveTo(-20, -12); g.lineTo(20, 18); g.moveTo(20, -12); g.lineTo(-20, 18); g.stroke();
    g.fillStyle = "#9b4dca"; g.beginPath(); g.moveTo(-26, -18); g.lineTo(26, -18); g.lineTo(34, -60); g.lineTo(-34, -60); g.closePath(); g.fill(); g.stroke();
    g.strokeStyle = "#9b4dca"; g.lineWidth = 5;
    for (let i = -3; i <= 3; i++) { g.beginPath(); g.moveTo(i * 9, -58); g.lineTo(i * 13, -82); g.stroke(); }
  } else if (kind === "leek") {
    g.fillStyle = "#3f9b3f";
    [[-0.5, -30], [0, -10], [0.5, -30]].forEach(([r, d]) => { g.save(); g.rotate(r); g.beginPath(); g.ellipse(0, -60 + d / 3, 14, 52, 0, 0, 7); g.fill(); g.stroke(); g.restore(); });
    const gr = g.createLinearGradient(0, -20, 0, 80); gr.addColorStop(0, "#a5d86e"); gr.addColorStop(0.4, "#f4f8e8"); gr.addColorStop(1, "#ffffff");
    g.fillStyle = gr; rr(g, -18, -30, 36, 110, 16); g.fill(); g.stroke();
    g.strokeStyle = "#b08b5a"; g.lineWidth = 3; for (let i = -2; i <= 2; i++) { g.beginPath(); g.moveTo(i * 5, 80); g.lineTo(i * 9, 98); g.stroke(); }
  } else if (kind === "shamrock") {
    g.strokeStyle = "#2f7a2f"; g.lineWidth = 7; g.beginPath(); g.moveTo(0, 10); g.quadraticCurveTo(10, 60, 22, 92); g.stroke();
    g.strokeStyle = INK; g.lineWidth = 4; g.fillStyle = "#2fae4a";
    for (const a of [-Math.PI / 2, Math.PI / 6, Math.PI * 5 / 6]) {
      g.save(); g.rotate(a);
      g.beginPath(); g.arc(30, -11, 17, 0, 7); g.arc(30, 11, 17, 0, 7); g.fill(); g.restore();
    }
    for (const a of [-Math.PI / 2, Math.PI / 6, Math.PI * 5 / 6]) {
      g.save(); g.rotate(a); g.beginPath(); g.arc(30, -11, 17, Math.PI * 0.75, Math.PI * 2.1); g.stroke(); g.beginPath(); g.arc(30, 11, 17, -Math.PI * 0.1, Math.PI * 1.25); g.stroke(); g.restore();
    }
    g.fillStyle = "#2fae4a"; g.beginPath(); g.arc(0, 0, 12, 0, 7); g.fill();
  }
  g.restore();
}

/* ---------- drapeaux ---------- */
function flag(g, kind, x, y, w, h) {
  g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip();
  const sal = (color, lw) => { g.strokeStyle = color; g.lineWidth = lw; g.beginPath(); g.moveTo(x, y); g.lineTo(x + w, y + h); g.moveTo(x + w, y); g.lineTo(x, y + h); g.stroke(); };
  const cross = (color, lw) => { g.fillStyle = color; g.fillRect(x + w / 2 - lw / 2, y, lw, h); g.fillRect(x, y + h / 2 - lw / 2, w, lw); };
  if (kind === "eng") { g.fillStyle = "#fff"; g.fillRect(x, y, w, h); cross("#d62839", h * 0.2); }
  if (kind === "sco") { g.fillStyle = "#1f4fb4"; g.fillRect(x, y, w, h); sal("#fff", h * 0.2); }
  if (kind === "nir") { g.fillStyle = "#fff"; g.fillRect(x, y, w, h); sal("#d62839", h * 0.16); }
  if (kind === "uk") { g.fillStyle = "#1f3f9a"; g.fillRect(x, y, w, h); sal("#fff", h * 0.2); sal("#d62839", h * 0.07); cross("#fff", h * 0.33); cross("#d62839", h * 0.2); }
  if (kind === "fr") { ["#1f3f9a", "#fff", "#d62839"].forEach((c, i) => { g.fillStyle = c; g.fillRect(x + i * w / 3, y, w / 3 + 1, h); }); }
  g.restore();
  g.save(); g.lineWidth = 5; g.strokeStyle = INK; g.strokeRect(x, y, w, h); g.restore();
}

/* ---------- Halloween ---------- */
function spooky(g, kind, x, y, s, t) {
  g.save(); g.translate(x, y); g.scale(s, s); g.lineWidth = 4; g.strokeStyle = INK; g.lineJoin = "round"; g.lineCap = "round";
  const eye = (a, b, r, c = INK) => { g.fillStyle = c; g.beginPath(); g.arc(a, b, r, 0, 7); g.fill(); };
  if (kind === "ghost") {
    g.translate(0, Math.sin(t * 3) * 6);
    g.fillStyle = "#fff"; g.beginPath(); g.moveTo(-40, 50); g.lineTo(-40, -10); g.arc(0, -10, 40, Math.PI, 0); g.lineTo(40, 50);
    for (let i = 0; i < 4; i++) g.quadraticCurveTo(30 - i * 20, 35, 20 - i * 20, 50);
    g.closePath(); g.fill(); g.stroke(); eye(-14, -12, 6); eye(14, -12, 6); g.beginPath(); g.ellipse(0, 12, 8, 11, 0, 0, 7); g.fill();
  } else if (kind === "witch") {
    g.fillStyle = "#8fd18b"; g.beginPath(); g.arc(0, 15, 36, 0, 7); g.fill(); g.stroke();
    g.beginPath(); g.moveTo(-4, 14); g.lineTo(14, 26); g.lineTo(-2, 28); g.stroke(); eye(-12, 6, 5); eye(14, 6, 5);
    g.beginPath(); g.arc(0, 32, 10, 0.3, Math.PI - 0.3); g.stroke();
    g.fillStyle = "#3b2463"; g.beginPath(); g.ellipse(0, -16, 58, 12, 0, 0, 7); g.fill(); g.stroke();
    g.beginPath(); g.moveTo(-30, -18); g.lineTo(10, -82); g.lineTo(30, -18); g.closePath(); g.fill(); g.stroke();
  } else if (kind === "monster") {
    g.fillStyle = "#b07fe0"; g.beginPath(); g.ellipse(0, 10, 44, 50, 0, 0, 7); g.fill(); g.stroke();
    g.fillStyle = "#fff"; g.beginPath(); g.arc(0, -4, 20, 0, 7); g.fill(); g.stroke(); eye(Math.sin(t * 2) * 6, -4, 8);
    g.fillStyle = "#fff"; g.beginPath(); g.moveTo(-18, 30); g.lineTo(18, 30); g.lineTo(10, 42); g.lineTo(2, 30); g.lineTo(-6, 42); g.closePath(); g.fill(); g.stroke();
    g.beginPath(); g.moveTo(-20, -36); g.lineTo(-30, -62); g.moveTo(20, -36); g.lineTo(30, -62); g.stroke();
  } else if (kind === "vampire") {
    g.fillStyle = "#c2182a"; g.beginPath(); g.moveTo(-50, 55); g.lineTo(-30, -6); g.lineTo(30, -6); g.lineTo(50, 55); g.closePath(); g.fill(); g.stroke();
    g.fillStyle = "#f1e6ea"; g.beginPath(); g.arc(0, 0, 32, 0, 7); g.fill(); g.stroke();
    g.fillStyle = INK; g.beginPath(); g.moveTo(-33, -4); g.quadraticCurveTo(-30, -38, 0, -36); g.quadraticCurveTo(30, -38, 33, -4); g.lineTo(0, -18); g.closePath(); g.fill();
    eye(-11, 0, 4); eye(11, 0, 4); g.beginPath(); g.arc(0, 12, 10, 0.2, Math.PI - 0.2); g.stroke();
    g.fillStyle = "#fff"; g.beginPath(); g.moveTo(-6, 20); g.lineTo(-3, 28); g.lineTo(0, 20); g.moveTo(1, 20); g.lineTo(4, 28); g.lineTo(7, 20); g.fill();
  } else if (kind === "skeleton") {
    g.fillStyle = "#fff"; g.beginPath(); g.arc(0, -34, 24, 0, 7); g.fill(); g.stroke(); eye(-9, -36, 6); eye(9, -36, 6);
    g.lineWidth = 6; g.strokeStyle = "#fff";
    const bones = () => { g.beginPath(); g.moveTo(0, -10); g.lineTo(0, 30); for (let i = 0; i < 3; i++) { g.moveTo(-18, -2 + i * 10); g.lineTo(18, -2 + i * 10); } g.moveTo(-26, -4); g.lineTo(-38, 22); g.moveTo(26, -4); g.lineTo(38, 22); g.moveTo(0, 30); g.lineTo(-14, 62); g.moveTo(0, 30); g.lineTo(14, 62); g.stroke(); };
    g.strokeStyle = INK; g.lineWidth = 11; bones(); g.strokeStyle = "#fff"; g.lineWidth = 5; bones();
  } else if (kind === "pumpkin") {
    g.fillStyle = "#f28c28";
    [-26, 26, 0].forEach(a => { g.beginPath(); g.ellipse(a, 10, 30, 42, 0, 0, 7); g.fill(); g.stroke(); });
    g.fillStyle = "#3f7d2a"; rr(g, -6, -46, 12, 18, 4); g.fill(); g.stroke();
    g.fillStyle = "#ffd34d"; g.beginPath(); g.moveTo(-26, -4); g.lineTo(-14, -20); g.lineTo(-4, -4); g.closePath(); g.moveTo(26, -4); g.lineTo(14, -20); g.lineTo(4, -4); g.closePath(); g.fill(); g.stroke();
    g.beginPath(); g.moveTo(-30, 20); g.lineTo(30, 20); g.lineTo(20, 36); g.lineTo(10, 28); g.lineTo(0, 38); g.lineTo(-10, 28); g.lineTo(-20, 36); g.closePath(); g.fill(); g.stroke();
  } else if (kind === "cat") {
    g.fillStyle = "#222"; g.beginPath(); g.ellipse(6, 26, 36, 30, 0, 0, 7); g.fill();
    g.strokeStyle = "#222"; g.lineWidth = 9; g.beginPath(); g.moveTo(38, 36); g.quadraticCurveTo(70, 20, 52, -16); g.stroke();
    g.fillStyle = "#222"; g.beginPath(); g.arc(-18, -12, 26, 0, 7); g.fill();
    g.beginPath(); g.moveTo(-40, -22); g.lineTo(-38, -50); g.lineTo(-24, -34); g.closePath(); g.moveTo(4, -22); g.lineTo(2, -50); g.lineTo(-12, -34); g.closePath(); g.fill();
    eye(-28, -14, 6, "#ffd34d"); eye(-8, -14, 6, "#ffd34d"); eye(-28, -14, 2.5); eye(-8, -14, 2.5);
  } else if (kind === "bat") {
    const f = Math.sin(t * 10) * 10;
    g.fillStyle = "#222"; g.beginPath(); g.moveTo(0, -6); g.lineTo(-30, -20 - f); g.lineTo(-62, -10 - f); g.lineTo(-50, 6); g.lineTo(-38, 0); g.lineTo(-28, 12); g.lineTo(-14, 6); g.lineTo(0, 16);
    g.lineTo(14, 6); g.lineTo(28, 12); g.lineTo(38, 0); g.lineTo(50, 6); g.lineTo(62, -10 - f); g.lineTo(30, -20 - f); g.closePath(); g.fill();
    g.beginPath(); g.ellipse(0, 2, 12, 16, 0, 0, 7); g.fill(); g.beginPath(); g.moveTo(-8, -10); g.lineTo(-10, -24); g.lineTo(-2, -12); g.moveTo(8, -10); g.lineTo(10, -24); g.lineTo(2, -12); g.fill();
    eye(-5, -2, 3, "#ffd34d"); eye(5, -2, 3, "#ffd34d");
  } else if (kind === "spider") {
    const dy = Math.sin(t * 2) * 8;
    g.strokeStyle = "#888"; g.lineWidth = 2; g.beginPath(); g.moveTo(0, -70); g.lineTo(0, -10 + dy); g.stroke();
    g.translate(0, dy); g.strokeStyle = "#222"; g.lineWidth = 5;
    for (let i = 0; i < 4; i++) { const yy = -2 + i * 9; g.beginPath(); g.moveTo(-14, yy); g.lineTo(-40, yy - 14 + i * 4); g.lineTo(-50, yy + 10); g.moveTo(14, yy); g.lineTo(40, yy - 14 + i * 4); g.lineTo(50, yy + 10); g.stroke(); }
    g.fillStyle = "#222"; g.beginPath(); g.arc(0, 16, 22, 0, 7); g.fill(); g.beginPath(); g.arc(0, -8, 14, 0, 7); g.fill();
    eye(-5, -10, 4, "#fff"); eye(5, -10, 4, "#fff"); eye(-5, -10, 1.6); eye(5, -10, 1.6);
  } else if (kind === "hat") {
    g.fillStyle = "#3b2463"; g.beginPath(); g.ellipse(0, 36, 62, 14, 0, 0, 7); g.fill(); g.stroke();
    g.beginPath(); g.moveTo(-34, 34); g.quadraticCurveTo(-10, -20, 6, -56); g.quadraticCurveTo(24, -50, 40, -40); g.quadraticCurveTo(20, -30, 34, 34); g.closePath(); g.fill(); g.stroke();
    g.fillStyle = "#f2a900"; g.fillRect(-30, 16, 62, 12); g.strokeRect(-30, 16, 62, 12); g.fillStyle = "#3b2463"; g.fillRect(-4, 18, 10, 8);
  } else if (kind === "house") {
    g.fillStyle = "#4a3b6b"; g.fillRect(-46, -10, 70, 66); g.strokeRect(-46, -10, 70, 66);
    g.beginPath(); g.moveTo(-54, -8); g.lineTo(-11, -48); g.lineTo(32, -8); g.closePath(); g.fill(); g.stroke();
    g.fillRect(24, -36, 28, 92); g.strokeRect(24, -36, 28, 92); g.beginPath(); g.moveTo(20, -34); g.lineTo(38, -70); g.lineTo(56, -34); g.closePath(); g.fill(); g.stroke();
    g.fillStyle = (Math.floor(t * 2) % 2) ? "#ffe066" : "#ffd34d";
    [[-36, 4], [-8, 4], [30, -20], [30, 10]].forEach(([a, b]) => { g.fillRect(a, b, 14, 16); g.strokeRect(a, b, 14, 16); });
    g.fillStyle = "#2a1f3d"; g.fillRect(-26, 30, 18, 26); g.strokeRect(-26, 30, 18, 26);
  }
  g.restore();
}
function splat(g, x, y, r, color, seed) {
  g.save(); g.translate(x, y); g.fillStyle = color; g.strokeStyle = INK; g.lineWidth = 4; g.beginPath();
  const n = 11;
  for (let i = 0; i <= n * 2; i++) {
    const a = (i / (n * 2)) * Math.PI * 2, k = i % 2 ? 0.62 : 1 + ((Math.sin(seed * 7 + i * 3.1) + 1) / 2) * 0.35;
    const xx = Math.cos(a) * r * k, yy = Math.sin(a) * r * k;
    i ? g.lineTo(xx, yy) : g.moveTo(xx, yy);
  }
  g.closePath(); g.fill(); g.stroke(); g.restore();
}

/* ---------- les scènes ---------- */
const SCENES = [
  // Titre
  S => { S.bg((g, t) => titleCard(g, t, "English with Amy", "Bilan d’anglais · Période 1 · CM1", "#2a5bd7")); S.wait(3.6); },

  // Se présenter
  S => {
    S.bg(g => { sky(g, "day"); ground(g); });
    amyBig(S, true); tomBig(S, false);
    S.wait(0.6);
    sayA(S, "Hello! My name is Amy.", "Bonjour ! Je m’appelle Amy.");
    sayA(S, "I’m ten years old.", "J’ai dix ans.");
    sayA(S, "My favourite colour is red.", "Ma couleur préférée est le rouge.");
    sayT(S, "Hello Amy! My name is Tom.", "Bonjour Amy ! Je m’appelle Tom.");
    sayT(S, "I’m nine years old. My favourite colour is blue.", "J’ai neuf ans. Ma couleur préférée est le bleu.");
    S.newPage();
    S.bg(g => sky(g, "mint")); amyNarr(S);
    sayN(S, "To introduce yourself, say three sentences.", "Pour te présenter, dis trois phrases.");
    const lines = [["My name is …", "Je m’appelle …"], ["I’m … years old.", "J’ai … ans."], ["My favourite colour is …", "Ma couleur préférée est …"]];
    lines.forEach((l, i) => S.show((g, a) => {
      card(g, 300, 210 + i * 120, 860, 96, ["#ffd6d6", "#d6e8ff", "#d9f5d0"][i], a);
      if (a > 0.2) { txt(g, l[0], 330, 268 + i * 120, { size: 44, font: FONT_T, align: "left" }); txt(g, l[1], 1130, 268 + i * 120, { size: 26, align: "right", color: "#555" }); }
    }, 1.4));
    sayN(S, "Now it’s your turn!", "À ton tour !", { extra: 2 });
  },

  // Le Royaume-Uni
  S => {
    S.bg(g => sky(g, "day")); amyNarr(S);
    S.show((g, a) => { g.save(); g.globalAlpha = clamp(a / 0.6, 0, 1); drawUK(g, 300, 196, 44, null, a, true); g.restore(); });
    sayN(S, "I live in London, in the United Kingdom.", "J’habite à Londres, au Royaume-Uni.");
    sayN(S, "The United Kingdom has four countries.", "Le Royaume-Uni est formé de quatre pays.");
    COUNTRIES.forEach(c => {
      S.newPage();
      S.bg((g, t) => { sky(g, "day"); drawUK(g, 300, 196, 44, c.id, t, false);
        const P = ([lon, lat]) => [300 + (lon + 10.6) * 0.58 * 44, 196 + (58.8 - lat) * 44];
        const [x, y] = P(c.at); txt(g, c.en, x, y, { size: 26, font: FONT_T, color: "#fff", stroke: INK, strokeW: 7 }); });
      amyNarr(S);
      S.show((g, a) => {
        card(g, 700, 200, 520, 380, "#ffffff", a);
        if (a < 0.3) return;
        g.save(); g.fillStyle = c.color; rr(g, 700, 200, 520, 84, 16); g.fill(); g.lineWidth = 5; g.strokeStyle = INK; g.stroke(); g.restore();
        txt(g, c.en, 960, 258, { size: 50, font: FONT_T, color: "#fff", stroke: INK, strokeW: 9 });
        txt(g, "(" + c.fr + ")", 960, 318, { size: 26, color: "#555" });
        txt(g, "Capital: " + c.cap, 730, 380, { size: 34, font: FONT_T, align: "left" });
        txt(g, "Emblem:", 730, 440, { size: 34, font: FONT_T, align: "left" });
        txt(g, c.embEn, 730, 482, { size: 30, align: "left" }); txt(g, "(" + c.embFr + ")", 730, 520, { size: 26, align: "left", color: "#555" });
        emblem(g, c.emb, 1110, 470, 0.95);
      });
      sayN(S, `${c.en}! The capital is ${c.cap}. The emblem is ${c.embEn}.`, `${c.fr[0].toUpperCase() + c.fr.slice(1)} ! Sa capitale est ${c.capFr}. Son emblème est ${c.embFr}.`, { extra: 1.2 });
    });
  },

  // Les drapeaux
  S => {
    S.bg(g => sky(g, "lilac")); amyNarr(S);
    const fl = [["eng", 300, 185, "England", "croix de saint Georges"], ["sco", 610, 185, "Scotland", "croix de saint André"], ["nir", 920, 185, "Northern Ireland", "croix de saint Patrick"]];
    sayN(S, "Look at the flags!", "Regarde les drapeaux !");
    fl.forEach(([k, x, y, en, fr], i) => S.show((g, a) => {
      const s = pop(clamp(a / 0.4, 0, 1)); g.save(); g.translate(x + 120, y + 75); g.scale(s, s); flag(g, k, -120, -75, 240, 150); g.restore();
      if (a > 0.3) { txt(g, en, x + 120, y + 190, { size: 28, font: FONT_T }); txt(g, fr, x + 120, y + 222, { size: 22, color: "#555" }); }
      if (i < 2 && a > 0.3) txt(g, "+", x + 275, y + 95, { size: 70, font: FONT_T });
    }, 1.2));
    S.show((g, a) => {
      if (a > 0.1) txt(g, "=", 650, 495, { size: 70, font: FONT_T });
      const s = pop(clamp((a - 0.3) / 0.5, 0, 1)); g.save(); g.translate(880, 475); g.scale(s, s); flag(g, "uk", -115, -70, 230, 140); g.restore();
      if (a > 0.8) txt(g, "the Union Jack", 1150, 485, { size: 30, font: FONT_T });
    });
    sayN(S, "Together, they make the Union Jack: the flag of the United Kingdom.", "Ensemble, ils forment l’Union Jack : le drapeau du Royaume-Uni (pas seulement de l’Angleterre !).", { extra: 1 });
    sayN(S, "The Welsh flag has a red dragon. It is not in the Union Jack.", "Le drapeau du pays de Galles a un dragon rouge. Il n’apparaît pas dans l’Union Jack.", { extra: 1 });
  },

  // Les nombres
  S => {
    S.bg(g => { sky(g, "sun"); ground(g, "#f2c46d"); });
    amyBig(S, false); tomBig(S, false); S.wait(0.4);
    sayT(S, "How old are you, Amy?", "Quel âge as-tu, Amy ?");
    sayA(S, "I’m ten years old!", "J’ai dix ans !");
    S.newPage();
    S.bg(g => sky(g, "paper")); amyNarr(S);
    sayN(S, "Let’s count from nought to twenty!", "Comptons de zéro à vingt !");
    const words = ["nought","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty"];
    const st = S.c;
    S.show((g, a) => {
      words.forEach((w, n) => {
        const age = a - n * 0.75; if (age < 0) return;
        const col = Math.floor(n / 7), row = n % 7, x = 290 + col * 320, y = 205 + row * 56;
        const s = pop(clamp(age / 0.3, 0, 1));
        g.save(); g.translate(x, y); g.scale(s, s);
        g.fillStyle = n >= 13 && n <= 19 ? "#ffd34d" : "#fff"; g.strokeStyle = INK; g.lineWidth = 4; g.beginPath(); g.arc(0, 0, 24, 0, 7); g.fill(); g.stroke();
        txt(g, String(n), 0, 10, { size: 26, font: FONT_T });
        if (n >= 13 && n <= 19) { const base = w.slice(0, -4); txt(g, base, 40, 11, { size: 32, align: "left" }); g.font = `32px ${FONT_B}`; const wd = g.measureText(base).width; txt(g, "teen", 40 + wd, 11, { size: 32, align: "left", color: "#d62839", weight: "bold" }); }
        else txt(g, w, 40, 11, { size: 32, align: "left" });
        g.restore();
      });
    }, words.length * 0.75 + 1);
    sayN(S, "From 13 to 19, the numbers end with “teen”.", "De 13 à 19, les nombres se terminent par « teen ».", { extra: 2 });
    void st;
  },

  // Les jours
  S => {
    S.bg(g => { sky(g, "pink"); ground(g, "#9bd17f"); });
    amyBig(S, false); tomBig(S, true); S.wait(0.4);
    sayA(S, "What’s the day today?", "Quel jour sommes-nous ?");
    sayT(S, "It’s Monday!", "C’est lundi !");
    S.newPage();
    S.bg(g => sky(g, "paper")); amyNarr(S);
    const days = [["Monday", "lundi"], ["Tuesday", "mardi"], ["Wednesday", "mercredi"], ["Thursday", "jeudi"], ["Friday", "vendredi"], ["Saturday", "samedi"], ["Sunday", "dimanche"]];
    sayN(S, "There are seven days in a week.", "Il y a sept jours dans une semaine.");
    S.show((g, a) => {
      days.forEach(([en, fr], i) => {
        const age = a - i * 0.7; if (age < 0) return;
        const we = i >= 5, x = we ? 330 + (i - 5) * 300 : 240 + i * 200, y = we ? 400 : 210, w = we ? 270 : 188;
        card(g, x, y, w, 120, we ? "#ffd34d" : "#cfe3ff", age, { tilt: i % 2 ? 0.04 : -0.04 });
        if (age > 0.2) { txt(g, en, x + w / 2, y + 58, { size: we ? 36 : 30, font: FONT_T }); txt(g, fr, x + w / 2, y + 96, { size: 24, color: "#555" }); }
      });
      if (a > 5.4) { txt(g, "the week-end", 1080, 462, { size: 32, font: FONT_T, color: "#d62839" }); txt(g, "le week-end", 1080, 496, { size: 24, color: "#555" }); }
    }, 6.2);
    sayN(S, "Saturday and Sunday are the week-end.", "Samedi et dimanche, c’est le week-end.");
    sayN(S, "In English, days always start with a capital letter: Monday.", "En anglais, les jours commencent toujours par une majuscule : Monday.", { extra: 1 });
    S.newPage();
    S.bg(g => sky(g, "paper")); amyNarr(S);
    const yt = [["Yesterday", "hier", "Sunday"], ["Today", "aujourd’hui", "Monday"], ["Tomorrow", "demain", "Tuesday"]];
    S.show((g, a) => {
      yt.forEach(([h, fr, d], i) => {
        const age = a - i * 0.6; if (age < 0) return;
        const x = 270 + i * 330;
        card(g, x, 240, 290, 240, i === 1 ? "#ffd34d" : "#ffffff", age);
        if (age > 0.2) { txt(g, h, x + 145, 300, { size: 40, font: FONT_T, color: "#2a5bd7" }); txt(g, fr, x + 145, 336, { size: 24, color: "#555" }); txt(g, d, x + 145, 430, { size: 44, font: FONT_T }); }
        if (i < 2 && age > 0.3) txt(g, "→", x + 310, 380, { size: 50, font: FONT_T });
      });
    }, 2);
    sayN(S, "Today is Monday. Yesterday was Sunday. Tomorrow is Tuesday.", "Aujourd’hui, c’est lundi. Hier, c’était dimanche. Demain, c’est mardi.", { extra: 1.5 });
  },

  // Les couleurs
  S => {
    S.bg(g => sky(g, "paper")); amyNarr(S);
    const cols = [["red", "rouge", "#e0303a"], ["blue", "bleu", "#2a5bd7"], ["green", "vert", "#2fae4a"], ["yellow", "jaune", "#ffd21f"], ["orange", "orange", "#f28c28"],
      ["pink", "rose", "#ff7fb6"], ["purple", "violet", "#7b3fc6"], ["brown", "marron", "#8a5a36"], ["black", "noir", "#222222"], ["white", "blanc", "#ffffff"],
      ["grey", "gris", "#9aa0a6"], ["light blue", "bleu clair", "#7cc7ff"], ["dark blue", "bleu foncé", "#1d2f8a"]];
    sayN(S, "What colour is it?", "De quelle couleur est-ce ?");
    S.show((g, a) => {
      cols.forEach(([en, fr, c], i) => {
        const age = a - i * 0.85; if (age < 0) return;
        const row = Math.floor(i / 5), col = i % 5, x = 330 + col * 200 + (row === 2 ? 200 : 0), y = 225 + row * 140;
        const s = pop(clamp(age / 0.35, 0, 1));
        g.save(); g.translate(x, y); g.scale(s, s); splat(g, 0, -14, 30, c, i); g.restore();
        if (age > 0.25) { txt(g, "It’s " + en + ".", x, y + 50, { size: 26, font: FONT_T }); txt(g, fr, x, y + 76, { size: 20, color: "#555" }); }
      });
    }, cols.length * 0.85 + 1.5);
    sayN(S, "My favourite colour is red. And you?", "Ma couleur préférée est le rouge. Et toi ?", { extra: 1.5 });
  },

  // Halloween
  S => {
    S.bg(g => { sky(g, "night"); g.fillStyle = "#fff6c9"; g.beginPath(); g.arc(1120, 120, 60, 0, 7); g.fill(); g.fillStyle = "#1d1f4a"; g.beginPath(); g.arc(1100, 105, 56, 0, 7); g.fill(); ground(g, "#3b2f5c"); });
    amyBig(S, true); tomBig(S, false);
    S.actor("deco", (g, t) => { spooky(g, "hat", 260, 340, 0.9, t); spooky(g, "pumpkin", 640, 560, 1.1, t); spooky(g, "bat", 650, 200, 1, t); });
    S.wait(0.4);
    sayA(S, "Happy Halloween!", "Joyeux Halloween !");
    sayT(S, "Trick or treat!", "Des bonbons ou un sort !");
    S.newPage();
    S.bg(g => sky(g, "night")); amyNarr(S);
    const items = [["ghost", "a ghost", "un fantôme"], ["witch", "a witch", "une sorcière"], ["monster", "a monster", "un monstre"], ["vampire", "a vampire", "un vampire"],
      ["skeleton", "a skeleton", "un squelette"], ["pumpkin", "a pumpkin", "une citrouille"], ["cat", "a black cat", "un chat noir"], ["bat", "a bat", "une chauve-souris"],
      ["spider", "a spider", "une araignée"], ["hat", "a hat", "un chapeau"], ["house", "a haunted house", "une maison hantée"]];
    sayN(S, "Here are the Halloween words.", "Voici les mots d’Halloween.");
    S.show((g, a) => {
      items.forEach(([k, en, fr], i) => {
        const age = a - i * 1.1; if (age < 0) return;
        const row = Math.floor(i / 4), col = i % 4, x = 340 + col * 240 + (row === 2 ? 120 : 0), y = 255 + row * 150;
        const s = pop(clamp(age / 0.35, 0, 1));
        g.save(); g.fillStyle = "rgba(255,255,255,.12)"; rr(g, x - 105, y - 70, 210, 140, 16); g.fill(); g.restore();
        g.save(); g.translate(x, y - 14); g.scale(s, s); spooky(g, k, 0, 0, 0.62, a); g.restore();
        if (age > 0.25) { txt(g, en, x, y + 44, { size: 25, font: FONT_T, color: "#ffd34d" }); txt(g, fr, x, y + 66, { size: 19, color: "#e6e0ff" }); }
      });
    }, items.length * 1.1 + 2);
    sayN(S, "Boo! Did you remember them all?", "Bouh ! Tu t’en souviens de tous ?", { extra: 1.5 });
  },

  // Fin
  S => {
    S.bg(g => { sky(g, "day"); ground(g); });
    amyBig(S, true); tomBig(S, true); S.wait(0.4);
    sayA(S, "Well done! Goodbye, see you soon!", "Bravo ! Au revoir, à bientôt !");
    sayT(S, "Bye-bye!", "Salut !");
    S.newPage();
    S.bg((g, t) => titleCard(g, t, "The end", "Révise bien : UK · Introduce yourself · Numbers · Days · Colours · Halloween", "#2a5bd7"));
    S.wait(4);
  },
];
