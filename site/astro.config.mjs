import { defineConfig } from 'astro/config';

// Statische Ausgabe: die Seiten entstehen beim Bauen aus den JSONs, die der
// Generator schreibt. Zur Laufzeit wird nichts gerechnet und nichts geladen.
export default defineConfig({
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory' },
});
