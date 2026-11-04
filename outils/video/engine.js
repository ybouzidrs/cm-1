/* Moteur de bande dessinée animée : chaque image est dessinée sur un canvas à partir du temps t.
   Une scène est une fonction qui reçoit un « studio » S. Elle est exécutée deux fois :
   une fois pour mesurer le minutage, puis à chaque image pour dessiner. */
"use strict";
const W = 1280, H = 720;
const FONT_T = '"Lilita One", "Arial Rounded MT Bold", sans-serif';
const FONT_B = '"Andika", "Verdana", sans-serif';
const INK = "#1b1b24";

/* ---------- outils ---------- */
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const ease = (x) => { x = clamp(x, 0, 1); return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; };
const pop = (x) => { x = clamp(x, 0, 1); const c = 1.70158 * 1.3; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;

function rr(g, x, y, w, h, r) {
  g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r);
  g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath();
}
function wrap(g, text, maxW) {
  const words = text.split(" "), lines = []; let line = "";
  for (const w of words) {
    const t = line ? line + " " + w : w;
    if (g.measureText(t).width > maxW && line) { lines.push(line); line = w; } else line = t;
  }
  if (line) lines.push(line);
  return lines;
}
function txt(g, s, x, y, o = {}) {
  g.save();
  g.font = `${o.weight || ""} ${o.size || 30}px ${o.font || FONT_B}`;
  g.fillStyle = o.color || INK; g.textAlign = o.align || "center"; g.textBaseline = o.base || "alphabetic";
  if (o.stroke) { g.lineWidth = o.strokeW || 8; g.strokeStyle = o.stroke; g.lineJoin = "round"; g.strokeText(s, x, y); }
  g.fillText(s, x, y);
  g.restore();
}
/* temps de lecture pour un enfant de CM1 */
function readTime(text, fr) { return 1.6 + 0.062 * text.length + 0.05 * (fr ? fr.length : 0); }

/* ---------- décors ---------- */
function halftone(g, color, dot, step) {
  g.save(); g.fillStyle = color;
  for (let y = 0; y < H; y += step) for (let x = (y / step) % 2 ? step / 2 : 0; x < W; x += step) { g.beginPath(); g.arc(x, y, dot, 0, 7); g.fill(); }
  g.restore();
}
function panelFrame(g) {
  g.save(); g.lineWidth = 10; g.strokeStyle = INK; rr(g, 14, 14, W - 28, H - 28, 18); g.stroke(); g.restore();
  g.save(); g.fillStyle = "#fff8e8"; g.beginPath(); g.rect(0, 0, W, H);
  const x = 14, y = 14, w = W - 28, h = H - 28, r = 18;
  g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath();
  g.fill("evenodd"); g.restore();
  g.save(); g.lineWidth = 10; g.strokeStyle = INK; rr(g, 14, 14, W - 28, H - 28, 18); g.stroke(); g.restore();
}
const SKIES = {
  day: ["#8fd3ff", "#d9f1ff", "rgba(255,255,255,.35)"],
  sun: ["#ffd36b", "#fff3c4", "rgba(255,255,255,.4)"],
  mint: ["#9fe3c9", "#e6fbf2", "rgba(255,255,255,.4)"],
  pink: ["#ffb4c8", "#ffe6ee", "rgba(255,255,255,.4)"],
  lilac: ["#c8b6ff", "#efe9ff", "rgba(255,255,255,.4)"],
  night: ["#1d1f4a", "#46307a", "rgba(255,255,255,.08)"],
  paper: ["#fff8e8", "#fff8e8", "rgba(0,0,0,.05)"],
};
function sky(g, name) {
  const [a, b, d] = SKIES[name] || SKIES.day;
  const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, a); gr.addColorStop(1, b);
  g.fillStyle = gr; g.fillRect(0, 0, W, H);
  halftone(g, d, 3, 22);
}
function ground(g, color = "#7fcf6b", y = 610) {
  g.save(); g.fillStyle = color; g.beginPath(); g.moveTo(0, y);
  for (let x = 0; x <= W; x += 80) g.quadraticCurveTo(x + 40, y - 14, x + 80, y);
  g.lineTo(W, H); g.lineTo(0, H); g.closePath(); g.fill(); g.lineWidth = 5; g.strokeStyle = INK; g.stroke(); g.restore();
}

