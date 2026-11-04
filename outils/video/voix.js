// Usage : node voix.js <film> <sortie.mp4>
// 1) liste les répliques, 2) les fait lire par espeak-ng (voix MBROLA), 3) refait le minutage,
// 4) fabrique la vidéo, 5) mixe la bande son et l'ajoute à la vidéo.
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const path = require("path"), fs = require("fs"), os = require("os");
const VOIX = {
  amy: ["-v", "mb-en1", "-p", "85", "-s", "125"],
  tom: ["-v", "mb-en1", "-p", "50", "-s", "125"],
  colombo: ["-v", "mb-fr1", "-p", "60", "-s", "135"],
};
async function talks(film) {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto("file://" + path.join(__dirname, "page.html") + "?film=" + film);
  await p.waitForFunction(() => window.READY === true, null, { timeout: 30000 });
  const r = await p.evaluate(() => ({ talks: FILM.talks, dur: FILM.dur })); await b.close(); return r;
}
const dur = (f) => Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).toString());
(async () => {
  const [film, out] = process.argv.slice(2);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "voix-"));
  const vfile = path.join(__dirname, "voix-" + film + ".js");
  if (fs.existsSync(vfile)) fs.unlinkSync(vfile);
  const first = await talks(film);
  const map = {}, files = {};
  first.talks.forEach((k, i) => {
    const key = k.who + "|" + k.text; if (files[key]) return;
    const f = path.join(tmp, `r${i}.wav`);
    const said = k.text.replace(/’/g, "'").replace(/…/g, "...").replace(/(\d) (\d{3})/g, "$1$2");
    execFileSync("espeak-ng", [...VOIX[k.who], "-w", f, said]);
    files[key] = f; map[key] = Math.round(dur(f) * 100) / 100;
  });
  fs.writeFileSync(vfile, "const VOICE_DUR = " + JSON.stringify(map) + ";\n");
  const second = await talks(film);
  console.log(`${second.talks.length} répliques, durée ${second.dur.toFixed(1)} s`);
  const video = path.join(tmp, "video.mp4");
  execFileSync("node", [path.join(__dirname, "render.js"), film, video, "20"], { stdio: "inherit" });
  const args = ["-y", "-loglevel", "error", "-i", video];
  const filt = [];
  second.talks.forEach((k, i) => { args.push("-i", files[k.who + "|" + k.text]); const ms = Math.round(k.t * 1000); filt.push(`[${i + 1}:a]adelay=${ms}|${ms},aresample=44100[a${i}]`); });
  filt.push(second.talks.map((_, i) => `[a${i}]`).join("") + `amix=inputs=${second.talks.length}:normalize=0,volume=1.3,alimiter=limit=0.9,apad[aout]`);
  const fscript = path.join(tmp, "filtre.txt"); fs.writeFileSync(fscript, filt.join(";\n"));
  args.push("-filter_complex_script", fscript, "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", "-t", second.dur.toFixed(2), "-movflags", "+faststart", out);
  execFileSync("ffmpeg", args, { stdio: "inherit" });
  console.log("terminé :", out);
})();
