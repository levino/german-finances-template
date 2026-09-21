# german-finances-template

Vorlage für eine Buchführung, die zugleich Steuerakte ist: ein Beancount-Ledger,
eine Belegablage, pro Veranlagungszeitraum eine Arbeitsmappe mit allen
ELSTER-Feldern, und eine kleine Website, die das prüfbar macht.

Gebaut für die Zusammenarbeit mit einem Agenten (Claude Code). Die Regeln, die
hier stehen, sind aus einer echten Einkommensteuererklärung entstanden — samt
der Fehler, die dabei passiert sind. Die Beispieldaten sind erfunden.

## Die eine Regel, die alles trägt

> **Beträge in einer Steuererklärung stammen aus Belegen. Der Ledger ist ein
> Suchindex, keine Belegquelle.**

Eine Buchung sagt „am 15.07. gingen 395 € an X". Sie sagt nicht, was geleistet
wurde, ob Umsatzsteuer enthalten ist und ob der Betrag abzugsfähig ist. Das
steht auf dem Beleg. Daraus folgt der ganze Rest:

- Jedes Feld der Arbeitsmappe trägt einen Status: 🟢 belegt · 🟡 Wert da, Beleg
  fehlt · 🔴 offen · ❓ zu entscheiden · ⛔ bewusst nicht erklärt.
- Ein 🟡 wird **nie** zu 🟢, ohne dass eine Datei unter `belege/` existiert.
- Fehlt ein Beleg, wird die Buchung **nicht gelöscht**. Sie bleibt und der
  fehlende Beleg wird benannt. Nur übertragen wird sie nicht.
- Kontoauszüge zählen als Beleg, wo die Gegenseite die Zahlung kennt
  (Finanzamt, Familienkasse, Bank) — sonst nicht.

## Aufbau

```
ledger/          Beancount: das Rechenwerk
belege/          die Nachweise, ein Ordner je Jahr
steuer/<jahr>/   Arbeitsmappe (Feldquelle), Stand, Erhebung, ELSTER-Übergabe
scripts/         Prüfungen, ELSTER-Export, Rechnungsstellung
site/            das Cockpit: macht die Arbeitsmappe prüfbar
docs/            Verfahrensdokumentation und Deployment
.claude/skills/  wie der Agent arbeiten soll
```

Wer neu anfängt, liest in dieser Reihenfolge: diese Datei, dann
`steuer/2025/arbeitsmappe.md`, dann `docs/lehren.md`.

## Schnellstart

```bash
python3 -m venv .venv && .venv/bin/pip install beancount
python3 scripts/beispielbelege.py          # erzeugt die Beispielbelege als PDF
.venv/bin/bean-check ledger/main.beancount
.venv/bin/python scripts/check_belege.py --year 2025
.venv/bin/python site/scripts/generate-data.py
.venv/bin/python scripts/elster_uebergabe.py 2025
cd site && npm install && npm run build
```

Die Beispieldaten sind erfunden: Mira und Jonas Beispiel, ein Honorar aus
Singapur, eine Spende, Schulgeld, eine Handwerkerrechnung, eine Dividende. Sie
zeigen jedes Muster einmal — auch zwei absichtlich offene Felder, damit
sichtbar ist, wie ein fehlender Beleg aussieht.

## Der Jahresablauf

1. **Erheben** — was liegt überhaupt vor? `steuer/<jahr>/erhebung.md` ist das
   Eingangsinterview: Familienstand, Kinder, Renten, Kapital, Vermietung,
   Ausland. Ergebnis ist eine Liste von Sachverhalten, nicht von Zahlen.
2. **Ledger aktualisieren** — Kontoauszüge importieren, `bean-check` grün.
3. **Kandidaten sammeln** — Konten durchsuchen, Ergebnis als 🟡 in die
   Arbeitsmappe, mit der Ledger-Fundstelle als Suchhinweis.
4. **Belege ablegen** — Datei nach `belege/<jahr>/`, `document:` an die
   Buchung, Feld auf 🟢, Betrag **aus dem Beleg** übernehmen.
5. **Prüfen** — `scripts/check_belege.py`, Abgleich gegen das Vorjahr: welche
   Position gab es damals, fehlt jetzt, und warum?
6. **Übertragen** — `scripts/elster_uebergabe.py <jahr>` erzeugt die Übergabe
   als Markdown und XML. Keine Zeile mit Status ≠ 🟢 ohne bewusste Entscheidung.

## Was hier absichtlich nicht drin ist

Keine Automatik, die Belege erfindet. Keine Schätzungen. Kein zweiter
Datenbestand neben dem Ledger. Und keine Steuerberatung: die Werkzeuge bereiten
auf, rechnen und zeigen Alternativen mit Argumenten — entscheiden muss der
Mensch, dem die Erklärung gehört.
