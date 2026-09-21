import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const css = fs.readFileSync(path.join(root, "styles.css"), "utf8");
const js = fs.readFileSync(path.join(root, "slides.js"), "utf8");

const slides = [...html.matchAll(/<section class="[^"]*\bslide\b[^"]*"[^>]*>/g)].map((match) => match[0]);
const errors = [];

if (slides.length < 35) errors.push(`Too few slides: ${slides.length}`);
slides.forEach((slide, index) => {
  if (!/data-section="[^"]+"/.test(slide)) errors.push(`Slide ${index + 1}: missing data-section`);
  if (!/data-title="[^"]+"/.test(slide)) errors.push(`Slide ${index + 1}: missing data-title`);
});

for (const localFile of ["styles.css", "slides.js"]) {
  if (!html.includes(localFile)) errors.push(`Missing reference to ${localFile}`);
  if (!fs.existsSync(path.join(root, localFile))) errors.push(`Missing file: ${localFile}`);
}

if (!css.includes("@media print")) errors.push("Missing print styles");
if (!js.includes("indexFromHash")) errors.push("Missing hash navigation");
if (/https?:\/\/[^"']+\.(woff2?|ttf|otf)/i.test(html + css)) errors.push("An external font breaks offline mode");

if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}

console.log(`OK: ${slides.length} slides; the presentation runs without external assets.`);