/* ---------- personnages ---------- */
function drawKid(g, x, y, s, o, t, talk) {
  g.save(); g.translate(x, y); g.scale(s, s);
  g.lineWidth = 5; g.strokeStyle = INK; g.lineJoin = "round"; g.lineCap = "round";
  const bob = Math.sin(t * 2.2 + (o.phase || 0)) * 3;
  // jambes
  g.fillStyle = o.pants || "#3a4a7a";
  rr(g, -38, -70, 30, 72, 10); g.fill(); g.stroke(); rr(g, 8, -70, 30, 72, 10); g.fill(); g.stroke();
  g.fillStyle = INK; rr(g, -44, -6, 40, 16, 8); g.fill(); rr(g, 6, -6, 40, 16, 8); g.fill();
  g.translate(0, bob);
  // bras
  const wave = o.wave ? Math.sin(t * 7) * 0.5 - 0.9 : 0.25;
  g.fillStyle = o.skin;
  g.save(); g.translate(-48, -150); g.rotate(0.25); rr(g, -12, 0, 24, 82, 12); g.fillStyle = o.shirt; g.fill(); g.stroke();
  g.beginPath(); g.arc(0, 88, 14, 0, 7); g.fillStyle = o.skin; g.fill(); g.stroke(); g.restore();
  g.save(); g.translate(48, -150); g.rotate(-wave); rr(g, -12, 0, 24, 82, 12); g.fillStyle = o.shirt; g.fill(); g.stroke();
  g.beginPath(); g.arc(0, 88, 14, 0, 7); g.fillStyle = o.skin; g.fill(); g.stroke(); g.restore();
  // corps
  g.fillStyle = o.shirt; rr(g, -52, -162, 104, 100, 26); g.fill(); g.stroke();
  if (o.stripe) { g.fillStyle = o.stripe; g.fillRect(-50, -120, 100, 14); g.strokeRect(-50, -120, 100, 14); }
  // tête
  g.fillStyle = o.skin; g.beginPath(); g.arc(0, -225, 62, 0, 7); g.fill(); g.stroke();
  // cheveux
  g.fillStyle = o.hair;
  if (o.hairStyle === "pony") {
    g.beginPath(); g.arc(0, -238, 64, Math.PI * 1.02, Math.PI * 1.98); g.quadraticCurveTo(30, -250, -64, -232); g.fill(); g.stroke();
    g.beginPath(); g.ellipse(62, -250, 20, 34, 0.5, 0, 7); g.fill(); g.stroke();
    g.fillStyle = o.bow || "#e5484d"; g.beginPath(); g.arc(46, -280, 12, 0, 7); g.fill(); g.stroke();
  } else if (o.hairStyle === "curly") {
    for (let i = 0; i < 9; i++) { const a = Math.PI * (1.05 + i * 0.11); g.beginPath(); g.arc(Math.cos(a) * 58, -228 + Math.sin(a) * 58, 20, 0, 7); g.fill(); g.stroke(); }
  } else {
    g.beginPath(); g.moveTo(-64, -230); g.quadraticCurveTo(-60, -300, 0, -292); g.quadraticCurveTo(62, -300, 64, -228);
    g.quadraticCurveTo(30, -262, -10, -255); g.quadraticCurveTo(-40, -250, -64, -230); g.fill(); g.stroke();
  }
  // visage
  const blink = (t % 3.7) < 0.12;
  g.fillStyle = INK;
  if (blink) { g.beginPath(); g.moveTo(-30, -228); g.lineTo(-14, -228); g.moveTo(14, -228); g.lineTo(30, -228); g.stroke(); }
  else { g.beginPath(); g.arc(-22, -228, 7, 0, 7); g.arc(22, -228, 7, 0, 7); g.fill(); }
  g.fillStyle = "rgba(255,120,120,.45)"; g.beginPath(); g.arc(-38, -205, 10, 0, 7); g.arc(38, -205, 10, 0, 7); g.fill();
  const open = talk ? (Math.sin(t * 18) + 1) / 2 : 0;
  g.fillStyle = "#8a2b2b";
  if (open > 0.15) { g.beginPath(); g.ellipse(0, -196, 14, 4 + open * 10, 0, 0, 7); g.fill(); g.stroke(); }
  else { g.beginPath(); g.arc(0, -205, 16, 0.2, Math.PI - 0.2); g.stroke(); }
  g.restore();
}
function drawDove(g, x, y, s, t, talk) {
  g.save(); g.translate(x, y + Math.sin(t * 2.4) * 8); g.scale(s, s);
  g.lineWidth = 5; g.strokeStyle = INK; g.lineJoin = "round"; g.lineCap = "round";
  // queue
  g.fillStyle = "#ffffff"; g.beginPath(); g.moveTo(-70, 10); g.lineTo(-150, -10); g.lineTo(-150, 40); g.closePath(); g.fill(); g.stroke();
  // corps
  g.beginPath(); g.ellipse(0, 10, 90, 58, -0.1, 0, 7); g.fill(); g.stroke();
  // aile qui bat
  const f = Math.sin(t * 9) * 0.6;
  g.save(); g.translate(-10, -10); g.rotate(-0.4 + f);
  g.beginPath(); g.ellipse(-40, -40, 80, 34, -0.4, 0, 7); g.fillStyle = "#f2f2f7"; g.fill(); g.stroke();
  g.beginPath(); g.moveTo(-100, -20); g.lineTo(-60, -30); g.moveTo(-90, -2); g.lineTo(-50, -18); g.stroke(); g.restore();
  // tête
  g.fillStyle = "#ffffff"; g.beginPath(); g.arc(78, -40, 40, 0, 7); g.fill(); g.stroke();
  const open = talk ? (Math.sin(t * 18) + 1) / 2 * 0.5 : 0;
  g.fillStyle = "#f4a51c"; g.beginPath(); g.moveTo(112, -48); g.lineTo(150, -38 - open * 8); g.lineTo(114, -30); g.closePath(); g.fill(); g.stroke();
  if (open > 0.05) { g.beginPath(); g.moveTo(114, -30); g.lineTo(146, -28 + open * 10); g.lineTo(112, -24); g.closePath(); g.fill(); g.stroke(); }
  g.fillStyle = INK; g.beginPath(); g.arc(88, -50, 7, 0, 7); g.fill();
  g.fillStyle = "#fff"; g.beginPath(); g.arc(90, -52, 2.5, 0, 7); g.fill();
  g.fillStyle = "rgba(255,120,150,.5)"; g.beginPath(); g.arc(70, -28, 8, 0, 7); g.fill();
  // pattes
  g.beginPath(); g.moveTo(-10, 66); g.lineTo(-14, 92); g.moveTo(20, 66); g.lineTo(24, 92); g.stroke();
  g.restore();
}

