# Cockpit

Macht die Arbeitsmappe prüfbar: Formular für Formular, Feld für Feld, mit der
Herleitung jeder Zahl aus den Buchungen. Astro, statisch gebaut.

**Kein zweiter Datenbestand.** `scripts/generate-data.py` liest Ledger,
Belegablage und Arbeitsmappe und schreibt die JSONs unter `src/data/`. Die
Seiten zeigen nur, was dort steht. Korrekturen gehören in die Quelle.

## Bauen

```bash
cd site
npm install
npm run alles     # Daten erzeugen und bauen
npm run dev       # Entwicklungsserver
```

## Die Auszeichnungen der Arbeitsmappe

`steuer/<jahr>/arbeitsmappe.md` ist die Feldquelle. `## ` Formular, `### `
Block, `#### ` Gruppe, Tabelle = Felder mit den Spalten
`Zeile / Feld | Wert | Quelle | Status`.

| Schreibweise | Wirkung |
|---|---|
| `[=](konto:Expenses:Spenden)` | Summe des Kontos im Jahr |
| `[=](konto:A+B)` | mehrere Konten |
| `[=](konto:A+!A:B)` | `!` schließt aus — so bleibt die Vorsteuer aus dem Gewinn |
| `[=](konto:A~Empfänger)` | `~` filtert auf einen Empfänger oder Buchungstext |
| `[=gewinn](konto:…)` | dreht das Vorzeichen der gemischten Summe |
| `[=](beleg:belege/2025/x.pdf)` | Summe der Buchungen zu genau diesem Beleg |
| `=` allein | Summenzeile: summiert die Zeilen derselben Nummer in der Gruppe |
| `[Text](belege/…)` | verlinkt den Beleg neben der Quelle |

Einnahmen stehen im Ledger negativ und werden fürs Formular gedreht. Nur
Buchungen mit `document:` oder `statement:` gelten als belegt.

Status: 🟢 belegt · 🟡 Wert da, Beleg fehlt · 🔴 offen · ❓ zu entscheiden ·
⛔ bewusst nicht erklärt. Stehen mehrere in einer Zeile, gewinnt die
dringendere (🔴 vor ❓ vor 🟡 vor ⛔ vor 🟢).

## Regeln

- **Ein Pfad je Jahr:** `/steuer/<jahr>/…`. Es gibt kein „aktuelles Jahr" —
  der Begriff lässt fertige Jahre aus der Ansicht fallen und verlinkt vom
  einen Jahr ins andere. Das Jahr kommt aus dem Pfad.
- **Keine Mutation:** `map`, `filter`, `reduce`, Spread statt `push`.
  Bedingte Listen entstehen als Array mit `filter(Boolean)`.
- **Keine technischen Artefakte im sichtbaren Text:** keine Dateinamen,
  keine Endungen, Belegverweise werden zu einem Link „Beleg".

## Zugangsschutz

Die Vorlage baut eine **statische** Seite ohne Anmeldung. Wer sie ins Netz
stellt, gehört hinter eine Anmeldung — die Seite enthält Belege und
Steuerdaten. Siehe `docs/deployment.md`; dort steht auch, warum eine Prüfung in
`src/middleware.ts` dafür nicht genügt.
