// Usage : node render.js <film> <sortie.mp4> [fps]   |   node render.js <film> --frames t1,t2,... <dossier>
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const path = require("path"), fs = require("fs");
(async () => {
  const [film, out, extra, dir] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  p.on("pageerror", e => console.error("ERREUR PAGE:", e.message));
  await p.goto("file://" + path.join(__dirname, "page.html") + "?film=" + film);
  await p.waitForFunction(() => window.READY === true, null, { timeout: 30000 });
  const dur = await p.evaluate(() => FILM.dur);
  console.log(`durée : ${dur.toFixed(1)} s`);
  if (out === "--frames") {
    fs.mkdirSync(dir, { recursive: true });
    for (const t of extra.split(",").map(Number)) {
      const d = await p.evaluate(([t]) => drawAt(t, 0.85), [t]);
      fs.writeFileSync(path.join(dir, `f-${String(t).padStart(6, "0")}.jpg`), Buffer.from(d.split(",")[1], "base64"));
    }
    await b.close(); return;
  }
  const fps = Number(extra || 20), n = Math.ceil(dur * fps);
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-c:v", "mjpeg", "-i", "-",
    "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], { stdio: ["pipe", "inherit", "inherit"] });
  for (let i = 0; i < n; i++) {
    const d = await p.evaluate(([t]) => drawAt(t), [i / fps]);
    if (!ff.stdin.write(Buffer.from(d.split(",")[1], "base64"))) await new Promise(r => ff.stdin.once("drain", r));
    if (i % 400 === 0) console.log(`${i}/${n}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on("close", r));
  await b.close();
  console.log("terminé :", out);
})();