/* ---------- bulles ---------- */
function bubble(g, text, fr, box, tail, age, o = {}) {
  const typed = clamp(age * 32, 0, text.length), shown = text.slice(0, Math.ceil(typed));
  const a = clamp(age / 0.18, 0, 1), sc = lerp(0.85, 1, pop(a));
  g.save(); g.globalAlpha = a;
  g.font = `${o.size || 34}px ${FONT_B}`;
  const lines = wrap(g, text, box.w - 50), lh = (o.size || 34) * 1.25, hgt = lines.length * lh + 34;
  const bx = box.x, by = box.y, cx = bx + box.w / 2, cy = by + hgt / 2;
  g.translate(cx, cy); g.scale(sc, sc); g.translate(-cx, -cy);
  g.lineWidth = 5; g.strokeStyle = INK; g.fillStyle = o.fill || "#ffffff"; g.lineJoin = "round";
  rr(g, bx, by, box.w, hgt, 26); g.fill(); g.stroke();
  if (tail) {
    const mx = clamp(tail.x, bx + 50, bx + box.w - 50), my = tail.y > by ? by + hgt : by;
    g.beginPath(); g.moveTo(mx - 22, my - (tail.y > by ? 3 : -3)); g.lineTo(tail.x, tail.y); g.lineTo(mx + 22, my - (tail.y > by ? 3 : -3));
    g.fill(); g.stroke(); g.fillRect(mx - 20, tail.y > by ? my - 7 : my + 1, 40, 6);
  }
  g.fillStyle = INK; g.textAlign = "left"; g.textBaseline = "top";
  let left = shown.length;
  lines.forEach((ln, i) => { const part = ln.slice(0, Math.max(0, left)); left -= ln.length + 1; g.fillText(part, bx + 25, by + 18 + i * lh); });
  g.restore();
  if (fr && age > text.length / 32 + 0.25) {
    const b = clamp((age - text.length / 32 - 0.25) / 0.3, 0, 1);
    caption(g, fr, b);
  }
  return hgt;
}
function caption(g, fr, alpha) {
  g.save(); g.globalAlpha = alpha; g.font = `italic 27px ${FONT_B}`;
  const lines = wrap(g, fr, 980), lh = 34, hgt = lines.length * lh + 22, y = H - 40 - hgt;
  g.fillStyle = "#fff3a6"; g.strokeStyle = INK; g.lineWidth = 4; rr(g, 140, y, W - 280, hgt, 12); g.fill(); g.stroke();
  g.fillStyle = "#2a5bd7"; g.font = `bold 18px ${FONT_B}`; g.textAlign = "left"; g.fillText("EN FRANÇAIS", 160, y - 8);
  g.fillStyle = INK; g.font = `italic 27px ${FONT_B}`; g.textAlign = "center"; g.textBaseline = "top";
  lines.forEach((l, i) => g.fillText(l, W / 2, y + 12 + i * lh));
  g.restore();
}
function card(g, x, y, w, h, fill, age, o = {}) {
  const a = pop(clamp(age / 0.35, 0, 1));
  g.save(); g.translate(x + w / 2, y + h / 2); g.scale(a, a); g.rotate((o.tilt || 0) * (1 - a + 1) / 2);
  g.lineWidth = 5; g.strokeStyle = INK; g.fillStyle = fill; rr(g, -w / 2, -h / 2, w, h, o.r || 16); g.fill(); g.stroke();
  g.restore();
  return a;
}
function titleCard(g, t, title, sub, color) {
  sky(g, "sun");
  const a = pop(clamp(t / 0.6, 0, 1));
  g.save(); g.translate(W / 2, 300); g.scale(a, a); g.rotate(-0.03);
  g.fillStyle = color || "#e2512a"; g.strokeStyle = INK; g.lineWidth = 7; rr(g, -470, -110, 940, 200, 30); g.fill(); g.stroke();
  txt(g, title, 0, 20, { size: 84, font: FONT_T, color: "#fff", stroke: INK, strokeW: 12 });
  g.restore();
  if (sub) txt(g, sub, W / 2, 470, { size: 40, font: FONT_T, color: INK });
}

