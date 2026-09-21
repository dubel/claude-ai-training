import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const css = fs.readFileSync(path.join(root, "styles.css"), "utf8");
const js = fs.readFileSync(path.join(root, "slides.js"), "utf8");

const slides = [...html.matchAll(/<section class="[^"]*\bslide\b[^"]*"[^>]*>/g)].map((match) => match[0]);
const errors = [];

if (slides.length < 35) errors.push(`Za mało slajdów: ${slides.length}`);
slides.forEach((slide, index) => {
  if (!/data-section="[^"]+"/.test(slide)) errors.push(`Slajd ${index + 1}: brak data-section`);
  if (!/data-title="[^"]+"/.test(slide)) errors.push(`Slajd ${index + 1}: brak data-title`);
});

for (const localFile of ["styles.css", "slides.js"]) {
  if (!html.includes(localFile)) errors.push(`Brak odwołania do ${localFile}`);
  if (!fs.existsSync(path.join(root, localFile))) errors.push(`Brak pliku ${localFile}`);
}

if (!css.includes("@media print")) errors.push("Brak stylów druku");
if (!js.includes("indexFromHash")) errors.push("Brak nawigacji przez hash");
if (/https?:\/\/[^"']+\.(woff2?|ttf|otf)/i.test(html + css)) errors.push("Zewnętrzna czcionka łamie tryb offline");

if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}

console.log(`OK: ${slides.length} slajdów, prezentacja działa bez zewnętrznych zasobów.`);