/* ---------- studio : minutage des scènes ---------- */
class Studio {
  constructor(g, u, meta) { this.g = g; this.u = u; this.c = 0; this.page = 0; this.meta = meta; this.rec = { pages: [0], talks: [], actors: {} }; }
  get drawing() { return !!this.g; }
  pageRange() { const p = this.meta.pages; return [p[this.page], p[this.page + 1] ?? this.meta.dur]; }
  on(start) { if (!this.g) return false; const [a, b] = this.pageRange(); return this.u >= start && this.u >= a && this.u < b; }
  newPage() { this.page++; if (!this.g) this.rec.pages.push(this.c); }
  wait(s) { this.c += s; }
  /* dessin permanent pendant la page */
  bg(fn) { if (this.on(this.c)) fn(this.g, this.u - this.pageRange()[0]); }
  /* élément qui apparaît au temps courant puis reste sur la page */
  show(fn, dur = 0) { const st = this.c; this.c += dur; if (this.on(st)) fn(this.g, this.u - st); return st; }
  actor(id, draw) { // draw(g, t, talking)
    if (!this.g) return;
    const [a, b] = this.pageRange(); if (this.u < a || this.u >= b) return;
    const talking = this.meta.talks.some(k => k.who === id && this.u >= k.s && this.u < k.e);
    draw(this.g, this.u, talking);
  }
  say(id, text, fr, box, tail, o = {}) {
    const sd = (typeof VOICE_DUR !== "undefined" && VOICE_DUR[id + "|" + text]) || 0;
    const st = this.c, d = (o.extra || 0) + Math.max(readTime(text, fr), sd ? sd + 0.9 : 0);
    if (!this.g) this.rec.talks.push({ who: id, text, s: st, e: st + (sd || text.length / 32) });
    this.c += d;
    if (this.on(st) && (o.keep || this.u < st + d + (o.linger ?? 0))) bubble(this.g, text, fr, box, tail, this.u - st, o);
    return st;
  }
}
function buildScene(fn) {
  const m = new Studio(null, 0, { pages: [0], talks: [], dur: 0 }); fn(m);
  return { fn, dur: m.c + 0.6, pages: m.rec.pages, talks: m.rec.talks };
}
function buildFilm(sceneFns) {
  const scenes = sceneFns.map(buildScene); let t = 0;
  const talks = [];
  for (const s of scenes) { s.t0 = t; for (const k of s.talks) talks.push({ who: k.who, text: k.text, t: t + k.s }); t += s.dur; }
  return { scenes, dur: t, talks };
}
function renderFrame(g, film, T) {
  const sc = film.scenes.find(s => T >= s.t0 && T < s.t0 + s.dur) || film.scenes[film.scenes.length - 1];
  const u = T - sc.t0;
  g.save(); g.clearRect(0, 0, W, H);
  const S = new Studio(g, u, { pages: sc.pages, talks: sc.talks, dur: sc.dur });
  sc.fn(S);
  g.restore();
  panelFrame(g);
  // fondu entre scènes et entre pages
  const pageStarts = sc.pages.map(p => p), near = Math.min(...pageStarts.map(p => Math.abs(u - p)), Math.abs(sc.dur - u));
  const f = clamp(1 - near / 0.25, 0, 1);
  if (f > 0) { g.fillStyle = `rgba(27,27,36,${f * 0.9})`; g.fillRect(0, 0, W, H); }
}
